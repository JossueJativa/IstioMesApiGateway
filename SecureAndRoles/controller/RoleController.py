from flask import Blueprint, request, jsonify, current_app, make_response
from utils.database import db
from model.Role import Role

role_blueprint = Blueprint('role_blueprint', __name__)

@role_blueprint.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = Role.query.all()
        return jsonify([role.to_dict() for role in roles]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching roles: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@role_blueprint.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return make_response(jsonify({'error': 'Role not found'}), 404)
        return jsonify(role.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching role {role_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@role_blueprint.route('/roles', methods=['POST'])
def create_role():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return make_response(jsonify({'error': 'Bad Request: Missing name'}), 400)
        
        new_role = Role(name=data['name'])
        db.session.add(new_role)
        db.session.commit()
        
        return jsonify(new_role.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error creating role: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@role_blueprint.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return make_response(jsonify({'error': 'Role not found'}), 404)
        
        data = request.get_json()
        if not data or 'name' not in data:
            return make_response(jsonify({'error': 'Bad Request: Missing name'}), 400)
        
        role.name = data['name']
        db.session.commit()
        
        return jsonify(role.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error updating role {role_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    
@role_blueprint.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return make_response(jsonify({'error': 'Role not found'}), 404)
        
        db.session.delete(role)
        db.session.commit()
        
        return jsonify({'message': 'Role deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting role {role_id}: {e}")
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)