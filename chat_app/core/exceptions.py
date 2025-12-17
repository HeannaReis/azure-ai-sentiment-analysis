# src/core/exceptions.py

class SAIApiError(Exception):
    """Exceção para erros ocorridos durante a comunicação com a API SAI."""
    pass

class ConfigurationError(Exception):
    """Exceção para erros de configuração, como chaves de API ou IDs de template ausentes."""
    pass