# src\core\ai_coordinator.py

import logging
from typing import Optional

from core.rate_limiter import RateLimiter
from config.chat_config import ChatConfig
from core.interfaces.abstract_chat_service import AbstractChatService
from core.interfaces.abstract_vision_service import AbstractVisionService

logger = logging.getLogger(__name__)

class AICoordinator:
    def __init__(self, chat_service: AbstractChatService, vision_service: AbstractVisionService):
        self.chat_service = chat_service
        self.vision_service = vision_service
        self.rate_limiter = RateLimiter(
            max_requests=ChatConfig.CHAT_RATE_LIMIT["max_requests"],
            period_seconds=ChatConfig.CHAT_RATE_LIMIT["period_seconds"]
        )
        logger.info(f"AICoordinator inicializado com rate limit: {ChatConfig.CHAT_RATE_LIMIT['max_requests']} reqs/{ChatConfig.CHAT_RATE_LIMIT['period_seconds']}s.")
        logger.info(f"Serviço de Chat (texto): {self.chat_service.__class__.__name__}, Serviço de Visão (imagem): {self.vision_service.__class__.__name__}")


    # Assinatura do método generate_content atualizada
    def generate_content(self, user_prompt: str, image_bytes: Optional[bytes] = None, system_context_for_llm: Optional[str] = None) -> str:
        """
        Gera conteúdo com base em um prompt do usuário, dados de imagem e um contexto de sistema opcional.
        Aplica controle de taxa antes de chamar o serviço apropriado.
        """
        self.rate_limiter.wait_for_slot()
        logger.debug("Slot de rate limit disponível, prosseguindo com a requisição.")

        if image_bytes:
            logger.info("Delegando para o serviço de visão para processar imagem e prompt.")
            # O serviço de visão recebe apenas o prompt direto do usuário
            return self.vision_service.analyze_image(image_bytes, user_prompt)
        elif user_prompt:
            logger.info("Delegando para o serviço de chat (LLM) para processar apenas prompt de texto.")
            # O serviço de chat LLM recebe o prompt do usuário e o contexto completo
            return self.chat_service.generate_content(user_prompt=user_prompt, system_context=system_context_for_llm)
        else:
            logger.warning("Nenhum prompt ou imagem fornecido para geração de conteúdo.")
            return "Por favor, forneça uma mensagem ou imagem para processar."
