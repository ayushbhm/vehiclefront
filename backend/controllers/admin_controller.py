from flask import jsonify, render_template, request, redirect, url_for, flash
from app import app, db
from models import ParkingLot, ParkingSpot, Reservation
from flask_login import login_required
from collections import defaultdict

from controllers.helper import ensure_role, _wants_json_response, optional_login_required

@app.route('/admin/lots')
@optional_login_required
def admin_lots():
    unauthorized = ensure_role('admin')
    if unauthorized:
        return unauthorized
    lots = ParkingLot.query.all()
    return render_template('admin_lots.html', lots=lots)

@app.route('/admin/lots/create', methods=['GET', 'POST'])
@optional_login_required
def create_lot():
    unauthorized = ensure_role('admin')
    if unauthorized:
        return unauthorized

    wants_json = _wants_json_response()
    
    if request.method == 'POST':
        if wants_json:
            data = request.get_json()
            name = data.get('name')
            price = float(data.get('price', 0))
            address = data.get('address', '')
            pincode = data.get('pincode', '')
            max_spots = int(data.get('max_spots', 0))
        else:
            name = request.form.get('name')
            price = float(request.form.get('price', 0))
            address = request.form.get('address', '')
            pincode = request.form.get('pincode', '')
            max_spots = int(request.form.get('max_spots', 0))

        if not name or max_spots <= 0:
            if wants_json:
                return jsonify({'error': 'Name and max_spots are required'}), 400
            flash('Name and max_spots are required')
            return redirect(url_for('admin_lots'))

        lot = ParkingLot(
            prime_location_name=name,
            price=price,
            address=address,
            pincode=pincode,
            max_spots=max_spots
        )
        db.session.add(lot)
        db.session.commit()

        for _ in range(max_spots):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)
        db.session.commit()

        if wants_json:
            return jsonify({
                'message': 'Parking lot created successfully!',
                'lot_id': lot.id
            }), 200
        
        flash('Parking lot created successfully!')
        return redirect(url_for('admin_lots'))

    return render_template('create_lot.html')

@app.route('/admin/lots/edit/<int:lot_id>', methods=['GET', 'POST'])
@optional_login_required
def edit_lot(lot_id):
    unauthorized = ensure_role('admin')
    if unauthorized:
        return unauthorized

    wants_json = _wants_json_response()
    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        if wants_json:
            data = request.get_json()
            name = data.get('name')
            price = float(data.get('price', 0))
            address = data.get('address', '')
            pincode = data.get('pincode', '')
            new_max_spots = int(data.get('max_spots', 0))
        else:
            name = request.form.get('name')
            price = float(request.form.get('price', 0))
            address = request.form.get('address', '')
            pincode = request.form.get('pincode', '')
            new_max_spots = int(request.form.get('max_spots', 0))

        lot.prime_location_name = name
        lot.price = price
        lot.address = address
        lot.pincode = pincode

        if new_max_spots > lot.max_spots:
            # Add new spots
            for _ in range(new_max_spots - lot.max_spots):
                db.session.add(ParkingSpot(lot_id=lot.id, status='A'))

        elif new_max_spots < lot.max_spots:
            # Only delete spots that are available AND have no reservations
            spots_to_remove = lot.max_spots - new_max_spots
            # Get available spots that have no reservations
            available_spots = ParkingSpot.query.filter_by(
                lot_id=lot.id, 
                status='A'
            ).all()
            
            # Filter spots that have no reservations
            removable_spots = []
            for spot in available_spots:
                reservation_count = Reservation.query.filter_by(spot_id=spot.id).count()
                if reservation_count == 0:
                    removable_spots.append(spot)
                if len(removable_spots) >= spots_to_remove:
                    break
            
            if len(removable_spots) < spots_to_remove:
                if wants_json:
                    return jsonify({
                        'error': f'Cannot reduce spots. Only {len(removable_spots)} spots can be removed (need to remove {spots_to_remove}). Some spots have reservations or are occupied.'
                    }), 400
                flash(f'Cannot reduce spots. Only {len(removable_spots)} spots can be removed. Some spots have reservations or are occupied.')
                return redirect(url_for('admin_lots'))
            
            # Delete only spots without reservations
            for spot in removable_spots:
                db.session.delete(spot)

        lot.max_spots = new_max_spots
        db.session.commit()
        
        if wants_json:
            return jsonify({
                'message': 'Parking lot updated!',
                'lot_id': lot.id
            }), 200
        
        flash('Parking lot updated!')
        return redirect(url_for('admin_lots'))

    return render_template('edit_lot.html', lot=lot)

@app.route('/admin/lots/delete/<int:lot_id>', methods=['POST'])
@optional_login_required
def delete_lot(lot_id):
    unauthorized = ensure_role('admin')
    if unauthorized:
        return unauthorized

    wants_json = _wants_json_response()
    lot = ParkingLot.query.get_or_404(lot_id)
    
    # Check for occupied spots (active reservations)
    occupied_count = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    if occupied_count > 0:
        if wants_json:
            return jsonify({'error': 'Cannot delete lot with occupied spots! Please wait for all active reservations to be released.'}), 400
        flash('Cannot delete lot with occupied spots! Please wait for all active reservations to be released.')
        return redirect(url_for('admin_lots'))
    
    # Check for active reservations (not yet released)
    all_spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    spots_with_active_reservations = []
    for spot in all_spots:
        # Check for active reservations (where leaving_timestamp is NULL)
        active_reservation = Reservation.query.filter_by(
            spot_id=spot.id,
            leaving_timestamp=None
        ).first()
        if active_reservation:
            spots_with_active_reservations.append(spot.id)
    
    if spots_with_active_reservations:
        if wants_json:
            return jsonify({
                'error': f'Cannot delete lot. Spots {spots_with_active_reservations} have active reservations. Please wait for all reservations to be released.'
            }), 400
        flash(f'Cannot delete lot. Some spots have active reservations.')
        return redirect(url_for('admin_lots'))

    # Safe to delete - no occupied spots and no active reservations
    # Historical reservations will be cascade deleted along with spots
    db.session.delete(lot)
    db.session.commit()
    
    if wants_json:
        return jsonify({'message': 'Parking lot deleted successfully!'}), 200
    
    flash('Parking lot deleted!')
    return redirect(url_for('admin_lots'))

@app.route('/admin/dashboard')
@optional_login_required
def admin_dashboard():
    unauthorized = ensure_role('admin')
    if unauthorized:
        return unauthorized

    total_spots = ParkingSpot.query.count()
    occupied = ParkingSpot.query.filter_by(status='O').count()
    available = ParkingSpot.query.filter_by(status='A').count()

    day_bookings = defaultdict(int)
    reservations = Reservation.query.all()
    for r in reservations:
        if r.parking_timestamp:
            day_key = r.parking_timestamp.strftime("%Y-%m-%d")
            day_bookings[day_key] += 1

    sorted_days = sorted(day_bookings.keys())
    booking_labels = sorted_days
    booking_counts = [day_bookings[d] for d in sorted_days]

    return render_template(
        'admin_dashboard.html',
        total_spots=total_spots,
        occupied=occupied,
        available=available,
        booking_labels=booking_labels,
        booking_counts=booking_counts
    )
