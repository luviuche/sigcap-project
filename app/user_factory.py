# app/user_factory.py
from .models import Cliente, Profesional

class UserFactory:
    @staticmethod
    def crear_usuario(tipo, data):
        email = data.get('email')
        password = data.get('password') # En un proyecto real, haríamos un hash aquí

        if not email or not password:
            raise ValueError("Email y password son requeridos")

        if tipo == 'cliente':
            return Cliente(email=email, password_hash=password)
        elif tipo == 'profesional':
            return Profesional(email=email, password_hash=password)
        else:
            raise ValueError(f"Tipo de usuario '{tipo}' no es válido.")