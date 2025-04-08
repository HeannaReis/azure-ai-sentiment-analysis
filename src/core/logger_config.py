# core/logger_config.py
import logging
from datetime import datetime
from config.config import Config

class LoggerSetup:
    @staticmethod
    def setup_logger():
        """Configura e retorna um logger global para a aplicação."""
        Config.ensure_directories()
        
        log_filename = f"log_{datetime.now().strftime('%Y%m%d')}.log"
        log_filepath = Config.LOG_DIR / log_filename

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_filepath, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)

# Instância global do logger
logger = LoggerSetup.setup_logger()