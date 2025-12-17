# src/services/sai_image_generator.py

import logging
import base64
import io
from PIL import Image

from config.chat_config import ChatConfig
from core.base_sai_service import BaseSaiService
from core.exceptions import ConfigurationError, SAIApiError

logger = logging.getLogger(__name__)

class SaiImageGenerator(BaseSaiService):
    def __init__(self):
        super().__init__()
        self.template_id = ChatConfig.SAI_IMAGE_GENERATION_TEMPLATE_ID
        if self.api_key:
            logger.info("SaiImageGenerator inicializado.")

    def generate_image(self, prompt: str) -> Image.Image | None:
        """
        Gera uma imagem usando a API SAI com o prompt fornecido.
        Retorna um objeto PIL Image.
        """
        if not self.template_id:
            raise ConfigurationError("SAI_IMAGE_GENERATION_TEMPLATE_ID não configurado.")

        inputs_data = {"str_image": prompt}

        try:
            logger.info(f"Enviando requisição de geração de imagem para SAI...")
            outputs = self._execute_request(self.template_id, inputs_data, timeout=500)

            image_data_url = None
            # Tenta primeiro 'image_output', depois 'str_output'
            if "image_output" in outputs:
                image_data_url = outputs["image_output"]
            elif "str_output" in outputs:
                image_data_url = outputs["str_output"]

            if not image_data_url:
                logger.error(f"Resposta da API não contém 'image_output' nem 'str_output' com dados de imagem. Outputs: {outputs}")
                return None

            # Remove o prefixo "data:image/png;base64," se presente
            if "," in image_data_url:
                base64_data = image_data_url.split(",")[1]
            else:
                base64_data = image_data_url # Assume que é apenas o base64 puro

            image_bytes = base64.b64decode(base64_data)
            logger.info("Imagem gerada pela API SAI e decodificada com sucesso.")
            return Image.open(io.BytesIO(image_bytes))

        except (ConfigurationError, SAIApiError) as e:
            logger.error(f"Falha ao gerar imagem: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao decodificar ou abrir a imagem: {e}", exc_info=True)
            return None
