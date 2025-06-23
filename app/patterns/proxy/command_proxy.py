# app/patterns/proxy/command_proxy.py
from app.patterns.command.commands import Command
from app.patterns.logger_singleton import Logger


class CommandProxy(Command):
    """
    Un proxy que añade logging y control de acceso (simulado)
    antes y después de ejecutar un comando real.
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
        Ejecuta la acción principal si el acceso es permitido.
        """
        if self._check_access():
            self._logger.log(f"Proxy: Registrando log ANTES de ejecutar {self._real_command.__class__.__name__}")

            # Delega la ejecución al objeto de comando real
            self._real_command.execute()

            self._logger.log(f"Proxy: Registrando log DESPUÉS de ejecutar {self._real_command.__class__.__name__}")

    # --- MÉTODO AÑADIDO ---
    def unexecute(self) -> None:
        """
        Ejecuta la acción de deshacer si el acceso es permitido.
        """
        if self._check_access():
            self._logger.log(f"Proxy: Registrando log ANTES de deshacer {self._real_command.__class__.__name__}")

            # Delega la acción de deshacer al objeto de comando real
            self._real_command.unexecute()

            self._logger.log(f"Proxy: Registrando log DESPUÉS de deshacer {self._real_command.__class__.__name__}")