# chat_streamlit.py
import streamlit as st
from core.handlers.gemini_handler import GeminiHandler
from PIL import Image
import os
from datetime import datetime
from core.config import ASSETS_DIR, PROMPT_CHAT_FILE

st.title("💬 Chat Interativo com IA (Texto e Imagem)")

# Carrega prompt dinâmico do chat
def load_chat_prompt():
    try:
        with open(PROMPT_CHAT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Você é um assistente técnico especialista em desenvolvimento de software e IA."

chat_prompt = load_chat_prompt()

# Inicializa GeminiHandler
@st.cache_resource
def get_gemini_handler():
    return GeminiHandler("gemini-2.0-flash-exp")

gemini_handler = get_gemini_handler()

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image"):
            st.image(message["image"])
        st.markdown(message["content"])

# Entrada do usuário (texto e imagem)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Digite sua mensagem:")
    uploaded_image = st.file_uploader("Opcional: envie uma imagem", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Enviar")

if submitted and user_input:
    img_path = None
    img_display = None

    if uploaded_image:
        os.makedirs(ASSETS_DIR, exist_ok=True)
        img_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_image.name}"
        img_path = os.path.join(ASSETS_DIR, img_name)
        with open(img_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        img_display = Image.open(img_path)

    # Exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input, "image": img_display})
    with st.chat_message("user"):
        if img_display:
            st.image(img_display)
        st.markdown(user_input)

    # Processa resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Gerando resposta..."):
            try:
                full_prompt = f"{chat_prompt}\n\n{user_input}"
                response = gemini_handler.generate_content(img_path, full_prompt)
                st.markdown(response)
            except Exception as e:
                response = f"❌ Erro ao gerar resposta: {str(e)}"
                st.error(response)

    # Salva resposta da IA no histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Opcional: remover imagem após uso
    if img_path and os.path.exists(img_path):
        os.remove(img_path)