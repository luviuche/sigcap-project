# app/patterns/decorator/billing.py
from abc import ABC, abstractmethod

# --- La Interfaz del Componente ---
# Define la interfaz común tanto para el objeto que envolvemos como para los decoradores.
class BillingComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# --- La Base del Decorador ---
# También implementa la interfaz y mantiene una referencia al objeto envuelto.
class BillingDecorator(BillingComponent):
    _component: BillingComponent = None

    def __init__(self, component: BillingComponent) -> None:
        self._component = component

    @property
    def component(self) -> BillingComponent:
        return self._component

    # El decorador base simplemente delega el trabajo al componente envuelto.
    # Las subclases extenderán este comportamiento.
    def get_cost(self) -> float:
        return self._component.get_cost()

    def get_description(self) -> str:
        return self._component.get_description()

# --- Decoradores Concretos ---
# Añaden su propia funcionalidad antes o después de delegar al componente.

class ImpuestoDecorator(BillingDecorator):
    """Añade un impuesto (ej. 19%) al costo total."""
    def get_cost(self) -> float:
        costo_base = super().get_cost()
        costo_impuesto = costo_base * 0.19
        return costo_base + costo_impuesto

    def get_description(self) -> str:
        return f"{super().get_description()}, con Impuesto (19%)"


class TarifaUrgenciaDecorator(BillingDecorator):
    """Añade una tarifa extra por servicio de urgencia."""
    def get_cost(self) -> float:
        return super().get_cost() + 25.0  # Tarifa de urgencia de 25.0

    def get_description(self) -> str:
        return f"{super().get_description()}, con Tarifa de Urgencia"