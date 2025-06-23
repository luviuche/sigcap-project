# app/patterns/command/commands.py
from __future__ import annotations
from abc import ABC, abstractmethod

# CAMBIO 1: Importamos la clase Cita para poder buscarla en la BD
from app.models import Cita


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def unexecute(self) -> None:
        pass


# --- Comandos Concretos con la Lógica de Deshacer Corregida ---

class ConfirmarCitaCommand(Command):
    def __init__(self, cita: 'Cita'):
        self._cita_id = cita.id  # Guardamos solo el ID, no el objeto entero
        self._estado_anterior = None

    def execute(self) -> None:
        cita_actual = Cita.query.get(self._cita_id)
        if not cita_actual: return

        print(f"[DEBUG Command] Ejecutando ConfirmarCitaCommand para Cita ID: {cita_actual.id}")
        self._estado_anterior = cita_actual.estado  # Guardamos el estado actual
        cita_actual.confirmar()

    def unexecute(self) -> None:
        if self._estado_anterior:
            # 1. Volvemos a cargar la cita desde la BD en la sesión actual
            cita_actual = Cita.query.get(self._cita_id)
            if not cita_actual: return

            print(
                f"[DEBUG Command] Deshaciendo ConfirmarCitaCommand para Cita ID: {cita_actual.id}. Restaurando a estado: {self._estado_anterior}")
            # 2. Obtenemos el objeto de estado anterior
            estado_obj_anterior = cita_actual._ESTADO_MAP.get(self._estado_anterior)
            # 3. Hacemos la transición sobre el objeto 'fresco'
            if estado_obj_anterior:
                # Pasamos notify=False para que el deshacer no genere nuevas notificaciones
                cita_actual.transicionar_a(estado_obj_anterior, notify=False)


# --- (Aplica la misma lógica para los otros comandos) ---

class CancelarCitaCommand(Command):
    def __init__(self, cita: 'Cita'):
        self._cita_id = cita.id
        self._estado_anterior = None

    def execute(self) -> None:
        cita_actual = Cita.query.get(self._cita_id)
        if not cita_actual: return

        self._estado_anterior = cita_actual.estado
        cita_actual.cancelar()

    def unexecute(self) -> None:
        if self._estado_anterior:
            cita_actual = Cita.query.get(self._cita_id)
            if not cita_actual: return

            estado_obj_anterior = cita_actual._ESTADO_MAP.get(self._estado_anterior)
            if estado_obj_anterior:
                cita_actual.transicionar_a(estado_obj_anterior, notify=False)


class CompletarCitaCommand(Command):
    def __init__(self, cita: 'Cita'):
        self._cita_id = cita.id
        self._estado_anterior = None

    def execute(self) -> None:
        cita_actual = Cita.query.get(self._cita_id)
        if not cita_actual: return

        self._estado_anterior = cita_actual.estado
        cita_actual.completar()

    def unexecute(self) -> None:
        if self._estado_anterior:
            cita_actual = Cita.query.get(self._cita_id)
            if not cita_actual: return

            estado_obj_anterior = cita_actual._ESTADO_MAP.get(self._estado_anterior)
            if estado_obj_anterior:
                cita_actual.transicionar_a(estado_obj_anterior, notify=False)


# --- Invocador Actualizado con Historial ---
class CommandInvoker:
    """
    El Invocador, ahora con la capacidad de mantener un historial
    y deshacer el último comando ejecutado.
    """
    def __init__(self):
        # El comando actual a ejecutar se mantiene igual
        self._command: Command = None
        # NUEVO: Una lista para guardar el historial de comandos ejecutados
        self._history: list[Command] = []

    def set_command(self, command: Command):
        self._command = command

    def execute_command(self):
        if self._command:
            self._command.execute()
            # NUEVO: Después de ejecutar, guardamos el comando en el historial
            self._history.append(self._command)

    def undo_command(self):
        """
        NUEVO: Método para deshacer el último comando.
        """
        if self._history:
            # Sacamos el último comando de la pila del historial
            last_command = self._history.pop()
            print(f"[DEBUG CommandInvoker] Deshaciendo el último comando: {last_command.__class__.__name__}")
            # Y llamamos a su método para deshacer
            last_command.unexecute()
        else:
            print("[DEBUG CommandInvoker] No hay comandos en el historial para deshacer.")
