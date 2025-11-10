from flask import jsonify
from app import app
from models import ParkingLot, ParkingSpot, Reservation
from flask_login import current_user

from controllers.helper import get_client_role, get_client_user_id, unauthorized_response, optional_login_required


# APIs
@app.route('/api/lots', methods=['GET'])
def api_lots():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        total = lot.max_spots
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        available = total - occupied
        data.append({
            'id': lot.id,
            'name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'total_spots': total,
            'occupied': occupied,
            'available': available
        })
    return jsonify(data)

@app.route('/api/lots/<int:lot_id>', methods=['GET'])
def api_lot_detail(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    spots_data = [{'id': s.id, 'status': s.status} for s in spots]
    data = {
        'id': lot.id,
        'name': lot.prime_location_name,
        'price': lot.price,
        'address': lot.address,
        'pincode': lot.pincode,
        'total_spots': lot.max_spots,
        'spots': spots_data
    }
    return jsonify(data)

@app.route('/api/spots/<int:spot_id>', methods=['GET'])
@optional_login_required
def api_spot_detail(spot_id):
    if get_client_role() != 'admin':
        return unauthorized_response()
    spot = ParkingSpot.query.get_or_404(spot_id)
    data = {
        'id': spot.id,
        'lot_id': spot.lot_id,
        'status': spot.status
    }
    return jsonify(data)

@app.route('/api/user/<int:user_id>/reservations', methods=['GET'])
@optional_login_required
def api_user_reservations(user_id):
    client_role = get_client_role()
    client_user_id = get_client_user_id()
    session_user_id = current_user.id if current_user.is_authenticated else None

    if client_role != 'admin' and client_user_id != user_id and session_user_id != user_id:
        return unauthorized_response()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    data = []
    for r in reservations:
        data.append({
            'id': r.id,
            'spot_id': r.spot_id,
            'lot_name': r.spot.lot.prime_location_name,
            'parking_timestamp': r.parking_timestamp.isoformat() if r.parking_timestamp else None,
            'leaving_timestamp': r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
            'cost': r.cost
        })
    return jsonify(data)

