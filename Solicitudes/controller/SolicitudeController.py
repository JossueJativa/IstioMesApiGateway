from flask import request, jsonify, make_response, Blueprint
from model.Solicitud import Solicitud
from utils.database import db
from utils.soap_certificado import obtener_certificado_soap
from utils.token import token_required

solicitudes_blueprint = Blueprint('solicitudes_blueprint', __name__)

@solicitudes_blueprint.route('/solicitudes', methods=['POST'])
@token_required
def crear_solicitud():
    data = request.get_json()
    # Validar campos requeridos
    if not data or 'tipo' not in data or 'usuario_id' not in data or 'detalle' not in data or 'username' not in data:
        return make_response(jsonify({'error': 'Bad Request: Missing required fields'}), 400)
    
    solicitud = Solicitud(
        tipo=data['tipo'],
        usuario_id=data['usuario_id'],
        estado='pendiente',
        detalle=data['detalle'],
        username=data['username']  # Guardar el username
    )

    try:
        db.session.add(solicitud)
        db.session.commit()
        certificado = obtener_certificado_soap(solicitud.id, solicitud.username)
        solicitud.certificado = certificado
        db.session.commit()
        return jsonify(solicitud.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': f'Internal Server Error: {str(e)}'}), 500)

@solicitudes_blueprint.route('/solicitudes/<int:solicitud_id>', methods=['GET'])
@token_required
def obtener_solicitud(solicitud_id):
    solicitud = Solicitud.query.get(solicitud_id)
    if not solicitud:
        return make_response(jsonify({'error': 'Solicitud no encontrada'}), 404)
    certificado = obtener_certificado_soap(solicitud.id, solicitud.username)
    return jsonify({**solicitud.to_dict(), 'certificado': certificado}), 200

@solicitudes_blueprint.route('/solicitudes/<int:solicitud_id>', methods=['PATCH'])
@token_required
def actualizar_estado_solicitud(solicitud_id):
    data = request.get_json()
    if not data or 'estado' not in data:
        return make_response(jsonify({'error': 'Bad Request: Missing "estado" field'}), 400)
    solicitud = Solicitud.query.get(solicitud_id)
    if not solicitud:
        return make_response(jsonify({'error': 'Solicitud no encontrada'}), 404)
    try:
        solicitud.estado = data['estado']
        db.session.commit()
        return jsonify({'id': solicitud.id, 'estado': solicitud.estado}), 200
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': f'Internal Server Error: {str(e)}'}), 500)