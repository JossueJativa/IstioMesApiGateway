from flask import Flask
from controller.SolicitudeController import solicitudes_blueprint
from utils.database import db
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solicitudes.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

app.register_blueprint(solicitudes_blueprint)

@app.route('/health')
def health():
    return jsonify(status='ok'), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001, host='0.0.0.0')
