# app/patterns/observer/events.py

from __future__ import annotations
from typing import List

# NOTA: En la versión final, hemos simplificado y quitado la dependencia de 'abc'
# para evitar conflictos de metaclases con SQLAlchemy, como descubrimos en el debugging.

class Subject:
    """
    El Sujeto (Observable). Mantiene una lista de observadores y los notifica
    de cualquier cambio de estado.
    """
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        """ Dispara una actualización en cada observador suscrito. """
        for observer in self._observers:
            observer.update(self)

class Observer:
    """
    La Interfaz del Observador. Define la interfaz para los objetos que deben
    ser notificados de las actualizaciones de un Sujeto.
    """
    def update(self, subject: Subject) -> None:
        """
        Recibe la actualización del sujeto. Las subclases deben implementar este método.
        """
        raise NotImplementedError()

# --- Observadores Concretos ---

class EmailNotifier(Observer):
    """
    Un observador concreto que reacciona al evento enviando un email (simulado).
    """
    def update(self, subject: Subject) -> None:
        # En un caso real, aquí se conectaría a un servicio de email.
        # 'Subject' es el objeto Cita que cambió de estado.
        print(f"-> EMAIL NOTIFIER: Enviando email por cambio en {subject.__class__.__name__} ID: {subject.id}. Nuevo estado: {subject.estado}")


class DashboardNotifier(Observer):
    """
    Un observador concreto que reacciona al evento actualizando un dashboard (simulado).
    """
    def update(self, subject: Subject) -> None:
        # En un caso real, esto enviaría una notificación push o una actualización vía WebSocket.
        print(f"-> DASHBOARD NOTIFIER: Actualizando dashboard por cambio en {subject.__class__.__name__} ID: {subject.id}.")