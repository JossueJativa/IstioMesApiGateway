from functools import wraps
from flask import request, jsonify, make_response, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return make_response(jsonify({'error': 'Token is missing!'}), 401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except Exception as e:
            return make_response(jsonify({'error': 'Token is invalid!'}), 401)
        return f(*args, **kwargs)
    return decorated
