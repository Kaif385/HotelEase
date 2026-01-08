from flask import Blueprint, render_template
from sqlalchemy import text
from app import db

report_bp = Blueprint('reports', __name__, url_prefix='/admin/reports')

@report_bp.route('/')
def analytics_dashboard():
    # 1. VIEW Usage: RoomOccupancy (Existing)
    occupancy_view = db.session.execute(text("SELECT * FROM RoomOccupancy")).fetchall()

    # 2. VIEW Usage: ShiftOverlap (NEW - Matches your SQL file)
    shift_buddies = db.session.execute(text("SELECT * FROM ShiftOverlap")).fetchall()

    # 3. VIEW Usage: PackagePossibilities (NEW - Matches your SQL file)
    # We fetch top 5 just to show the Cross Join works
    packages = db.session.execute(text("SELECT * FROM PackagePossibilities LIMIT 5")).fetchall()

    # 4. Complex Query: VIP Guest Ranking (Using your GetGuestLevel Function)
    vip_guests = db.session.execute(text("""
        SELECT g.full_name,
        (IFNULL(SUM(b.total_amount), 0) + IFNULL(SUM(so.total_order_cost), 0)) AS total_lifetime_spent,
        GetGuestLevel((IFNULL(SUM(b.total_amount), 0) + IFNULL(SUM(so.total_order_cost), 0))) AS vip_status
        FROM Guests g
        LEFT JOIN Bookings b ON g.guest_id = b.guest_id
        LEFT JOIN ServiceOrders so ON b.booking_id = so.booking_id
        GROUP BY g.guest_id
        ORDER BY total_lifetime_spent DESC LIMIT 5
    """)).fetchall()

    # 5. Complex Query: High Value Services
    top_services = db.session.execute(text("""
        SELECT s.service_name, SUM(so.total_order_cost) AS total_revenue
        FROM Services s
        JOIN ServiceOrders so ON s.service_id = so.service_id
        GROUP BY s.service_name
        HAVING total_revenue > 1000
    """)).fetchall()
    
    # 6. Unused Room Types (Subquery)
    unused_rooms = db.session.execute(text("""
        SELECT name, base_price FROM RoomTypes 
        WHERE type_id NOT IN (
            SELECT DISTINCT r.type_id FROM Rooms r 
            JOIN Bookings b ON r.room_id = b.room_id
        )
    """)).fetchall()

    # 7. Group Concat (String Aggregation)
    service_summary = db.session.execute(text("""
        SELECT b.booking_id, g.full_name,
        GROUP_CONCAT(s.service_name SEPARATOR ', ') AS services_ordered
        FROM Bookings b
        JOIN Guests g ON b.guest_id = g.guest_id
        JOIN ServiceOrders so ON b.booking_id = so.booking_id
        JOIN Services s ON so.service_id = s.service_id
        GROUP BY b.booking_id
    """)).fetchall()

    return render_template('admin/reports.html',
                           occupancy=occupancy_view,
                           vip_guests=vip_guests,
                           top_services=top_services,
                           shift_buddies=shift_buddies,
                           unused_rooms=unused_rooms,
                           service_summary=service_summary,
                           packages=packages)