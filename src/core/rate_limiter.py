import time
from collections import deque
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int, period_seconds: int):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.requests = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        with self.lock:
            current_time = time.time()

            # Remove requests antigos fora da janela de tempo
            while self.requests and self.requests[0] <= current_time - self.period_seconds:
                self.requests.popleft()

            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True
            else:
                return False

    def wait_for_slot(self):
        while not self.allow_request():
            time.sleep(1)