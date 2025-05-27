# app/patterns/observer/events.py

# Ya no necesitamos ABC ni abstractmethod para este enfoque más simple.
from __future__ import annotations
from typing import List

# --- El Sujeto (Observable) - Ahora una clase normal ---
class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        # print(f"[DEBUG Subject.notify] Notificando a {len(self._observers)} observadores.") # Print para ver cuántos hay
        for observer in self._observers:
            # print(f"[DEBUG Subject.notify] Notificando a {observer.__class__.__name__}")
            observer.update(self)

# --- El Observador - Ahora una clase normal ---
class Observer:
    def update(self, subject: Subject) -> None:
        """
        Recibe la actualización del sujeto.
        Lanzamos un error si una subclase no implementa este método.
        """
        raise NotImplementedError()

# --- Observadores Concretos (no necesitan cambios) ---

class EmailNotifier(Observer):
    def update(self, subject: Subject) -> None:
        print(f"-> EMAIL NOTIFIER: Enviando email por cambio en {subject.__class__.__name__} ID: {subject.id}. Nuevo estado: {subject.estado}")


class DashboardNotifier(Observer):
    def update(self, subject: Subject) -> None:
        print(f"-> DASHBOARD NOTIFIER: Actualizando dashboard por cambio en {subject.__class__.__name__} ID: {subject.id}.")