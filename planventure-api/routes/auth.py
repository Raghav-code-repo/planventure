from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    try:
        # Validate email
        valid = validate_email(data['email'])
        email = valid.email
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(email=email)
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token()
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {'id': user.id, 'email': user.email}
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    try:
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            token = user.generate_auth_token()
            return jsonify({
                'token': token,
                'user': {'id': user.id, 'email': user.email}
            }), 200
        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
