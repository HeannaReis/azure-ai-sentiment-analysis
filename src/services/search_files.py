import os
import glob
from pathlib import Path
from config.config import Config
import logging  # Importe o módulo de logging

# Configure o logging (você pode ajustar o nível conforme necessário)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ler_todos_arquivos_python() -> str:
    """Lê todo o conteúdo de todos os arquivos .py a partir de src/"""
    src_dir = Config.BASE_DIR
    conteudo_total = ""

    if not src_dir.exists():
        logging.warning(f"Diretório 'src' não encontrado: {src_dir}")
        return ""

    padrao_busca = os.path.join(src_dir.as_posix(), '**', '*.py')
    arquivos = glob.glob(padrao_busca, recursive=True)

    for arquivo in sorted(arquivos):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                rel_path = os.path.relpath(arquivo, src_dir)
                conteudo_total += f"\n\n# {rel_path}\n\n{f.read()}"
                logging.info(f"Arquivo lido com sucesso: {rel_path}")  # Log de sucesso
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {arquivo}: {e}")  # Log de erro
            continue

    return conteudo_total