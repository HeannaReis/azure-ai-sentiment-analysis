# src/main_app.py

import streamlit as st
import time
from datetime import datetime
from PIL import Image
import io
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Opcional: salvar logs em arquivo
        # logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from config.chat_config import ChatConfig
from core.sai_llm_service import SaiLLMService
from core.sai_vision_service import SaiVisionService
from core.ai_coordinator import AICoordinator
from services.image_processor import check_clipboard, reset_uploader, clear_all_images
from services.sai_image_generator import SaiImageGenerator
from services.search_files import ler_todos_arquivos_python

load_dotenv(dotenv_path=ChatConfig.BASE_DIR / ".env")

try:
    ChatConfig.validate()
    logger.info("✅ Configurações validadas com sucesso")
    logger.info(f"📊 Config: {ChatConfig.info()}")
except ValueError as e:
    logger.critical(f"❌ Erro de configuração: {e}")
    st.error(f"🚨 Erro de Configuração\n\n{e}")
    st.info("💡 Verifique o arquivo `.env` e reinicie a aplicação")
    st.stop()

# Inicialização com tratamento de erro
try:
    sai_client = SaiImageGenerator()
except Exception as e:
    logger.error(f"Erro ao inicializar SaiImageGenerator: {e}")
    st.warning("⚠️ Geração de imagens indisponível")
    sai_client = None

# Inicializa estados do session_state (sem alterações)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "clipboard_image_preview" not in st.session_state:
    st.session_state.clipboard_image_preview = None
if "clipboard_image_file" not in st.session_state:
    st.session_state.clipboard_image_file = None
if "last_message_time" not in st.session_state:
    st.session_state.last_message_time = 0
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = "uploader_0"
if "current_prompt_to_process" not in st.session_state:
    st.session_state.current_prompt_to_process = None
if "current_image_bytes_to_process" not in st.session_state:
    st.session_state.current_image_bytes_to_process = None

# Configurações
MAX_MESSAGES = 15
MAX_CONTEXT_MESSAGES = 10

# Carregamento de código com cache e tratamento de erro
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_codigo_fonte():
    """Carrega o código-fonte da aplicação para contexto do LLM."""
    try:
        codigo = ler_todos_arquivos_python()
        if codigo:
            logger.info(f"✅ Código-fonte carregado: {len(codigo)} caracteres")
            return codigo
        else:
            logger.warning("⚠️ Nenhum código-fonte encontrado")
            return ""
    except Exception as e:
        logger.error(f"❌ Erro ao carregar código-fonte: {e}")
        return ""

codigo_fonte_app = carregar_codigo_fonte()

# Inicialização do AICoordinator com tratamento de erro
@st.cache_resource
def get_ai_coordinator():
    """Inicializa e retorna o coordenador de IA."""
    try:
        sai_llm_service = SaiLLMService()
        sai_vision_service = SaiVisionService()
        coordinator = AICoordinator(
            chat_service=sai_llm_service,
            vision_service=sai_vision_service
        )
        logger.info("✅ AICoordinator inicializado")
        return coordinator
    except Exception as e:
        logger.critical(f"❌ Erro ao inicializar AICoordinator: {e}")
        st.error(f"🚨 Erro Fatal\n\n{e}")
        st.stop()

ai_coordinator = get_ai_coordinator()

# Funções de callback e agendamento (pequenas adaptações)
def on_paste_click():
    clipboard_file, clipboard_preview = check_clipboard()
    if clipboard_file and clipboard_preview:
        reset_uploader(st.session_state)
        st.session_state.clipboard_image_file = clipboard_file
        st.session_state.clipboard_image_preview = clipboard_preview
        return True
    return False

def on_file_upload():
    st.session_state.clipboard_image_preview = None
    st.session_state.clipboard_image_file = None

def schedule_message_processing(user_input, image_file_obj=None):
    st.session_state.processing = True
    st.session_state.current_prompt_to_process = user_input
    if image_file_obj:
        try:
            image_bytes = image_file_obj.getbuffer()
            st.session_state.current_image_bytes_to_process = image_bytes
        except Exception as e:
            logger.error(f"Erro ao obter bytes da imagem: {e}")
            st.session_state.current_image_bytes_to_process = None
            st.error("Erro ao processar a imagem. Tente novamente.")
    else:
        st.session_state.current_image_bytes_to_process = None
    st.rerun()

