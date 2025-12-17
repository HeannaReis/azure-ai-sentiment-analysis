# chat_platform/services/search_files.py
import os
import glob
from pathlib import Path
import logging
from config.chat_config import ChatConfig

logger = logging.getLogger(__name__)

# Configurações
EXCLUDE_DIRS = {"ml_fine_tunning", "ml_models", "__pycache__", "venv", ".git", ".venv"}
EXCLUDE_FILES = {"search_files.py"}
MAX_FILE_SIZE = 100_000  # 100KB
MAX_TOTAL_SIZE = 500_000  # 500KB

def should_exclude_path(path: Path) -> bool:
    """Verifica se o caminho deve ser excluído."""
    return (
        any(exclude in path.parts for exclude in EXCLUDE_DIRS) or
        path.name in EXCLUDE_FILES
    )

def ler_todos_arquivos_python() -> str:
    """
    Lê todo o conteúdo de todos os arquivos .py do diretório 'src'.
    Retorna string formatada para contexto do LLM.
    """
    src_dir = ChatConfig.SRC_DIR

    if not src_dir.exists():
        logger.warning(f"Diretório src não encontrado: {src_dir}")
        return ""

    conteudo_total = ""
    arquivos_lidos = 0

    # Busca recursiva
    padrao_busca = str(src_dir / "**" / "*.py")
    arquivos = sorted(glob.glob(padrao_busca, recursive=True))

    logger.info(f"Encontrados {len(arquivos)} arquivos Python em {src_dir}")

    for arquivo in arquivos:
        path = Path(arquivo)

        # Filtro de exclusão
        if should_exclude_path(path):
            logger.debug(f"Excluído: {path.name}")
            continue

        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                file_content = f.read()

                # Validação de tamanho
                if len(file_content) > MAX_FILE_SIZE:
                    logger.warning(f"Arquivo grande truncado: {path.name}")
                    file_content = file_content[:MAX_FILE_SIZE] + "\n# ... (truncado)"

                # Verifica limite total
                if len(conteudo_total) + len(file_content) > MAX_TOTAL_SIZE:
                    logger.warning(f"Limite de contexto atingido após {arquivos_lidos} arquivos")
                    break

                # Adiciona ao contexto
                rel_path = path.relative_to(ChatConfig.BASE_DIR)
                conteudo_total += f"\n\n# {rel_path}\n\n{file_content}"
                arquivos_lidos += 1
                logger.debug(f"Lido: {rel_path}")

        except Exception as e:
            logger.error(f"Erro ao ler {arquivo}: {e}")
            continue

    logger.info(f"Contexto gerado: {arquivos_lidos} arquivos, {len(conteudo_total)} caracteres")
    return conteudo_total