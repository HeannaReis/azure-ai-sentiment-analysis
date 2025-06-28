from google import genai
from google.genai import types
from PIL import Image
import io
import os

class GeminiImageGenerator:
    def __init__(self):
        api_key = os.getenv("API_KEY_GEMINI")
        if not api_key:
            raise ValueError("API_KEY_GEMINI não encontrada no arquivo .env")
        self.client = genai.Client(api_key=api_key)

    def generate_image(self, prompt: str) -> Image.Image | None:
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-preview-image-generation',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    return Image.open(io.BytesIO(part.inline_data.data))
            return None
        except Exception as e:
            print(f"Erro ao gerar imagem: {e}")
            return None
