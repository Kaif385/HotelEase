from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import text
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    # If user is already logged in, send them to dashboard
    if 'user_id' in session:
        return redirect(url_for('admin.dashboard'))
    # Otherwise, send them to login
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # --- Industry Standard: Never store plain text passwords. 
        # (For this student project, we compare plain text as per your SQL Insert)
        query = text("SELECT * FROM Users WHERE username = :u AND password = :p")
        user = db.session.execute(query, {'u': username, 'p': password}).fetchone()
        
        if user:
            session['user_id'] = user.user_id
            session['role'] = user.role
            flash('Login Successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))