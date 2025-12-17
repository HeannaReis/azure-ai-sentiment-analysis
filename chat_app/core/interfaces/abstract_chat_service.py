# src\core\interfaces\abstract_chat_service.py

import abc
from typing import Optional # Importar Optional

class AbstractChatService(abc.ABC):
    """Interface para serviços de chat baseados em texto."""
    @abc.abstractmethod
    def generate_content(self, user_prompt: str, system_context: Optional[str] = None) -> str: # Assinatura atualizada
        """
        Gera conteúdo textual a partir de um prompt do usuário,
        com um contexto de sistema opcional.
        """
        pass