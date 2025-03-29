from core.handlers.signal_handler import setup_signal_handler
from services.image_processor import ImageProcessor
import json

def main():
    setup_signal_handler()
    processor = ImageProcessor()
    processor.process_images()

    # Obter e imprimir o histórico após o processamento
    history = processor.get_history()
    for item in history:
        print(f"Imagem: {item['image_name']}, Resumo: {item['summary']}")

    # Salvar o histórico em um arquivo JSON
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    main()