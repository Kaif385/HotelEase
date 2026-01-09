from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import text
from app import db

auth_bp = Blueprint('auth', __name__)

# -------------------------------------------------
# Home Route
# -------------------------------------------------
@auth_bp.route('/')
def index():
    # If user already logged in → go to dashboard
    if 'user_id' in session:
        return redirect(url_for('admin.dashboard'))

    # Otherwise → go to login page
    return redirect(url_for('auth.login'))


# -------------------------------------------------
# Login Route
# -------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Raw SQL query (safe using named parameters)
        query = text("""
            SELECT user_id, username, role
            FROM Users
            WHERE username = :u AND password = :p
        """)

        result = db.session.execute(query, {
            'u': username,
            'p': password
        })

        # Convert Row → dict-like object
        user = result.mappings().fetchone()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']

            flash('Login Successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')


# -------------------------------------------------
# Logout Route
# -------------------------------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
