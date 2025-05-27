# app/patterns/state/cita_state.py

from __future__ import annotations
from abc import ABC, abstractmethod

class CitaState(ABC):
    # Usamos 'Cita' entre comillas para evitar la importación circular
    @abstractmethod
    def solicitar(self, cita: 'Cita'):
        pass

    @abstractmethod
    def confirmar(self, cita: 'Cita'):
        pass

    @abstractmethod
    def cancelar(self, cita: 'Cita'):
        pass

    @abstractmethod
    def completar(self, cita: 'Cita'):
        pass


# --- Estados Concretos (ligeramente modificados para usar la referencia adelantada) ---

class EstadoSolicitada(CitaState):
    def solicitar(self, cita: 'Cita'):
        print("La cita ya ha sido solicitada.")

    def confirmar(self, cita: 'Cita'):
        # print("[DEBUG EstadoSolicitada.confirmar] Entrando a confirmar...")  # Print para ver si se llama
        print("Cita confirmada.")  # Este es el print original que buscamos
        cita.transicionar_a(EstadoConfirmada())

    def cancelar(self, cita: 'Cita'):
        print("Cita solicitada cancelada.")
        cita.transicionar_a(EstadoCancelada())

    def completar(self, cita: 'Cita'):
        print("No se puede completar una cita que solo ha sido solicitada.")


class EstadoConfirmada(CitaState):
    def solicitar(self, cita: 'Cita'):
        print("No se puede solicitar una cita ya confirmada.")

    def confirmar(self, cita: 'Cita'):
        print("La cita ya ha sido confirmada.")

    def cancelar(self, cita: 'Cita'):
        print("Cita confirmada ha sido cancelada.")
        cita.transicionar_a(EstadoCancelada())

    def completar(self, cita: 'Cita'):
        print("Cita completada exitosamente.")
        cita.transicionar_a(EstadoCompletada())


class EstadoCancelada(CitaState):
    def solicitar(self, cita: 'Cita'):
        print("No se puede solicitar una cita cancelada.")

    def confirmar(self, cita: 'Cita'):
        print("No se puede confirmar una cita cancelada.")

    def cancelar(self, cita: 'Cita'):
        print("La cita ya está cancelada.")

    def completar(self, cita: 'Cita'):
        print("No se puede completar una cita cancelada.")


class EstadoCompletada(CitaState):
    def solicitar(self, cita: 'Cita'):
        print("No se puede solicitar una cita ya completada.")

    def confirmar(self, cita: 'Cita'):
        print("No se puede confirmar una cita ya completada.")

    def cancelar(self, cita: 'Cita'):
        print("No se puede cancelar una cita ya completada.")

    def completar(self, cita: 'Cita'):
        print("La cita ya ha sido completada.")