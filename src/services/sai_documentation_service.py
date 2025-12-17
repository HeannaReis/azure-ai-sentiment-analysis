# src/services/sai_documentation_service.py
import logging
import base64
from typing import Optional

from config.config import Config
from core.base_sai_service import BaseSaiService
from core.exceptions import ConfigurationError, SAIApiError

logger = logging.getLogger(__name__)

class SaiDocumentationService(BaseSaiService):
    def __init__(self):
        super().__init__()
        self.template_id = Config.SAI_DOCUMENTATION_TEMPLATE_ID
        if self.api_key:
            logger.info("SaiDocumentationService inicializado.")

    def generate_documentation(self, image_bytes: bytes, text_context: Optional[str] = None) -> str:
        """
        Gera documentação para uma imagem usando a API SAI.
        image_bytes: Bytes da imagem a ser analisada.
        text_context: Texto adicional (prompt, histórico, etc.) para contextualizar a análise.
        """
        if not self.template_id:
            raise ConfigurationError("SAI_DOCUMENTATION_TEMPLATE_ID não configurado.")

        # Codifica a imagem para base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        # O template espera "str_image" como uma data URL
        str_image_data_url = f"data:image/png;base64,{base64_image}"

        inputs_data = {
            "str_image": str_image_data_url,
            "str_text": text_context if text_context else "" # Garante que str_text seja sempre enviado, mesmo que vazio
        }

        logger.info(f"Enviando requisição de documentação para SAI...")

        try:
            outputs = self._execute_request(self.template_id, inputs_data)

            if "str_output" in outputs:
                return outputs["str_output"]
            else:
                logger.warning(f"Resposta da API de documentação não contém 'str_output'. Outputs: {outputs}")
                return "A API de documentação retornou uma resposta sem o conteúdo esperado."
        except (ConfigurationError, SAIApiError) as e:
            logger.error(f"Falha ao gerar documentação: {e}")
            raise # Re-lança a exceção específica
        except Exception as e:
            logger.error(f"Erro inesperado ao gerar documentação: {e}", exc_info=True)
            raise SAIApiError(f"Erro inesperado na geração de documentação: {str(e)}") from e