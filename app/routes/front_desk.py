# app/routes/front_desk.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from app import db
# Import the new helper
from app.services.db_utils import check_availability_proc

front_desk_bp = Blueprint('front_desk', __name__, url_prefix='/reception')

@front_desk_bp.route('/')
@front_desk_bp.route('/room-grid')
def room_grid():
    # 1. VIEW Usage: RoomOccupancy (As defined in your SQL)
    # We join it with the Rooms table to show the grid
    query = text("""
        SELECT r.room_id, r.room_number, r.status, rt.name as type_name, rt.base_price,
               COALESCE(v.total_bookings, 0) as historical_bookings
        FROM Rooms r
        JOIN RoomTypes rt ON r.type_id = rt.type_id
        LEFT JOIN RoomOccupancy v ON r.room_number = v.room_number
        ORDER BY r.room_number
    """)
    rooms = db.session.execute(query).fetchall()
    return render_template('reception/room_grid.html', rooms=rooms)

@front_desk_bp.route('/book', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        guest_id = request.form.get('guest_id')
        room_id = request.form.get('room_id')
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        total_price = request.form.get('total_price')

        # TCL: START TRANSACTION
        # Flask-SQLAlchemy handles 'START TRANSACTION' automatically when we use try/except
        try:
            # 1. Attempt to Insert (This will fire the 'PreventDoubleBooking' Trigger)
            query = text("""
                INSERT INTO Bookings (guest_id, room_id, check_in, check_out, total_amount)
                VALUES (:g, :r, :cin, :cout, :amt)
            """)
            db.session.execute(query, {
                'g': guest_id, 'r': room_id, 'cin': check_in, 'cout': check_out, 'amt': total_price
            })
            
            # 2. Update Room Status
            update_room = text("UPDATE Rooms SET status = 'booked' WHERE room_id = :rid")
            db.session.execute(update_room, {'rid': room_id})
            
            # TCL: COMMIT
            db.session.commit()
            
            flash('Booking Created Successfully!', 'success')
            return redirect(url_for('front_desk.room_grid'))
            
        except Exception as e:
            # TCL: ROLLBACK
            db.session.rollback()
            
            # Check if it's our specific Trigger error
            error_msg = str(e)
            if "Room is already booked" in error_msg:
                flash('Error: This room is already booked for those dates! (Trigger Activated)', 'danger')
            else:
                flash(f'Database Error: {error_msg}', 'danger')

    # Load Form Data
    guests = db.session.execute(text("SELECT * FROM Guests")).fetchall()
    
    # Use the Stored Procedure for availability? 
    # (Optional: In a real app, you'd filter the dropdown. For now, we list all rooms)
    rooms = db.session.execute(text("SELECT r.room_id, r.room_number, rt.name, rt.base_price FROM Rooms r JOIN RoomTypes rt ON r.type_id = rt.type_id")).fetchall()
    
    return render_template('reception/booking_form.html', guests=guests, rooms=rooms)


@front_desk_bp.route('/invoice/<int:booking_id>')
def invoice(booking_id):
    # 1. Fetch Booking & Guest Info
    booking_sql = text("""
        SELECT b.booking_id, b.check_in, b.check_out, b.total_amount, 
            g.full_name, g.phone, g.email
        FROM Bookings b
        JOIN Guests g ON b.guest_id = g.guest_id
        WHERE b.booking_id = :bid
    """)
    booking = db.session.execute(booking_sql, {'bid': booking_id}).fetchone()

    # 2. Fetch Services ordered by this booking
    services_sql = text("""
        SELECT s.service_name, so.quantity, so.total_order_cost 
        FROM ServiceOrders so
        JOIN Services s ON so.service_id = s.service_id
        WHERE so.booking_id = :bid
    """)
    services = db.session.execute(services_sql, {'bid': booking_id}).fetchall()

    # 3. Calculate Final Total
    service_total = sum(s.total_order_cost for s in services)
    final_total = booking.total_amount + service_total

    return render_template('reception/invoice.html', 
                        booking=booking, 
                        services=services, 
                        final_total=final_total)

# --- BOOKING MANAGEMENT (Completes the remaining DB Concepts) ---

@front_desk_bp.route('/booking/<int:booking_id>', methods=['GET', 'POST'])
def booking_details(booking_id):
    """
    Shows details for a specific booking.
    Allows adding services (Trigger Test) and Checking Out (Stored Proc Test).
    """
    # 1. Fetch Basic Booking Info
    booking = db.session.execute(text("""
        SELECT b.*, g.full_name, r.room_number 
        FROM Bookings b
        JOIN Guests g ON b.guest_id = g.guest_id
        JOIN Rooms r ON b.room_id = r.room_id
        WHERE b.booking_id = :bid
    """), {'bid': booking_id}).fetchone()

    # 2. Add Service Logic (trigger: BeforeServiceOrderInsert)
    if request.method == 'POST' and 'service_id' in request.form:
        service_id = request.form.get('service_id')
        quantity = request.form.get('quantity')
        
        try:
            # Note: We do NOT insert 'total_order_cost'. 
            # We let the MySQL TRIGGER calculate it automatically.
            db.session.execute(text("""
                INSERT INTO ServiceOrders (booking_id, service_id, quantity)
                VALUES (:bid, :sid, :qty)
            """), {'bid': booking_id, 'sid': service_id, 'qty': quantity})
            db.session.commit()
            flash('Service added! The DB Trigger automatically calculated the cost.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding service: {e}', 'danger')
        
        return redirect(url_for('front_desk.booking_details', booking_id=booking_id))

    # 3. Fetch Services for this booking
    # COVERS COMPLEX QUERY #11: GROUP_CONCAT isn't needed here for display, 
    # but we list them normally. We will put GROUP_CONCAT in the reports.
    ordered_services = db.session.execute(text("""
        SELECT so.*, s.service_name 
        FROM ServiceOrders so
        JOIN Services s ON so.service_id = s.service_id
        WHERE so.booking_id = :bid
    """), {'bid': booking_id}).fetchall()

    # 4. Fetch Available Services for dropdown
    all_services = db.session.execute(text("SELECT * FROM Services")).fetchall()

    return render_template('reception/booking_details.html', 
                           booking=booking, 
                           ordered_services=ordered_services, 
                           all_services=all_services)

@front_desk_bp.route('/checkout/<int:booking_id>', methods=['POST'])
def checkout_guest(booking_id):
    """
    COVERS STORED PROCEDURE: CompleteBooking
    """
    try:
        # We use the raw connection to call the procedure
        # Procedure: UPDATE Bookings SET status='completed'; UPDATE Rooms SET status='available'
        from app.services.db_utils import complete_booking_proc
        complete_booking_proc(booking_id)
        
        flash('Guest Checked Out Successfully (Stored Procedure Executed)', 'success')
    except Exception as e:
        flash(f'Checkout Failed: {e}', 'danger')
        
    return redirect(url_for('front_desk.room_grid'))