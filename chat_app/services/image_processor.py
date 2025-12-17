# chat_platform/src/services/image_processor.py
import streamlit as st
import io
import os
from datetime import datetime
from PIL import Image

# Tenta importar ImageGrab apenas se estiver em um ambiente onde possa funcionar
try:
    from PIL import ImageGrab
    IMAGEGRAB_AVAILABLE = True
except ImportError:
    IMAGEGRAB_AVAILABLE = False
    print("ImageGrab (para clipboard) não disponível. Este recurso pode não funcionar.")


def check_clipboard() -> tuple[object | None, Image.Image | None]:
    """
    Verifica a área de transferência para uma imagem.
    Retorna um objeto de arquivo simulado (para compatibilidade com st.file_uploader)
    e um objeto PIL Image.
    """
    if not IMAGEGRAB_AVAILABLE:
        st.sidebar.warning("Acesso à área de transferência não disponível neste ambiente.")
        return None, None
    try:
        img = ImageGrab.grabclipboard()
        if img is not None and isinstance(img, Image.Image):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            # Objeto de arquivo simulado para compatibilidade
            class ClipboardFile:
                def __init__(self, bytes_data, name_suffix=""):
                    self.bytes_data = bytes_data
                    self.name = f"clipboard_{datetime.now().strftime('%Y%m%d%H%M%S')}{name_suffix}.png"
                def getbuffer(self):
                    return self.bytes_data.getvalue()
                @property
                def size(self):
                    return len(self.bytes_data.getvalue())

            return ClipboardFile(img_byte_arr, name_suffix=f"_{img.size[0]}x{img.size[1]}"), img
        return None, None
    except Exception as e:
        st.sidebar.error(f"Erro ao acessar a área de transferência: {e}")
        return None, None

def reset_uploader(session_state):
    """Reseta o Streamlit file_uploader alterando sua chave."""
    current_key = session_state.file_uploader_key
    key_num = int(current_key.split("_")[1])
    session_state.file_uploader_key = f"uploader_{key_num + 1}"
    session_state.uploaded_image = None

def clear_all_images(session_state):
    """Limpa todas as imagens carregadas ou da área de transferência."""
    reset_uploader(session_state)
    session_state.clipboard_image_preview = None
    session_state.clipboard_image_file = None