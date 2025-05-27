# app/models.py

# CAMBIO 1: Importamos 'timezone' del módulo datetime
from typing import ClassVar, List
from sqlalchemy import orm
from .patterns.state.cita_state import (
    CitaState,
    EstadoSolicitada,
    EstadoConfirmada,
    EstadoCancelada,
    EstadoCompletada
)
from .patterns.observer.events import Subject, EmailNotifier, DashboardNotifier, Observer
from .database import db
from datetime import datetime, timezone


# -----------------------------------------------------------------------------
# 1. EL MODELO DE DATOS: La clase Cita
# -----------------------------------------------------------------------------
class Cita(db.Model, Subject):  # Sigue heredando de ambos
    # Las columnas se definen como antes
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    estado = db.Column(db.String(50), nullable=False, default='EstadoSolicitada')
    profesional_id = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)

    _estado_obj: ClassVar[CitaState] = None
    _ESTADO_MAP = {
        'EstadoSolicitada': EstadoSolicitada(),
        'EstadoConfirmada': EstadoConfirmada(),
        'EstadoCancelada': EstadoCancelada(),
        'EstadoCompletada': EstadoCompletada(),
    }

    # No definimos un __init__ explícito para Cita.
    # Dejamos que SQLAlchemy maneje la creación inicial de atributos a partir de kwargs.
    # El @orm. Reconstructor se encargará de la lógica post-creación/carga.

    @orm.reconstructor
    def init_on_load(self):
        # Inicializamos el Subject para crear la lista _observers
        Subject.__init__(self)

        # Adjuntamos observadores
        self.attach(EmailNotifier())
        self.attach(DashboardNotifier())

        # Establecemos el objeto de estado correcto basado en el string 'estado'
        # Es importante no notificar aquí porque es una carga, no un cambio de estado.
        current_state_class = self._ESTADO_MAP.get(self.estado, EstadoSolicitada())
        self._estado_obj = current_state_class  # Asignamos directamente el objeto de estado

        # Si es una instancia completamente nueva y el estado es el default de la columna,
        # y _estado_obj no se asignó bien (poco probable con el get y default),
        # podrías forzarlo. Pero el get con default debería bastar.
        # Self. Estado ya tiene 'EstadoSolicitada' por el default de la columna
        # o el valor que venga de la BD.

    # El método transicionar_a y los métodos de acción (confirmar, etc.) se mantienen igual
    def transicionar_a(self, nuevo_estado: CitaState, notify: bool = True):
        # print(
        #    f"[DEBUG Cita transicionar_a ID:{getattr(self, 'id', 'N/A')}] Transicionando a {nuevo_estado.__class__.__name__}. Notificar: {notify}")
        self._estado_obj = nuevo_estado
        self.estado = nuevo_estado.__class__.__name__

        if notify:
            # Asegurarse de que _observers existe antes de notificar
            if not hasattr(self, '_observers'):
                Subject.__init__(self)  # Llama al init de Subject si _observers no existe

            # print(
            #    f"[DEBUG Cita transicionar_a ID:{getattr(self, 'id', 'N/A')}] Llamando a self.notify(). _observers: {getattr(self, '_observers', [])}")
            self.notify()

    def solicitar(self):
        # ... (se mantiene igual)
        self._estado_obj.solicitar(self)

    def confirmar(self):
        # print(
        #    f"[DEBUG Cita confirmar ID:{getattr(self, 'id', 'N/A')}] Llamando a _estado_obj.confirmar(). Estado actual obj: {type(self._estado_obj)}")
        self._estado_obj.confirmar(self)

    def cancelar(self):
        # ... (se mantiene igual)
        self._estado_obj.cancelar(self)

    def completar(self):
        # ... (se mantiene igual)
        self._estado_obj.completar(self)

    def to_dict(self):
        # ... (se mantiene igual)
        return {
            'id': self.id,
            'fecha_hora': self.fecha_hora.isoformat(),
            'estado': self.estado,
            'profesional_id': self.profesional_id,
            'cliente_id': self.cliente_id
        }


# El CitaBuilder también necesita un pequeño ajuste para que funcione sin el __init__ explícito
class CitaBuilder:
    def __init__(self):
        self._data = {}

    def con_profesional(self, profesional_id):
        self._data['profesional_id'] = profesional_id
        return self

    def para_cliente(self, cliente_id):
        self._data['cliente_id'] = cliente_id
        return self

    def en_fecha_hora(self, fecha_hora):
        self._data['fecha_hora'] = fecha_hora
        return self

    def con_estado_inicial(self, estado):
        # SQLAlchemy asignará el default 'EstadoSolicitada' si no se provee.
        # Si se provee, lo usará.
        self._data['estado'] = estado
        return self

    def build(self):
        if 'profesional_id' not in self._data or 'cliente_id' not in self._data:
            raise ValueError("Se requiere un profesional y un cliente para crear la cita.")
        # Creamos la instancia de Cita pasando los datos.
        # SQLAlchemy se encargará de la asignación a las columnas.
        return Cita(**self._data)

# -----------------------------------------------------------------------------
# 3. MODELOS DE USUARIO
# -----------------------------------------------------------------------------

# Clase base para todos los usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # En un proyecto real, aquí guardaríamos el hash de la contraseña
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
    # Podríamos añadir campos específicos del cliente aquí

class Profesional(Usuario):
    __mapper_args__ = {
        'polymorphic_identity': 'profesional',
    }
    # Podríamos añadir campos específicos del profesional aquí