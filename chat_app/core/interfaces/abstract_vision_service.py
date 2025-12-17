import abc

class AbstractVisionService(abc.ABC):
    """Interface para serviços de análise de imagem."""
    @abc.abstractmethod
    def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """Analisa uma imagem com um prompt, retornando um resultado textual."""
        pass