def execute_scheduled_processing():
    user_input = st.session_state.current_prompt_to_process
    image_bytes = st.session_state.current_image_bytes_to_process

    current_time = time.time()
    time_since_last_message = current_time - st.session_state.last_message_time
    wait_time = max(0, 2 - time_since_last_message)
    time.sleep(wait_time)
    st.session_state.last_message_time = time.time()

    img_display_for_history = None

    if image_bytes:
        try:
            img_display_for_history = Image.open(io.BytesIO(image_bytes))
            st.session_state.messages.append({"role": "user", "content": user_input, "image": img_display_for_history})
        except Exception as e:
            logger.error(f"Erro ao preparar imagem para histórico: {e}")
            st.session_state.messages.append({"role": "user", "content": f"{user_input} (erro ao carregar imagem)"})
            image_bytes = None
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    response = ""
    system_context_for_llm = None

    if not image_bytes:
        # Se não há imagem, constrói o contexto completo para o LLM
        system_context_for_llm = ""
        if codigo_fonte_app:
            system_context_for_llm += f"CONTEXTO DO CÓDIGO DA APLICAÇÃO:\n```python\n{codigo_fonte_app}\n```\n\n"

        # Pegar apenas as mensagens mais recentes para o contexto
        start_idx = max(0, len(st.session_state.messages) - 1 - MAX_CONTEXT_MESSAGES)
        recent_messages = st.session_state.messages[start_idx:-1]

        logger.info(f"Enviando {len(recent_messages)} mensagens recentes como contexto para o LLM")

        for message in recent_messages:
            role = message["role"]
            content = message["content"]
            system_context_for_llm += f"{role.capitalize()}: {content}\n"

    try:
        # Chama o AICoordinator, passando o user_input como prompt e o contexto se for texto puro
        response = ai_coordinator.generate_content(
            user_prompt=user_input,
            image_bytes=image_bytes,
            system_context_for_llm=system_context_for_llm
        )
    except Exception as e:
        logger.error(f"Erro na geração da resposta da IA: {e}")
        response = f"❌ Erro ao gerar resposta: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": response})

    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    st.session_state.processing = False
    st.session_state.current_prompt_to_process = None
    st.session_state.current_image_bytes_to_process = None

if st.session_state.processing and st.session_state.current_prompt_to_process is not None:
    execute_scheduled_processing()
    st.rerun()

st.set_page_config(page_title="SAI IA", page_icon="🤖")

with st.sidebar:
    st.title("SAI IA")

    st.markdown("### Gerar Imagem")
    with st.form(key="image_generation_form", clear_on_submit=False):
        image_prompt_input = st.text_input("Digite o prompt para gerar uma imagem:", key="image_prompt_sai_form")
        submitted_image_prompt = st.form_submit_button("Gerar Imagem", icon="✨")

        if submitted_image_prompt:
            if image_prompt_input:
                generated_image_pil = sai_client.generate_image(image_prompt_input)
                if generated_image_pil:
                    st.session_state.messages.append({"role": "assistant", "image": generated_image_pil, "content": f"Imagem gerada com o prompt: {image_prompt_input}"})
                    st.rerun()
            else:
                st.warning("Por favor, digite um prompt para gerar a imagem.")

    st.markdown("### Adicionar Imagem (Opcional)")
    st.caption("Adicione uma imagem se quiser fazer perguntas sobre ela")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Colar", width='stretch'):
            if on_paste_click():
                st.success("Imagem colada!")
                st.rerun()
            else:
                st.warning("Nada encontrado na área de transferência.")
    with col2:
        if st.session_state.clipboard_image_preview or st.session_state.uploaded_image:
            if st.button("🗑️ Limpe", width='stretch'):
                clear_all_images(st.session_state)
                st.rerun()
        else:
            st.write("")

    uploaded_file = st.file_uploader(
        "📷 Ou faça upload de imagem",
        type=["png", "jpg", "jpeg"],
        label_visibility="visible",
        key=st.session_state.file_uploader_key
    )

    if uploaded_file and st.session_state.uploaded_image != uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        on_file_upload()
        st.success("Imagem carregada!")
        st.rerun()

    if st.session_state.clipboard_image_preview:
        st.image(st.session_state.clipboard_image_preview, width='stretch')
        st.caption("Imagem da área de transferência")
    elif st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, width='stretch')
        st.caption("Imagem carregada")

    st.markdown("---")

    if st.button("🧹 Limpar conversa", width='stretch'):
        st.session_state.messages = []
        st.rerun()

    st.caption("Desenvolvido com Streamlit e SAI AI") # Atualizado a descrição

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image"):
            st.image(message["image"], width='stretch')
        st.markdown(message["content"])

if st.session_state.processing:
    with st.chat_message("assistant"):
        st.markdown("Gerando resposta...")

if not st.session_state.processing:
    current_image_file_obj = st.session_state.clipboard_image_file or st.session_state.uploaded_image
    placeholder = "Digite sua pergunta sobre a imagem ou qualquer outro assunto..." if current_image_file_obj else "Digite sua mensagem..."
    user_input = st.chat_input(placeholder)

    if user_input:
        schedule_message_processing(user_input, current_image_file_obj)
else:
    st.chat_input("Aguarde o processamento...", disabled=True)