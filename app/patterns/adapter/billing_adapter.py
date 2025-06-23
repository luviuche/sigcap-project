# app/patterns/adapter/billing_adapter.py

from app.models import Cita
from app.patterns.decorator.billing import BillingComponent

class CitaBillingAdapter(BillingComponent):
    """
    Implementa el patrón Adapter.
    Adapta un objeto Cita, que tiene una interfaz incompatible, para que pueda
    funcionar con la interfaz que espera el sistema de facturación (BillingComponent).
    """
    def __init__(self, cita: Cita):
        self._cita = cita

    def get_cost(self) -> float:
        """
        Traduce la llamada a get_cost() para que devuelva el costo_base de la Cita.
        """
        return self._cita.costo_base

    def get_description(self) -> str:
        """
        Traduce la llamada a get_description() para que devuelva una descripción
        basada en los datos de la Cita.
        """
        return f"Cita ID {self._cita.id}"