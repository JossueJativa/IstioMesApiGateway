from utils.database import db
from datetime import datetime

class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    detalle = db.Column(db.String(200))
    username = db.Column(db.String(100), nullable=False)  # Nuevo campo para guardar el username

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'usuario_id': self.usuario_id,
            'estado': self.estado,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'detalle': self.detalle,
            'username': self.username
        }