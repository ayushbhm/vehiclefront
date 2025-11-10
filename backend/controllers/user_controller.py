from sqlalchemy import desc
from app import app, db
from flask import jsonify, render_template, redirect, url_for, flash
from controllers.helper import (
    ensure_role,
    get_client_user_id,
    get_daywise_booking_data,
    unauthorized_response,
    _wants_json_response,
    optional_login_required,
)
from models import ParkingLot, ParkingSpot, Reservation, User
from datetime import datetime
from flask_login import login_required, current_user
from login_manager import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def _resolve_request_user_id():
    """Resolve the user id from the request headers or current session."""
    user_id = get_client_user_id()
    if user_id is not None:
        return user_id
    if current_user.is_authenticated:
        return current_user.id
    return None

@app.route('/user/lots')
@optional_login_required
def user_lots():
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized
    lots = ParkingLot.query.all()
    
    lots_with_status = []
    for lot in lots:
        total_spots = lot.max_spots
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        available = total_spots - occupied
        lots_with_status.append({
            'lot': lot,
            'available': available,
            'occupied': occupied
        })
    return render_template('user_lots.html', lots=lots_with_status)

@app.route('/user/book/<int:lot_id>', methods=['POST'])
@optional_login_required
def book_spot(lot_id):
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized
    
    wants_json = _wants_json_response()
    
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        if wants_json:
            return jsonify({'error': 'No spots available in this lot!'}), 400
        flash('No spots available in this lot!')
        return redirect(url_for('user_lots'))

    user_id = _resolve_request_user_id()
    if user_id is None:
        if wants_json:
            return jsonify({'error': 'User ID missing for booking'}), 401
        return unauthorized_response(message='User ID missing for booking', redirect_endpoint='user_lots')

    spot.status = 'O'
    db.session.add(spot)
    db.session.commit()

    reservation = Reservation(
        spot_id=spot.id,
        user_id=user_id,
        parking_timestamp=datetime.utcnow()
    )
    db.session.add(reservation)
    db.session.commit()

    if wants_json:
        return jsonify({
            'message': f'Spot {spot.id} booked successfully!',
            'reservation_id': reservation.id,
            'spot_id': spot.id
        }), 200
    
    flash(f'Spot {spot.id} booked successfully!')
    return redirect(url_for('user_reservations'))

@app.route('/user/reservations')
@optional_login_required
def user_reservations():
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized

    user_id = _resolve_request_user_id()
    if user_id is None:
        return unauthorized_response(message='User ID missing for reservations', redirect_endpoint='user_lots')

    reservations = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).all()
    return render_template('user_reservations.html', reservations=reservations)

@app.route('/user/release/<int:res_id>', methods=['POST'])
@optional_login_required
def release_spot(res_id):
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized

    wants_json = _wants_json_response()
    
    reservation = Reservation.query.get_or_404(res_id)
    requester_user_id = _resolve_request_user_id()
    if requester_user_id is None:
        if wants_json:
            return jsonify({'error': 'User ID missing for release'}), 401
        return unauthorized_response(message='User ID missing for release', redirect_endpoint='user_reservations')

    if reservation.user_id != requester_user_id:
        if wants_json:
            return jsonify({'error': 'Unauthorized release!'}), 403
        flash('Unauthorized release!')
        return redirect(url_for('user_reservations'))

    spot = ParkingSpot.query.get(reservation.spot_id)
    spot.status = 'A'
    db.session.add(spot)

    reservation.leaving_timestamp = datetime.utcnow()
    reservation.cost = spot.lot.price
    db.session.commit()

    if wants_json:
        return jsonify({
            'message': f'Spot {spot.id} released. Cost: ₹{reservation.cost}',
            'cost': reservation.cost
        }), 200
    
    flash(f'Spot {spot.id} released. Cost: ₹{reservation.cost}')
    return redirect(url_for('user_reservations'))

@app.route('/user/history')
@optional_login_required
def user_history():
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized

    user_id = _resolve_request_user_id()
    if user_id is None:
        return unauthorized_response(message='User ID missing for history', redirect_endpoint='user_dashboard')
    
    history = (Reservation.query
                .filter_by(user_id=user_id)
                .order_by(Reservation.parking_timestamp.desc())
                .all())
    return render_template('user_history.html', history=history)

@app.route('/user/dashboard')
@optional_login_required
def user_dashboard():
    unauthorized = ensure_role('user')
    if unauthorized:
        return unauthorized

    user_id = _resolve_request_user_id()
    if user_id is None:
        return unauthorized_response(message='User ID missing for dashboard', redirect_endpoint='user_dashboard')
    
    active_reservations = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).all()
    active_count = len(active_reservations)

    history_reservations = Reservation.query.filter(
        Reservation.user_id == user_id,
        Reservation.leaving_timestamp.isnot(None)
    ).all()
    history_count = len(history_reservations)
    total_cost = sum([res.cost or 0 for res in history_reservations])

    recent_reservations = Reservation.query.filter_by(user_id=user_id)\
        .order_by(desc(Reservation.parking_timestamp)).limit(5).all()

    chart_labels, chart_data = get_daywise_booking_data(user_id)

    return render_template(
        'user_dashboard.html',
        active_count=active_count,
        history_count=history_count,
        total_cost=total_cost,
        recent_reservations=recent_reservations,
        chart_labels=chart_labels,
        chart_data=chart_data
    )