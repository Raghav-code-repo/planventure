from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No Authorization header'}), 401
            
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Invalid token format',
                'message': str(e)
            }), 401
    return decorated_function

def get_current_user():
    try:
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        from models.user import User
        user = User.query.get(user_id)
        if not user:
            raise Exception('User not found')
        return user
    except Exception as e:
        return None
