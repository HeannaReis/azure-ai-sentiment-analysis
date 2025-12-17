# src/core/base_sai_service.py
import requests
import json
import logging
from typing import Dict

from config.config import Config
from core.exceptions import SAIApiError, ConfigurationError
from core.rate_limiter import RateLimiter # Importa o RateLimiter

logger = logging.getLogger(__name__)

class BaseSaiService:
    """
    Classe base para serviços que interagem com a API SAI.
    Encapsula a lógica comum de autenticação, requisição e tratamento de erros.
    """
    def __init__(self):
        try:
            self.api_key = Config.get_api_key()
            logger.info(f"{self.__class__.__name__} inicializado com API key válida")
        except ValueError as e:
            logger.error(f"{self.__class__.__name__}: {e}")
            self.api_key = None

        self.base_url = Config.SAI_BASE_URL

        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        } if self.api_key else {}

        # Inicializa um RateLimiter interno para chamadas à API SAI
        self.api_rate_limiter = RateLimiter(
            max_requests=Config.SAI_API_RATE_LIMIT["max_requests"],
            period_seconds=Config.SAI_API_RATE_LIMIT["period_seconds"]
        )
        logger.info(f"{self.__class__.__name__} API Rate Limiter: {Config.SAI_API_RATE_LIMIT['max_requests']} reqs/{Config.SAI_API_RATE_LIMIT['period_seconds']}s")

    def _execute_request(self, template_id: str, inputs: dict, timeout: int = 500) -> Dict:
        """
        Executa uma requisição POST para um template da API SAI e retorna os outputs.
        Levanta exceções customizadas em caso de erro.
        """
        # Aplica o rate limiting antes de executar a requisição
        self.api_rate_limiter.wait_for_slot()
        logger.debug("Slot de rate limit da API disponível para requisição SAI.")

        if not self.api_key:
            raise ConfigurationError(
                "SAI_LIBRARY_API_KEY não configurada. "
                "Verifique o arquivo .env e reinicie a aplicação."
            )
        if not template_id:
            raise ConfigurationError(
                f"ID do template não fornecido para {self.__class__.__name__}"
            )

        url = f"{self.base_url}/api/templates/{template_id}/execute"
        data = {"inputs": inputs}
        response = None

        try:
            logger.info("="*80)
            logger.info(f"🚀 REQUISIÇÃO API SAI - {self.__class__.__name__}")
            logger.info(f"URL: {url}")
            logger.info(f"Template ID: {template_id}")
            logger.info(f"Timeout: {timeout}s")
            logger.debug(f"Payload: {json.dumps(data, indent=2, ensure_ascii=False)}")
            logger.info("="*80)

            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=timeout
            )

            logger.info(f"📥 Status: {response.status_code}")
            logger.debug(f"Headers: {dict(response.headers)}")

            response.raise_for_status()

            return self._extract_content(response)

        except requests.exceptions.HTTPError as http_err:
            # O _handle_http_error já levanta a exceção SAIApiError
            self._handle_http_error(http_err, response)
        except requests.exceptions.Timeout:
            raise SAIApiError(
                f"⏱️ Timeout após {timeout}s ao comunicar com API SAI "
                f"(Template: {template_id[:8]}...)"
            )
        except requests.exceptions.ConnectionError as conn_err:
            raise SAIApiError(
                f"🔌 Erro de conexão com API SAI: {str(conn_err)}"
            ) from conn_err
        except SAIApiError:
            raise # Re-raise SAIApiError se já foi levantada
        except Exception as e:
            logger.error(f"❌ Erro inesperado em {self.__class__.__name__}", exc_info=True)
            raise SAIApiError(f"Erro inesperado: {str(e)}") from e

    def _extract_content(self, response: requests.Response) -> Dict:
        """
        Método separado para extração de conteúdo da resposta da API.
        """
        raw_content = response.text.strip()

        if not raw_content:
            raise SAIApiError("API retornou resposta vazia")

        content_type = response.headers.get('Content-Type', '').lower()

        # Tenta parsear como JSON
        if 'application/json' in content_type:
            try:
                response_json = response.json()
                logger.debug(f"JSON parseado: {list(response_json.keys())}")

                # Estrutura esperada: {"outputs": {...}}
                if "outputs" in response_json:
                    return response_json["outputs"]

                # Fallback: procura campos conhecidos
                for key in ['str_output', 'text', 'content', 'result', 'response']:
                    if key in response_json:
                        logger.debug(f"Usando campo '{key}' como str_output")
                        return {"str_output": response_json[key]}

                # Último recurso: retorna JSON completo
                logger.warning("Estrutura JSON desconhecida, retornando como string")
                return {"str_output": json.dumps(response_json)}

            except json.JSONDecodeError:
                logger.debug("Falha ao parsear JSON, tratando como texto")

        # Trata como texto puro
        logger.debug(f"Resposta tratada como texto ({len(raw_content)} chars)")
        return {"str_output": raw_content}

    def _handle_http_error(self, error: requests.exceptions.HTTPError, response: requests.Response) -> None:
        """
        Tratamento de erro HTTP separado.
        """
        status_code = response.status_code if response else "N/A"

        # Tenta extrair mensagem de erro da API
        error_message = f"Erro HTTP {status_code}"
        try:
            error_json = response.json()
            api_error = error_json.get('error') or error_json.get('message')
            if api_error:
                error_message = f"{error_message}: {api_error}"
        except:
            pass # Ignora erro ao tentar parsear JSON se a resposta não for JSON

        logger.error(f"❌ {error_message}")
        logger.debug(f"Resposta: {response.text[:500]}")

        raise SAIApiError(error_message) from error