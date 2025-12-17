# src/core/handlers/signal_handler.py
import signal
import sys
from core.logger_config import logger

class SignalHandler:
    """Gerencia sinais do sistema operacional para interrupção controlada."""

    @staticmethod
    def handler(signum, frame):
        """
        Manipulador de sinal para interrupção controlada.

        Args:
            signum: Número do sinal
            frame: Frame atual
        """
        logger.warning("🚨 Processamento interrompido pelo usuário.")
        sys.exit(1)

    @staticmethod
    def setup():
        """Configura o manipulador de sinais para SIGINT (Ctrl+C)."""
        signal.signal(signal.SIGINT, SignalHandler.handler)