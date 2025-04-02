# config.py
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_GENERATED_DIR = os.path.join(BASE_DIR, "assets", "image_generated")
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed_images')
OUTPUT_DOCX = os.path.join(BASE_DIR, "resumo_analises_imagens.docx")
OUTPUT_MD = os.path.join(BASE_DIR, "resumo_analises_imagens.md")

# Caminhos para prompts dinâmicos
PROMPT_DOC_FILE = os.path.join(BASE_DIR, 'src', 'prompt', "prompt_doc.txt")
PROMPT_CHAT_FILE = os.path.join(BASE_DIR, 'src', 'prompt', "prompt_chat.txt")