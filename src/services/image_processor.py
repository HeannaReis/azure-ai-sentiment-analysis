# image_processor.py
import os
import time
import shutil
from core.config import ASSETS_DIR, PROCESSED_DIR, PROMPT_DOC_FILE
from core.handlers.gemini_handler import GeminiHandler
from services.document_service import DocumentService
from services.markdown_service import MarkdownService
from utils.file_utils import list_images
from core.logger_config import logger

class ImageProcessor:
    def __init__(self):
        self.gemini_handler = GeminiHandler("gemini-2.0-flash-exp")
        self.document_service = DocumentService()
        self.markdown_service = MarkdownService()
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        self.prompt = self._load_prompt()
        self.history = []  # Inicializa o histórico

    def _load_prompt(self):
        try:
            with open(PROMPT_DOC_FILE, "r", encoding="utf-8") as file:
                prompt = file.read().strip()
                logger.info(f"Prompt carregado com sucesso: {prompt}")
                return prompt
        except FileNotFoundError:
            logger.error(f"Arquivo de prompt não encontrado em {PROMPT_DOC_FILE}")
            raise FileNotFoundError(f"Arquivo de prompt não encontrado em {PROMPT_DOC_FILE}")

    def process_images(self):
        images = list_images(ASSETS_DIR)
        if not images:
            logger.warning("Nenhuma imagem encontrada em 'assets/'.")
            return

        for idx, image_name in enumerate(images, start=1):
            logger.info(f"Processando imagem {idx}/{len(images)}: {image_name}")
            summary = self._process_image(image_name)
            self.document_service.add_image_summary(image_name, summary)
            self.markdown_service.add_image_summary(image_name, summary)
            self.document_service.save_document()
            self.markdown_service.save_markdown()
            self._move_image(image_name)
            self._update_history(image_name, summary)  # Atualiza o histórico
            if idx < len(images):
                logger.info("Aguardando 7 segundos para próxima requisição...")
                time.sleep(7)

    def _process_image(self, image_name):
        img_path = os.path.join(ASSETS_DIR, image_name)
        # Primeiro, copia a imagem para o diretório de processados
        processed_path = os.path.join(PROCESSED_DIR, image_name)
        shutil.copy2(img_path, processed_path)
        
        try:
            response_text = self.gemini_handler.generate_content(img_path, self.prompt)
            logger.info(f"Resumo gerado para '{image_name}': {response_text}")
            return response_text
        except Exception as e:
            logger.error(f"Erro ao processar '{image_name}': {str(e)}")
            return f"Erro ao processar imagem: {str(e)}"

    def _move_image(self, image_name):
        origem = os.path.join(ASSETS_DIR, image_name)
        destino = os.path.join(PROCESSED_DIR, image_name)
        shutil.move(origem, destino)
        logger.info(f"Imagem '{image_name}' movida para '{PROCESSED_DIR}'.")

    def _update_history(self, image_name, summary):
        """Atualiza o histórico com a imagem e seu resumo."""
        self.history.append({"image_name": image_name, "summary": summary})
        logger.info(f"Histórico atualizado com '{image_name}'.")

    def get_history(self):
        """Retorna o histórico de processamento."""
        return self.history