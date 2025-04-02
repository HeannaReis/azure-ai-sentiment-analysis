# main.py
from core.handlers.signal_handler import setup_signal_handler
from services.image_processor import ImageProcessor
from core.rate_limiter import RateLimiter
import json

def main():
    setup_signal_handler()

    # Inicializa o RateLimiter com o número máximo de requisições e o período
    rate_limiter = RateLimiter(max_requests=9, period_seconds=60)  # 9 requisições por minuto

    # Passa o RateLimiter para o ImageProcessor
    processor = ImageProcessor(rate_limiter)
    processor.process_images()

    # Obter e imprimir o histórico após o processamento
    history = processor.get_history()
    for item in history:
        print(f"Imagem: {item['image_name']}, Resumo: {item['summary']}")

    # Salvar o histórico em um arquivo JSON
    with open(processor.historico_json_file, "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    main()