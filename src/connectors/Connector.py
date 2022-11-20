from decimal import Decimal
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod, abstractproperty
import requests
from websocket import WebSocketApp

from .ws_handlers.Handler import Handler

class Connector(ABC):
    base_http: str
    base_ws: str
    message_handlers: List[Handler]
    ws: WebSocketApp

    def __init__(self, base_http: str, base_ws: str, message_handlers: List[Handler], desired_pairs: List[Tuple[str, str]]):
        self.base_http = base_http
        self.base_ws = base_ws
        self.message_handlers = message_handlers
        self.desired_pairs = desired_pairs

    @abstractmethod
    def request(self, uri_path: str, payload: dict) -> requests.models.Response:
        ...
    
    @abstractmethod
    def request_balance(self) -> dict:
        ...

    @abstractmethod
    def request_trade_history(self) -> dict:
        ...
    
    @abstractmethod
    def get_offered_pairs(self) -> List[Tuple[str, str]]:
        ...

    @abstractmethod
    def subscribe(self, pairs: List[Tuple[str, str]]):
        ...

    def start_websocket(self):
        self.ws = WebSocketApp(
            self.base_ws,
            on_open=self.handle_open,
            on_message=self.handle_message,
            on_error=lambda ws, err: print(err))
        self.ws.run_forever()

    def handle_open(self, ws: WebSocketApp):
        self.subscribe(self.desired_pairs)

    def handle_message(self, ws: WebSocketApp, message: str):
        for handler in self.message_handlers:
            if handler.handle(self.ws, message):
                return
        raise Exception(f'No Handler found for message: {message}')

    def get_balance(self) -> Dict[str, Decimal]:
        balances = self.request_balance()
        return {asset: Decimal(balance) for asset, balance in balances.items()}

    def get_trade_history(self) -> Dict[str, Decimal]:
        return self.request_trade_history()
