# app/patterns/proxy/command_proxy.py
from app.patterns.command.commands import Command
from app.patterns.logger_singleton import Logger

class CommandProxy(Command):
    """
    Implementa el patrón Proxy.
    Actúa como un sustituto de un objeto 'Command' real, permitiendo añadir
    lógica de control (logging, control de acceso) antes y después de la ejecución
    del comando real.
    """
    def __init__(self, real_command: Command, user_role: str):
        self._real_command = real_command
        self._user_role = user_role
        self._logger = Logger()

    def _check_access(self) -> bool:
        """
        Método privado que simula una comprobación de permisos.
        """
        print(f"[DEBUG Proxy] Verificando acceso para rol: {self._user_role}...")
        if self._user_role == "admin":
            print("[DEBUG Proxy] Acceso concedido.")
            return True
        print("[DEBUG Proxy] Acceso denegado.")
        return False

    def execute(self) -> None:
        """
        El método de ejecución del proxy. Controla el acceso y delega
        la llamada al objeto de comando real.
        """
        if self._check_access():
            self._logger.log(f"Proxy: Registrando log ANTES de ejecutar {self._real_command.__class__.__name__}")

            # Delegamos la ejecución al objeto de comando real
            self._real_command.execute()

            self._logger.log(f"Proxy: Registrando log DESPUÉS de ejecutar {self._real_command.__class__.__name__}")