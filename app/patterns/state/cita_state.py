# app/patterns/state/cita_state.py
from __future__ import annotations
from abc import ABC, abstractmethod

class CitaState(ABC):
    """
    La Interfaz de Estado. Define los métodos que todos los estados concretos
    deben implementar y que el Contexto (Cita) puede llamar.
    """
    @abstractmethod
    def confirmar(self, cita: 'Cita'):
        pass

    @abstractmethod
    def cancelar(self, cita: 'Cita'):
        pass

    @abstractmethod
    def completar(self, cita: 'Cita'):
        pass

# --- Estados Concretos ---

class EstadoSolicitada(CitaState):
    """ Implementa el comportamiento para cuando una cita está solicitada. """
    def confirmar(self, cita: 'Cita'):
        print("Cita confirmada.")
        cita.transicionar_a(EstadoConfirmada())

    def cancelar(self, cita: 'Cita'):
        print("Cita solicitada cancelada.")
        cita.transicionar_a(EstadoCancelada())

    def completar(self, cita: 'Cita'):
        print("No se puede completar una cita que solo ha sido solicitada.")


class EstadoConfirmada(CitaState):
    """ Implementa el comportamiento para cuando una cita está confirmada. """
    def confirmar(self, cita: 'Cita'):
        print("La cita ya ha sido confirmada.")

    def cancelar(self, cita: 'Cita'):
        print("Cita confirmada ha sido cancelada.")
        cita.transicionar_a(EstadoCancelada())

    def completar(self, cita: 'Cita'):
        print("Cita completada exitosamente.")
        cita.transicionar_a(EstadoCompletada())


class EstadoCancelada(CitaState):
    """ Implementa el comportamiento para cuando una cita está cancelada. """
    def confirmar(self, cita: 'Cita'):
        print("No se puede confirmar una cita cancelada.")

    def cancelar(self, cita: 'Cita'):
        print("La cita ya está cancelada.")

    def completar(self, cita: 'Cita'):
        print("No se puede completar una cita cancelada.")


class EstadoCompletada(CitaState):
    """ Implementa el comportamiento para cuando una cita está completada. """
    def confirmar(self, cita: 'Cita'):
        print("No se puede confirmar una cita ya completada.")

    def cancelar(self, cita: 'Cita'):
        print("No se puede cancelar una cita ya completada.")

    def completar(self, cita: 'Cita'):
        print("La cita ya ha sido completada.")