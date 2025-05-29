from functools import wraps
from flask import request, jsonify, make_response, current_app
import requests

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
        # Validar el token usando el microservicio de autenticación
        if not verify_token_http(token):
            return make_response(jsonify({'error': 'Token is invalid!'}), 401)
        return f(*args, **kwargs)
    return decorated

def verify_token_http(token, auth_service_url='http://localhost:5000/verify'):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(auth_service_url, headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception:
        return False
