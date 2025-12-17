# src/config/config.py
import os
from pathlib import Path
from typing import Dict

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(f"Config BASE_DIR: {BASE_DIR}")  # Debugging line para verificar o caminho base
    ASSETS_DIR = BASE_DIR / "assets"
    
    PROCESSED_DIR = BASE_DIR / "processed_images"
    print(f"Config PROCESSED_DIR: {PROCESSED_DIR}")  # Debugging line para verificar o caminho de imagens processadas
    OUTPUT_DOCX = BASE_DIR / "resumo_analises_imagens.docx"
    OUTPUT_MD = BASE_DIR / "resumo_analises_imagens.md"

    # Caminhos para prompts dinâmicos
    PROMPT_DIR = BASE_DIR / "prompt"
    PROMPT_DOC_FILE = PROMPT_DIR / "prompt_doc.txt"
    # PROMPT_CHAT_FILE não é mais necessário para a aplicação de documentação

    # Configuração de logs
    LOG_DIR = BASE_DIR / "logs"

    # Configuração de histórico
    HISTORY_FILE = BASE_DIR / "historico_analises.json"

    # Configuração de rate limiting para o processamento geral (pode ser ajustado)
    PROCESSING_RATE_LIMIT: Dict[str, int] = {
        "max_requests": int(os.getenv("PROCESSING_RATE_LIMIT_REQUESTS", "9")),
        "period_seconds": int(os.getenv("PROCESSING_RATE_LIMIT_PERIOD", "60"))
    }

    # Configuração de rate limiting para chamadas à API SAI
    SAI_API_RATE_LIMIT: Dict[str, int] = {
        "max_requests": int(os.getenv("SAI_API_RATE_LIMIT_REQUESTS", "14")),
        "period_seconds": int(os.getenv("SAI_API_RATE_LIMIT_PERIOD", "60"))
    }

    # API SAI
    SAI_BASE_URL = "https://sai-library.saiapplications.com"

    # Template ID para geração de documentação (fornecido pelo usuário)
    SAI_DOCUMENTATION_TEMPLATE_ID = "6941fe5ae62abe55742ae842"

    @classmethod
    def validate(cls) -> None:
        """
        Valida se todas as configurações obrigatórias estão presentes.

        Raises:
            ValueError: Se alguma configuração obrigatória estiver faltando
        """
        required_configs = {
            "SAI_BASE_URL": cls.SAI_BASE_URL,
            "SAI_DOCUMENTATION_TEMPLATE_ID": cls.SAI_DOCUMENTATION_TEMPLATE_ID,
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
    def ensure_directories(cls):
        """Garante que todos os diretórios necessários existam."""
        for directory in [cls.ASSETS_DIR, cls.PROCESSED_DIR, cls.LOG_DIR, cls.PROMPT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

# Garante que os diretórios existam ao importar a configuração
Config.ensure_directories()