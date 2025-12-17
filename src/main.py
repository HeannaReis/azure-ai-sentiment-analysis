# src/main.py
from core.handlers.signal_handler import SignalHandler # Importa a classe SignalHandler
from services.image_processor import ImageProcessor
from core.rate_limiter import RateLimiter
import json
from config.config import Config
from core.logger_config import logger
from dotenv import load_dotenv

def main():
    load_dotenv() # Carrega as variáveis de ambiente do .env
    SignalHandler.setup() # Configura o manipulador de sinais

    try:
        Config.validate() # Valida as configurações da aplicação
        logger.info("✅ Configurações validadas com sucesso")
    except ValueError as e:
        logger.critical(f"❌ Erro de configuração: {e}")
        print(f"🚨 Erro de Configuração: {e}")
        return # Sai da aplicação se a configuração for inválida

    # Inicializa o RateLimiter para o loop de processamento geral
    processing_rate_limiter = RateLimiter(
        max_requests=Config.PROCESSING_RATE_LIMIT["max_requests"],
        period_seconds=Config.PROCESSING_RATE_LIMIT["period_seconds"]
    )

    processor = ImageProcessor(processing_rate_limiter)
    processor.process_images()

    # O histórico já é salvo internamente pelo ImageProcessor,
    # mas você pode recuperá-lo e imprimi-lo aqui se desejar.
    history = processor.get_history()
    if history:
        print("\n--- Histórico Final de Análises ---")
        for item in history:
            print(f"Imagem: {item['image_name']}, Resumo: {item['summary'][:100]}...") # Imprime os primeiros 100 caracteres do resumo
    else:
        print("\nNenhuma imagem foi processada ou nenhum histórico foi gerado.")

if __name__ == "__main__":
    main()