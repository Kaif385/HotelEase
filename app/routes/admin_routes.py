# app/routes/admin_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import text
from app import db

# Create the Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- DASHBOARD ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    # 1. Fetch Live Data
    guest_count = db.session.execute(text("SELECT COUNT(*) FROM Guests")).scalar()
    
    # Calculate Total Revenue
    revenue_sql = text("""
        SELECT 
        (SELECT IFNULL(SUM(total_amount), 0) FROM Bookings) + 
        (SELECT IFNULL(SUM(total_order_cost), 0) FROM ServiceOrders)
    """)
    total_revenue = db.session.execute(revenue_sql).scalar()
    
    # Count Available Rooms
    room_count = db.session.execute(text("SELECT COUNT(*) FROM Rooms WHERE status = 'available'")).scalar()

    # Get Recent Bookings
    recent_bookings = db.session.execute(text("""
        SELECT b.booking_id, g.full_name, b.check_in, b.booking_status, b.total_amount
        FROM Bookings b
        JOIN Guests g ON b.guest_id = g.guest_id
        ORDER BY b.booking_id DESC
        LIMIT 5
    """)).fetchall()

    return render_template('admin/dashboard.html', 
                           guest_count=guest_count,
                           total_revenue=total_revenue,
                           room_count=room_count,
                           recent_bookings=recent_bookings)

# --- AUDIT LOGS ---
@admin_bp.route('/audit-logs')
def audit_logs():
    logs = db.session.execute(text("SELECT * FROM AuditLog ORDER BY action_timestamp DESC")).fetchall()
    return render_template('admin/audit_logs.html', logs=logs)

# --- EMPLOYEES ---
@admin_bp.route('/employees')
def employees():
    sql = text("SELECT * FROM Employees ORDER BY hire_date DESC")
    employees_data = db.session.execute(sql).fetchall()
    return render_template('admin/employees.html', employees=employees_data)

# --- GUEST MANAGEMENT ---
@admin_bp.route('/guests')
def manage_guests():
    """
    Renders the Guest Management Page.
    """
    query = text("""
        SELECT g.guest_id, g.full_name, g.phone, g.email, g.nationality,
               (SELECT COUNT(*) FROM Bookings b WHERE b.guest_id = g.guest_id) as total_bookings
        FROM Guests g
        ORDER BY g.guest_id DESC
    """)
    guests = db.session.execute(query).fetchall()
    return render_template('admin/guests.html', guests=guests)

@admin_bp.route('/guests/delete/<int:guest_id>', methods=['POST'])
def delete_guest(guest_id):
    """
    Deletes a guest. 
    NOTE: This action will automatically fire the MySQL Trigger 'LogGuestDeletion'.
    """
    try:
        # Execute Delete
        db.session.execute(text("DELETE FROM Guests WHERE guest_id = :gid"), {'gid': guest_id})
        db.session.commit()
        
        flash('Guest record deleted successfully. The Audit Log has been updated via Trigger.', 'success')
    except Exception as e:
        db.session.rollback()
        if "foreign key constraint" in str(e).lower():
            flash('Cannot delete this guest because they have existing booking records.', 'danger')
        else:
            flash(f'Error deleting guest: {str(e)}', 'danger')
            
    return redirect(url_for('admin.manage_guests'))