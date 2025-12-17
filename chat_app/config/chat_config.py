# src/config/chat_config.py

import os
from pathlib import Path
from typing import Dict

class ChatConfig:
    """
    Configurações centralizadas da aplicação SAI Multi Agent.

    Estrutura do projeto:
    projeto/
    ├── chat_app/
    │   ├── config/
    │   │   └── chat_config.py  ← Este arquivo
    │   ├── core/
    │   ├── services/
    │   └── main_app.py
    ├── .env
    └── README.md

    Variáveis de ambiente obrigatórias (.env):
    - SAI_LIBRARY_API_KEY: Chave de autenticação da API SAI

    Variáveis opcionais:
    - RATE_LIMIT_REQUESTS: Máximo de requisições (padrão: 7)
    - RATE_LIMIT_PERIOD: Período em segundos (padrão: 60)
    """

    # Diretórios
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    print(BASE_DIR)
    SRC_DIR = BASE_DIR
    print(SRC_DIR)

    # Rate Limiting (com fallback para valores padrão)
    CHAT_RATE_LIMIT: Dict[str, int] = {
        "max_requests": int(os.getenv("RATE_LIMIT_REQUESTS", "7")),
        "period_seconds": int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    }

    # API SAI
    SAI_BASE_URL = "https://sai-library.saiapplications.com"

    # Template IDs
    SAI_IMAGE_GENERATION_TEMPLATE_ID = "69165a1e9600da174fc60a05"
    """Template para geração de imagens via DALL-E/Stable Diffusion"""

    SAI_VISION_TEMPLATE_ID = "690a94d76151064fad274988"
    """Template para análise de imagens (Vision API)"""

    SAI_LLM_TEMPLATE_ID = "66efacc0976f05c335ef78d2"
    """Template para chat de texto (LLM API)"""

    @classmethod
    def validate(cls) -> None:
        """
        Valida se todas as configurações obrigatórias estão presentes.

        Raises:
            ValueError: Se alguma configuração obrigatória estiver faltando
        """
        required_configs = {
            "SAI_BASE_URL": cls.SAI_BASE_URL,
            "SAI_IMAGE_GENERATION_TEMPLATE_ID": cls.SAI_IMAGE_GENERATION_TEMPLATE_ID,
            "SAI_VISION_TEMPLATE_ID": cls.SAI_VISION_TEMPLATE_ID,
            "SAI_LLM_TEMPLATE_ID": cls.SAI_LLM_TEMPLATE_ID,
        }

        missing = [name for name, value in required_configs.items() if not value]

        if missing:
            raise ValueError(
                f"Configurações obrigatórias faltando: {', '.join(missing)}"
            )

        # Valida se BASE_DIR existe
        if not cls.BASE_DIR.exists():
            raise ValueError(f"BASE_DIR não existe: {cls.BASE_DIR}")

    @classmethod
    def get_api_key(cls) -> str:
        """
        Obtém a API key do ambiente.

        Returns:
            str: API key da SAI

        Raises:
            ValueError: Se SAI_LIBRARY_API_KEY não estiver definida
        """
        api_key = os.getenv("SAI_LIBRARY_API_KEY")
        if not api_key:
            raise ValueError(
                "SAI_LIBRARY_API_KEY não encontrada no .env. "
                "Configure a variável de ambiente antes de usar a aplicação."
            )
        return api_key

    @classmethod
    def info(cls) -> Dict[str, str]:
        """
        Retorna informações de configuração para debug.

        Returns:
            Dict com informações não-sensíveis da configuração
        """
        return {
            "base_dir": str(cls.BASE_DIR),
            "src_dir": str(cls.SRC_DIR),
            "api_url": cls.SAI_BASE_URL,
            "rate_limit": f"{cls.CHAT_RATE_LIMIT['max_requests']} reqs/{cls.CHAT_RATE_LIMIT['period_seconds']}s",
            "templates": {
                "image_gen": cls.SAI_IMAGE_GENERATION_TEMPLATE_ID[:8] + "...",
                "vision": cls.SAI_VISION_TEMPLATE_ID[:8] + "...",
                "llm": cls.SAI_LLM_TEMPLATE_ID[:8] + "..."
            }
        }

# Validação automática ao importar (opcional, pode ser removido)
# ChatConfig.validate()