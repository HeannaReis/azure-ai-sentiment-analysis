# src/core/sai_llm_service.py

import logging
from typing import Optional

from config.chat_config import ChatConfig
from core.interfaces.abstract_chat_service import AbstractChatService
from core.base_sai_service import BaseSaiService # Importa a classe base
from core.exceptions import ConfigurationError # Importa a exceção

logger = logging.getLogger(__name__)

# Herda da classe base e da interface
class SaiLLMService(BaseSaiService, AbstractChatService):
    def __init__(self):
        # O __init__ é drasticamente simplificado
        super().__init__() # Chama o construtor da classe base
        self.llm_template_id = ChatConfig.SAI_LLM_TEMPLATE_ID
        if self.api_key:
            logger.info("SaiLLMService inicializado.")

    def generate_content(self, user_prompt: str, system_context: Optional[str] = None) -> str:
        """
        Gera conteúdo textual usando a API SAI LLM.
        A lógica de requisição foi movida para a classe base.
        """
        if not self.llm_template_id:
            raise ConfigurationError("SAI_LLM_TEMPLATE_ID não configurado.")

        inputs_data = {"str_texto": user_prompt}
        if system_context:
            inputs_data["str_aplicacao1"] = system_context

        logger.info(f"Enviando requisição de geração de texto para SAI LLM...")

        outputs = self._execute_request(self.llm_template_id, inputs_data)

        # Tenta extrair JSON do texto
        if "str_output" in outputs:
            raw_text = outputs["str_output"]

            # Tenta parsear como JSON
            try:
                import json
                parsed = json.loads(raw_text)
                if "resposta" in parsed:
                    return parsed["resposta"]
            except json.JSONDecodeError:
                pass  # Retorna texto puro

            return raw_text
        else:
            logger.warning(f"Resposta da API não contém 'str_output'. Outputs: {outputs}")
            return "A API retornou uma resposta sem o conteúdo esperado."