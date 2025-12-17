# src/core/sai_vision_service.py

import logging
import base64

from config.chat_config import ChatConfig
from core.interfaces.abstract_vision_service import AbstractVisionService
from core.base_sai_service import BaseSaiService # Importa a classe base
from core.exceptions import ConfigurationError # Importa a exceção

logger = logging.getLogger(__name__)

# Herda da classe base e da interface
class SaiVisionService(BaseSaiService, AbstractVisionService):
    def __init__(self):
        # __init__ simplificado
        super().__init__()
        self.vision_template_id = ChatConfig.SAI_VISION_TEMPLATE_ID
        if self.api_key:
            logger.info("SaiVisionService inicializado.")

    def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """
        Analisa uma imagem usando a API SAI de visão computacional.
        """
        if not self.vision_template_id:
            raise ConfigurationError("SAI_VISION_TEMPLATE_ID não configurado.")

        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        str_image_data_url = f"data:image/png;base64,{base64_image}"

        inputs_data = {
            "str_message": prompt,
            "str_image": str_image_data_url,
        }

        logger.info(f"Enviando requisição de análise de imagem para SAI...")

        # Chama o método da classe base
        outputs = self._execute_request(self.vision_template_id, inputs_data)

        if "str_output" in outputs:
            return outputs["str_output"]
        else:
            logger.warning(f"Resposta da API de visão não contém 'str_output'. Outputs: {outputs}")
            return "A API de visão retornou uma resposta sem o conteúdo esperado."