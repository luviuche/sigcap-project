# app/user_factory.py
from .models import Cliente, Profesional

class UserFactory:
    """
    Implementa el patrón Factory Method para crear diferentes tipos de usuarios.
    Desacopla al cliente de las clases de usuario concretas.
    """
    @staticmethod
    def crear_usuario(tipo: str, data: dict):
        """
        Crea una instancia de un subtipo de Usuario basándose en el 'tipo'.
        :param tipo: El tipo de usuario a crear ('cliente' o 'profesional').
        :param data: Un diccionario con los datos del usuario (ej. email, password).
        :return: Una instancia de Cliente or Profesional.
        :raises ValueError: Si el tipo de usuario no es válido o faltan datos.
        """
        email = data.get('email')
        password = data.get('password') # En un proyecto real, aquí se haría un hash

        if not email or not password:
            raise ValueError("Email y password son requeridos")

        if tipo == 'cliente':
            return Cliente(email=email, password_hash=password)
        elif tipo == 'profesional':
            return Profesional(email=email, password_hash=password)
        else:
            raise ValueError(f"Tipo de usuario '{tipo}' no es válido.")