# app/__init__.py
from flask import Flask, request, jsonify, render_template

# --- Importaciones Centrales y de Patrones ---
from .database import db
from .patterns.logger_singleton import Logger

def create_app():
    """
    Función que implementa el patrón Application Factory.
    Crea, configura y devuelve la instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    # --- Configuración de la Aplicación ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sigcap.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False # Para que los JSON respeten el orden de los diccionarios

    # --- Inicialización de Extensiones ---
    db.init_app(app)

    # --- Importaciones de Componentes de la App ---
    # Se importan aquí para evitar importaciones circulares.
    from .models import Cita, CitaBuilder, Usuario, Cliente, Profesional
    from .user_factory import UserFactory
    from .patterns.command.commands import (
        ConfirmarCitaCommand,
        CancelarCitaCommand,
        CompletarCitaCommand,
        CommandInvoker
    )
    from .patterns.facade.booking_facade import BookingFacade
    from .patterns.decorator.billing import ImpuestoDecorator, TarifaUrgenciaDecorator
    from .patterns.adapter.billing_adapter import CitaBillingAdapter
    from .patterns.proxy.command_proxy import CommandProxy

    # --- Creación de la Base de Datos ---
    with app.app_context():
        # Crea todas las tablas definidas en models.py si no existen
        db.create_all()

    # --- Instancia Única de Nuestro Logger (Singleton) ---
    logger = Logger()

    # -------------------------------------------------------------------------
    # --- DEFINICIÓN DE RUTAS DE LA API ---
    # -------------------------------------------------------------------------

    @app.route('/')
    def hello_world():
        logger.log("Se ha accedido a la página principal (frontend).")
        # Esta función busca 'index.html' en la carpeta 'templates' y lo devuelve
        return render_template('index.html')

    # --- Rutas para Patrones Creacionales (Factory y Builder) ---

    @app.route('/usuarios/registrar', methods=['POST'])
    def registrar_usuario():
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

    @app.route('/citas', methods=['POST'])
    def crear_cita():
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

    # --- Rutas para Patrones de Comportamiento (State, Observer, Command, Proxy) ---

    @app.route('/citas/<int:cita_id>/confirmar', methods=['POST'])
    def confirmar_cita(cita_id):
        cita = Cita.query.get_or_404(cita_id)
        comando_real = ConfirmarCitaCommand(cita)
        proxy = CommandProxy(comando_real, user_role="admin") # Simulamos un usuario admin
        invoker = CommandInvoker()
        invoker.set_command(proxy)
        invoker.execute_command()
        db.session.commit()
        logger.log(f"Comando 'confirmar' (a través de Proxy) ejecutado en Cita ID: {cita.id}. Nuevo estado: {cita.estado}")
        return jsonify(cita.to_dict())

    # (Las rutas para cancelar y completar usarían la misma estructura de Command y Proxy)

    # --- Rutas para Patrones Estructurales (Facade, Adapter, Decorator) ---

    @app.route('/reservas-completas', methods=['POST'])
    def crear_reserva_completa():
        data = request.get_json()
        if not data or 'usuario' not in data or 'cita' not in data:
            return jsonify({"error": "Se requieren los datos de 'usuario' y 'cita'"}), 400
        try:
            fachada = BookingFacade()
            resultado = fachada.realizar_reserva_completa(data['usuario'], data['cita'])
            return jsonify(resultado), 201
        except (ValueError, KeyError) as e:
            logger.log(f"Error en el proceso de reserva completa: {e}")
            return jsonify({"error": str(e)}), 400

    @app.route('/citas/<int:cita_id>/costo-detallado', methods=['GET'])
    def obtener_costo_cita(cita_id):
        cita_db = Cita.query.get_or_404(cita_id)
        componente_facturacion = CitaBillingAdapter(cita_db)
        args = request.args
        if args.get('urgencia') == 'true':
            componente_facturacion = TarifaUrgenciaDecorator(componente_facturacion)
        if args.get('impuesto') == 'true':
            componente_facturacion = ImpuestoDecorator(componente_facturacion)
        costo_final = componente_facturacion.get_cost()
        descripcion_final = componente_facturacion.get_description()
        logger.log(f"Calculado costo para Cita ID: {cita_id}. Costo final: {costo_final}")
        return jsonify({
            'cita_id': cita_id,
            'costo_final': round(costo_final, 2),
            'descripcion': descripcion_final
        })

    return app