# src/services/image_processor.py
import os
import time
import shutil
import json
import base64 # Necessário para codificar a imagem
from io import BytesIO # Pode ser útil para manipulação de bytes, mas não estritamente necessário aqui

from config.config import Config # Importa a classe Config
from services.document_service import DocumentService
from services.markdown_service import MarkdownService
from utils.file_utils import list_images
from core.logger_config import logger
from core.rate_limiter import RateLimiter
from services.sai_documentation_service import SaiDocumentationService # Novo import
from core.exceptions import SAIApiError, ConfigurationError # Novos imports

class ImageProcessor:
    def __init__(self, rate_limiter: RateLimiter):
        # Remove o handler Gemini
        # self.gpt_handler = GenerativeModelHandler("gemini-2.5-flash")

        self.sai_documentation_service = SaiDocumentationService() # Inicializa o novo serviço SAI
        self.document_service = DocumentService()
        self.markdown_service = MarkdownService()
        os.makedirs(Config.PROCESSED_DIR, exist_ok=True) # Usa Config
        self.prompt = self._load_prompt()
        # self.history não é mais usado diretamente, o histórico é carregado em analises_anteriores
        self.rate_limiter = rate_limiter # Rate limiter para o loop de processamento geral
        self.historico_json_file = Config.HISTORY_FILE # Usa Config
        self.analises_anteriores = self._carregar_historico_json()

    def _load_prompt(self):
        try:
            with open(Config.PROMPT_DOC_FILE, "r", encoding="utf-8") as file: # Usa Config
                prompt = file.read().strip()
                logger.info(f"Prompt carregado com sucesso: {prompt}")
                return prompt
        except FileNotFoundError:
            logger.warning(f"Arquivo de prompt não encontrado em {Config.PROMPT_DOC_FILE}. Usando prompt vazio.")
            return "" # Retorna string vazia se o arquivo não for encontrado

    def _carregar_historico_json(self):
        try:
            if os.path.exists(self.historico_json_file):
                with open(self.historico_json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON do histórico em {self.historico_json_file}. Iniciando com histórico vazio.")
            return []

    def _salvar_historico_json(self):
        with open(self.historico_json_file, "w", encoding="utf-8") as f:
            json.dump(self.analises_anteriores, f, indent=4)

    def process_images(self):
        images = list_images(Config.ASSETS_DIR) # Usa Config
        if not images:
            logger.warning("Nenhuma imagem encontrada em 'assets/'.")
            return

        for idx, image_name in enumerate(images, start=1):
            logger.info(f"Processando imagem {idx}/{len(images)}: {image_name}")

            try:
                self.rate_limiter.wait_for_slot() # Rate limit para o loop de processamento geral
                summary = self._process_image(image_name)
                self.document_service.add_image_summary(image_name, summary)
                self.markdown_service.add_image_summary(image_name, summary)
                self.document_service.save_document()
                self.markdown_service.save_markdown()
                self._move_image(image_name)
                self._update_history(image_name, summary)
                self._salvar_historico_json() # Salva o histórico após cada imagem processada

            except (ConfigurationError, SAIApiError) as e:
                logger.error(f"Erro específico da API SAI ao processar a imagem {image_name}: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado ao processar a imagem {image_name}: {e}", exc_info=True)

            time.sleep(4) # Pequeno atraso entre as imagens
            logger.info("Preparando a próxima análise...")

    def _process_image(self, image_name):
        img_path = os.path.join(Config.ASSETS_DIR, image_name) # Usa Config
        processed_path = os.path.join(Config.PROCESSED_DIR, image_name) # Usa Config
        shutil.copy2(img_path, processed_path) # Copia para processed antes de enviar

        try:
            # Lê os bytes da imagem
            with open(img_path, "rb") as f:
                image_bytes = f.read()

            # Constrói o contexto de texto com o prompt e o histórico
            historico_str = "\n".join([f"Imagem anterior '{entry['image_name']}': {entry['summary']}" for entry in self.analises_anteriores])
            full_text_context = f"{self.prompt}\n\nHistórico de análises anteriores:\n{historico_str}\n\nAnalise a seguinte imagem para documentação de processo:"

            # Chama o novo serviço SAI para gerar a documentação
            response_text = self.sai_documentation_service.generate_documentation(image_bytes, full_text_context)
            logger.info(f"Documentação gerada para '{image_name}': {response_text}")
            return response_text
        except (ConfigurationError, SAIApiError) as e:
            logger.error(f"Erro ao chamar o serviço SAI para '{image_name}': {str(e)}")
            return f"Erro ao gerar documentação: {str(e)}"
        except Exception as e:
            logger.error(f"Erro inesperado ao preparar ou enviar imagem '{image_name}': {str(e)}", exc_info=True)
            return f"Erro inesperado: {str(e)}"

    def _move_image(self, image_name):
        origem = os.path.join(Config.ASSETS_DIR, image_name) # Usa Config
        # A imagem já foi copiada para processed_path em _process_image, então apenas remove de assets
        os.remove(origem)
        logger.info(f"Imagem '{image_name}' removida de '{Config.ASSETS_DIR}'.")

    def _update_history(self, image_name, summary):
        self.analises_anteriores.append({"image_name": image_name, "summary": summary}) # Atualiza o histórico
        logger.info(f"Histórico de análises anteriores atualizado com '{image_name}'.")

    def get_history(self):
        return self.analises_anteriores # Retorna o histórico completo