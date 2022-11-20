from typing import List, Tuple
from decimal import Decimal
import requests
import base64
import hashlib
import hmac
import urllib.parse
import time
from .ws_handlers.Handler import Handler
from .Connector import Connector

class BinanceUSConnector(Connector):
    base_http: str = 'https://api.binance.us'
    base_ws: str = 'wss://stream.binance.us:9443'

    def __init__(self, api_key: str, api_priv: str, message_handlers: List[Handler], desired_markets: List[Tuple[str, str]]):
        super().__init__(
            self.base_http, self.base_ws, message_handlers, desired_markets)
        self.api_key = api_key
        self.api_priv = api_priv

    def subscribe(self):
        joined = ','.join([f'{base}/{quote}' for base, quote in self.desired_markets])
        self.ws.send('{"event":"subscribe", "market":'+joined+', "subscription":{"name":"ticker"}}')

    def generate_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self.api_priv, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    def request(self, uri_path, data) -> requests.models.Response:
        data['timestamp'] = int(round(time.time() * 1000))
        headers = {'X-MBX-APIKEY': self.api_key}
        signature = self.generate_signature(data) 
        params={
            **data,
            "signature": signature,
            }           
        req = requests.get((self.base_http + uri_path), params=params, headers=headers)
        return req

    def get_offered_markets(self) -> List[Tuple[str, str]]: # need to confirm
        result = self.request('/sapi/v1/otc/coinPairs', {}).json()
        return [(market['fromCoin'], market['toCoin']) for market in result]
