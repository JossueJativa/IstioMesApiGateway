from flask import Blueprint, request, jsonify
from utils.database import db
from model.User import User
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from flask import current_app, make_response
from utils.auth import token_required

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/users', methods=['GET'])
@token_required
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching users: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        user_data = user.to_dict()
        return jsonify(user_data), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching user {user_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@user_blueprint.route('/users', methods=['POST'])
@token_required
def create_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password' not in data or 'role_id' not in data:
            return make_response(jsonify({'error': 'Bad Request: Missing required fields'}), 400)
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role_id=data['role_id']
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error creating user: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'role_id' not in data:
            return make_response(jsonify({'error': 'Bad Request: Missing required fields'}), 400)
        
        user.username = data['username']
        user.email = data['email']
        user.role_id = data['role_id']
        
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        
        db.session.commit()
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error updating user {user_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting user {user_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return make_response(jsonify({'error': 'Bad Request: Missing username or password'}), 400)
        
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return make_response(jsonify({'error': 'Invalid credentials'}), 401)
        
        token = jwt.encode({'user_id': user.id}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    except Exception as e:
        current_app.logger.error(f"Error during login: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@user_blueprint.route('/verify', methods=['GET'])
def verify():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    if not token:
        return make_response(jsonify({'error': 'Token is missing!'}), 401)
    try:
        jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True}), 200
    except Exception:
        return make_response(jsonify({'valid': False}), 401)