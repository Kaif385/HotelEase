from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

guest_api_bp = Blueprint('guest_api', __name__, url_prefix='/api/guests')

@guest_api_bp.route('/search')
def search_guest():
    query_str = request.args.get('q', '')
    if not query_str:
        return jsonify([])
        
    sql = text("SELECT guest_id, full_name, phone FROM Guests WHERE full_name LIKE :q OR phone LIKE :q")
    results = db.session.execute(sql, {'q': f'%{query_str}%'}).fetchall()
    
    # Convert to JSON format
    guests_list = [{'id': r.guest_id, 'text': f"{r.full_name} ({r.phone})"} for r in results]
    return jsonify(guests_list)