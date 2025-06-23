# app/models.py
from typing import ClassVar, List
from sqlalchemy import orm
from datetime import datetime, timezone

from .database import db
from .patterns.state.cita_state import (
    CitaState,
    EstadoSolicitada,
    EstadoConfirmada,
    EstadoCancelada,
    EstadoCompletada
)
from .patterns.observer.events import Subject, Observer, EmailNotifier, DashboardNotifier


# -----------------------------------------------------------------------------
# 1. MODELO DE DATOS: Cita (Integrando State y Observer)
# -----------------------------------------------------------------------------
class Cita(db.Model, Subject):
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    estado = db.Column(db.String(50), nullable=False, default='EstadoSolicitada')
    profesional_id = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    costo_base = db.Column(db.Float, nullable=False, default=50.0)

    # Atributo transitorio para el patrón State, marcado para que SQLAlchemy lo ignore.
    _estado_obj: ClassVar[CitaState] = None

    # Mapa de traducción para el patrón State
    _ESTADO_MAP = {
        'EstadoSolicitada': EstadoSolicitada(),
        'EstadoConfirmada': EstadoConfirmada(),
        'EstadoCancelada': EstadoCancelada(),
        'EstadoCompletada': EstadoCompletada(),
    }

    @orm.reconstructor
    def init_on_load(self):
        """
        Este método es llamado por SQLAlchemy cada vez que una instancia es creada
        o cargada desde la BD. Es el lugar perfecto para inicializar nuestros patrones.
        """
        # 1. Inicializa la parte 'Subject' del patrón Observer
        Subject.__init__(self)
        self.attach(EmailNotifier())
        self.attach(DashboardNotifier())

        # 2. Inicializa la parte 'State' del patrón State
        # Asigna el objeto de estado correcto basándose en el string guardado en la BD.
        self._estado_obj = self._ESTADO_MAP.get(self.estado, EstadoSolicitada())

    def transicionar_a(self, nuevo_estado: CitaState, notify: bool = True):
        """Método central para cambiar el estado y notificar a los observadores."""
        self._estado_obj = nuevo_estado
        self.estado = nuevo_estado.__class__.__name__

        if notify:
            self.notify()

    # --- Métodos de acción que delegan al objeto de estado ---
    def confirmar(self):
        self._estado_obj.confirmar(self)

    def cancelar(self):
        self._estado_obj.cancelar(self)

    def completar(self):
        self._estado_obj.completar(self)

    def to_dict(self):
        """Convierte el objeto en un diccionario para las respuestas API."""
        return {
            'id': self.id,
            'fecha_hora': self.fecha_hora.isoformat(),
            'estado': self.estado,
            'profesional_id': self.profesional_id,
            'cliente_id': self.cliente_id,
            'costo_base': self.costo_base
        }


# -----------------------------------------------------------------------------
# 2. PATRÓN BUILDER: CitaBuilder
# -----------------------------------------------------------------------------
class CitaBuilder:
    def __init__(self):
        self._data = {}

    def con_profesional(self, profesional_id):
        self._data['profesional_id'] = profesional_id
        return self

    def para_cliente(self, cliente_id):
        self._data['cliente_id'] = cliente_id
        return self

    def con_estado_inicial(self, estado):
        self._data['estado'] = estado
        return self

    def build(self):
        if 'profesional_id' not in self._data or 'cliente_id' not in self._data:
            raise ValueError("Se requiere un profesional y un cliente para crear la cita.")

        # Crea la instancia de Cita. SQLAlchemy se encarga de la asignación de atributos.
        # El decorador @orm.reconstructor (init_on_load) se llamará automáticamente después.
        return Cita(**self._data)


# -----------------------------------------------------------------------------
# 3. MODELOS DE USUARIO (Para el Factory Method)
# -----------------------------------------------------------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    tipo_usuario = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo_usuario
    }

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario
        }


class Cliente(Usuario):
    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }


class Profesional(Usuario):
    __mapper_args__ = {
        'polymorphic_identity': 'profesional',
    }