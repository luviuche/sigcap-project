# app/patterns/logger_singleton.py
from datetime import datetime, timezone

class Logger:
    _instance = None

    # El método __new__ se llama antes de __init__ y controla la creación de la instancia
    def __new__(cls):
        if cls._instance is None:
            print("Creando instancia del Logger...")
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message):
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"[{timestamp}] - LOG: {message}"
        self.logs.append(log_entry)
        print(log_entry) # Imprimimos en la consola para verlo en tiempo real