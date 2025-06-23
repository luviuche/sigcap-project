# app/patterns/facade/booking_facade.py

from app.database import db
from app.models import CitaBuilder
from app.user_factory import UserFactory


class BookingFacade:
    """
    Implementa el patrón Facade.
    Proporciona una interfaz simple para el subsistema complejo de creación
    de usuarios y citas.
    """

    def realizar_reserva_completa(self, datos_usuario: dict, datos_cita: dict) -> dict:
        """
        Orquesta la creación de un usuario y una cita en una sola operación,
        ocultando la complejidad al cliente.
        """
        print("[DEBUG Facade] Iniciando proceso de reserva completa...")

        # 1. Usar el UserFactory para crear al cliente
        try:
            cliente = UserFactory.crear_usuario('cliente', datos_usuario)
            db.session.add(cliente)
            db.session.commit()  # Guardamos para obtener el ID del cliente
            print(f"[DEBUG Facade] Cliente ID: {cliente.id} creado/encontrado.")
        except ValueError as e:
            raise e  # Relanzamos la excepción para que sea manejada por la API

        # 2. Usar el CitaBuilder para crear la cita
        try:
            # Usamos el ID del cliente recién creado
            datos_cita['cliente_id'] = cliente.id

            nueva_cita = (CitaBuilder()
                          .con_profesional(datos_cita['profesional_id'])
                          .para_cliente(datos_cita['cliente_id'])
                          .build())
            db.session.add(nueva_cita)
            db.session.commit()  # Guardamos para obtener el ID de la cita
            print(f"[DEBUG Facade] Cita ID: {nueva_cita.id} creada para el cliente ID: {cliente.id}.")
        except (ValueError, KeyError) as e:
            # En una aplicación real, aquí se podría implementar una compensación
            # (ej. borrar el usuario recién creado si la creación de la cita falla).
            raise e

        print("[DEBUG Facade] Proceso de reserva completa finalizado.")

        # 3. Devolvemos un diccionario con los resultados de la operación completa
        return {
            'cliente': cliente.to_dict(),
            'cita': nueva_cita.to_dict()
        }