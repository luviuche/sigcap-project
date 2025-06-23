# app/patterns/logger_singleton.py
from datetime import datetime, timezone

class Logger:
    """
    Implementa el patrón Singleton para asegurar una única instancia del logger
    en toda la aplicación.
    """
    _instance = None

    def __new__(cls):
        """
        Metodo de creación que controla la instanciación.
        Si la instancia no existe, la crea. Si ya existe, devuelve la existente.
        """
        if cls._instance is None:
            print("Creando instancia del Logger...")
            cls._instance = super(Logger, cls).__new__(cls)
            # Podríamos inicializar un archivo de log aquí si quisiéramos
        return cls._instance

    def log(self, message: str):
        """
        Registra un mensaje con timestamp en la consola.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"[{timestamp}] - LOG: {message}"
        print(log_entry)