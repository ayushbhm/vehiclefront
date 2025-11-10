from flask import current_app, render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from itsdangerous import URLSafeTimedSerializer as Serializer
from controllers.helper import _wants_json_response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw, role='user')
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

def generate_token(user_id, role):
    """Generate a token for the user."""
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user_id, 'role': role}, salt='auth-token')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if request wants JSON response
        wants_json = _wants_json_response() or request.is_json
        
        if wants_json:
            # JSON request from Vue
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            # Form request (legacy)
            username = request.form.get('username')
            password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            if wants_json:
                # Return JSON with token and role
                token = generate_token(user.id, user.role)
                return jsonify({
                    'access_token': token,
                    'role': user.role,
                    'user_id': user.id
                }), 200
            else:
                # Legacy form-based login
                login_user(user)
                flash('Logged in successfully.')
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
        else:
            if wants_json:
                return jsonify({'error': 'Invalid username or password'}), 401
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))