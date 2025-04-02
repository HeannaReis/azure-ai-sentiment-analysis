import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API Gemini do arquivo .env
api_key = os.getenv("API_KEY_GEMINI")

# Verifica se a chave da API foi carregada corretamente
if not api_key:
    raise ValueError("API_KEY_GEMINI não encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

prompt = "gerar a imagem do simbolo do corinthians."

response = client.models.generate_content(
    model='gemini-2.0-flash-exp-image-generation',
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("ed-image.png")
        image.show()