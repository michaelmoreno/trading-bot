from typing import Dict, List, Tuple
from decimal import Decimal
import requests
import base64
import hashlib
import hmac
import urllib.parse
import time
from websocket import WebSocketApp
from .ws_handlers.Handler import Handler
from .Connector import Connector

class KrakenConnector(Connector):
    base_http: str = 'https://api.kraken.com'
    base_ws: str = 'wss://ws.kraken.com'

    def __init__(self, api_key: str, api_priv: str, message_handlers: List[Handler], desired_markets: List[Tuple[str, str]]):
        super().__init__(
            self.base_http, self.base_ws, message_handlers, desired_markets)
        self.api_key = api_key
        self.api_priv = api_priv

    def get_offered_markets(self) -> List[Tuple[str, str]]:
        result = requests.get(f'{self.base_http}/0/public/Assetmarkets').json()['result']
        return [(market['base'], market['quote']) for market in result.values()]

    def subscribe(self):
        joined = ','.join([f'{base}/{quote}' for base, quote in self.desired_markets])
        self.ws.send('{"event":"subscribe", "market":'+joined+', "subscription":{"name":"ticker"}}')

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

    def request_balance(self) -> dict:
        return self.request('/0/private/Balance', {}).json()['result']

    def request_trade_history(self) -> requests.models.Response:
        return self.request('/0/private/TradesHistory', {}).json()['result']
