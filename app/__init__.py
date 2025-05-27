# app/__init__.py

from flask import Flask, request, jsonify
from .database import db
from .patterns.logger_singleton import Logger


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sigcap.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # --- Importamos los modelos aquí para que estén disponibles para todas las rutas ---
    from . import models
    from .models import Cita, CitaBuilder
    from .user_factory import UserFactory

    with app.app_context():
        db.create_all()

    logger = Logger()

    # --- INICIO DE LA DEFINICIÓN DE RUTAS ---

    @app.route('/')
    def hello_world():
        logger.log("Se ha accedido a la ruta principal /")
        return '¡El servidor SIGCAP está funcionando!'

    @app.route('/citas', methods=['POST'])
    def crear_cita():
        # ... (esta ruta no cambia)
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        try:
            logger.log(f"Recibida petición para crear cita para cliente ID: {data.get('cliente_id')}")
            nueva_cita = (CitaBuilder()
                          .con_profesional(data['profesional_id'])
                          .para_cliente(data['cliente_id'])
                          .build())
            db.session.add(nueva_cita)
            db.session.commit()
            logger.log(f"Cita ID: {nueva_cita.id} creada exitosamente.")
            return jsonify(nueva_cita.to_dict()), 201
        except (ValueError, KeyError) as e:
            logger.log(f"Error al crear cita: {e}")
            return jsonify({"error": str(e)}), 400

    @app.route('/usuarios/registrar', methods=['POST'])
    def registrar_usuario():
        # ... (esta ruta no cambia)
        data = request.get_json()
        if not data or 'tipo' not in data:
            return jsonify({"error": "Se requiere el tipo de usuario"}), 400
        try:
            logger.log(f"Recibida petición para registrar usuario tipo: {data.get('tipo')}")
            nuevo_usuario = UserFactory.crear_usuario(data['tipo'], data)
            db.session.add(nuevo_usuario)
            db.session.commit()
            logger.log(f"Usuario ID: {nuevo_usuario.id} ({nuevo_usuario.email}) creado exitosamente.")
            return jsonify(nuevo_usuario.to_dict()), 201
        except ValueError as e:
            logger.log(f"Error al registrar usuario: {e}")
            return jsonify({"error": str(e)}), 400

    # --- NUEVAS RUTAS PARA MANEJAR ESTADOS DE LA CITA ---

    @app.route('/citas/<int:cita_id>/confirmar', methods=['POST'])
    def confirmar_cita(cita_id):
        # 1. Busca la cita en la BD. get_or_404 devuelve error 404 si no la encuentra.
        cita = Cita.query.get_or_404(cita_id)

        # 2. Llama al método de acción (que delega al estado actual)
        cita.confirmar()

        # 3. Guarda los cambios en la BD
        db.session.commit()

        logger.log(f"Acción 'confirmar' ejecutada en Cita ID: {cita.id}. Nuevo estado: {cita.estado}")
        return jsonify(cita.to_dict())

    @app.route('/citas/<int:cita_id>/cancelar', methods=['POST'])
    def cancelar_cita(cita_id):
        cita = Cita.query.get_or_404(cita_id)
        cita.cancelar()
        db.session.commit()
        logger.log(f"Acción 'cancelar' ejecutada en Cita ID: {cita.id}. Nuevo estado: {cita.estado}")
        return jsonify(cita.to_dict())

    @app.route('/citas/<int:cita_id>/completar', methods=['POST'])
    def completar_cita(cita_id):
        cita = Cita.query.get_or_404(cita_id)
        cita.completar()
        db.session.commit()
        logger.log(f"Acción 'completar' ejecutada en Cita ID: {cita.id}. Nuevo estado: {cita.estado}")
        return jsonify(cita.to_dict())

    # --- FIN DE LA DEFINICIÓN DE RUTAS ---

    return app