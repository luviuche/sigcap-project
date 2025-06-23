# app/patterns/command/commands.py
from __future__ import annotations
from abc import ABC, abstractmethod

# Para evitar una importación circular con models.py, usamos una referencia adelantada.
# El archivo models.py importará este archivo, así que no podemos importarlo aquí directamente.
# La pista de tipo 'Cita' funcionará gracias a "from __future__ import annotations".
# From app.models import Cita <-- NO HACER ESTA IMPORTACIÓN AQUÍ

class Command(ABC):
    """
    La Interfaz del Comando. Declara un método para ejecutar una operación.
    """
    @abstractmethod
    def execute(self) -> None:
        pass

# --- Comandos Concretos ---

class ConfirmarCitaCommand(Command):
    """
    Encapsula la acción de confirmar una Cita. Contiene una referencia
    a la Cita (el Receptor) sobre la cual actuará.
    """
    def __init__(self, cita: 'Cita'):
        self._cita = cita

    def execute(self) -> None:
        print(f"[DEBUG Command] Ejecutando ConfirmarCitaCommand para Cita ID: {self._cita.id}")
        self._cita.confirmar()


class CancelarCitaCommand(Command):
    """ Encapsula la acción de cancelar una Cita. """
    def __init__(self, cita: 'Cita'):
        self._cita = cita

    def execute(self) -> None:
        print(f"[DEBUG Command] Ejecutando CancelarCitaCommand para Cita ID: {self._cita.id}")
        self._cita.cancelar()


class CompletarCitaCommand(Command):
    """ Encapsula la acción de completar una Cita. """
    def __init__(self, cita: 'Cita'):
        self._cita = cita

    def execute(self) -> None:
        print(f"[DEBUG Command] Ejecutando CompletarCitaCommand para Cita ID: {self._cita.id}")
        self._cita.completar()


class CommandInvoker:
    """
    El Invocador. No sabe nada sobre la operación concreta. Solo toma un comando
    y lo ejecuta. Podría extenderse para soportar colas, historial, etc.
    """
    def __init__(self):
        self._command: Command = None

    def set_command(self, command: Command):
        self._command = command

    def execute_command(self):
        if self._command:
            self._command.execute()
        else:
            print("[DEBUG CommandInvoker] No hay comando para ejecutar.")