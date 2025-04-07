# core/rate_limiter.py
import time
from collections import deque
from threading import Lock
from typing import Optional

class RateLimiter:
    """
    Implementa um limitador de taxa para controlar o número de requisições
    em um determinado período de tempo.
    """
    def __init__(self, max_requests: int, period_seconds: int):
        """
        Inicializa o limitador de taxa.
        
        Args:
            max_requests: Número máximo de requisições permitidas no período
            period_seconds: Período de tempo em segundos
        """
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.requests = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        """
        Verifica se uma nova requisição pode ser feita.
        
        Returns:
            bool: True se a requisição for permitida, False caso contrário
        """
        with self.lock:
            current_time = time.time()

            # Remove requisições antigas fora da janela de tempo
            while self.requests and self.requests[0] <= current_time - self.period_seconds:
                self.requests.popleft()

            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True
            return False

    def wait_for_slot(self) -> None:
        """
        Aguarda até que um slot esteja disponível para uma nova requisição.
        """
        while not self.allow_request():
            current_time = time.time()
            
            # Calcula o tempo de espera baseado na requisição mais antiga
            if self.requests:
                earliest_request_time = self.requests[0] 
                remaining_time = max(0, self.period_seconds - (current_time - earliest_request_time))
            else:
                remaining_time = 1  # Espera padrão se não houver requisições
                
            time.sleep(remaining_time)