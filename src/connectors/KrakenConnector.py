from typing import List, Tuple
import requests
import base64
import hashlib
import hmac
import urllib.parse
import time
from websocket import WebSocketApp
from .ws_handlers.Handler import Handler

class KrakenConnector:
    base_http: str = 'https://api.kraken.com'
    base_ws: str = 'wss://ws.kraken.com'
    _offered_pairs: List[Tuple[str, str]]
    message_handlers: List[Handler]

    def __init__(self, api_key: str, api_priv: str, message_handlers: List[Handler]):
        self.api_key = api_key
        self.api_priv = api_priv
        self._offered_pairs = []
        self.message_handlers = message_handlers

    @property
    def offered_pairs(self) -> List[Tuple[str, str]]:
        result = requests.get(f'{self.base_http}/0/public/AssetPairs').json()['result']
        return [(pair['base'], pair['quote']) for pair in result.values()]

    def start_websocket(self):
        self.ws = WebSocketApp(
            self.base_ws,
            on_open=self.handle_open,
            on_message=self.handle_message,
            on_error=lambda ws, err: print(err))
        self.ws.run_forever()

    def handle_message(self, ws: WebSocketApp, message: str):
        for handler in self.message_handlers:
            if handler.handle(self.ws, message):
                return
        raise Exception(f'No Handler found for message: {message}')

    def handle_open(self, ws: WebSocketApp):
        self.ws.send('{"event":"subscribe", "pair":["XBT/USD"], "subscription":{"name":"ticker"}}')

    def generate_signature(self, urlpath: str, payload: dict) -> str:
        postdata = urllib.parse.urlencode(payload)
        encoded = (payload['nonce'] + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.api_priv), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def request(self, uri_path: str, payload: dict) -> requests.models.Response:
        payload['nonce'] = str(int(time.time() * 1000))
        headers = {
            'API-Key': self.api_key,
            'API-Sign': self.generate_signature(uri_path, payload)
        }
        res = requests.post(self.base_http + uri_path, headers=headers, data=payload)
        return res
