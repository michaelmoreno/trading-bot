from abc import ABC, abstractmethod
from websocket import WebSocketApp

class Handler(ABC):
    @abstractmethod
    def match(self, message: str) -> bool:
        ...
    
    @abstractmethod
    def execute(self, ws: WebSocketApp, message: str) -> None:
        ...

    def handle(self, ws: WebSocketApp, message: str) -> bool:
        if self.match(message):
            self.execute(ws, message)
            return True
        return False
