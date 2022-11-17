from typing import List, Tuple
import requests
import base64
import hashlib
import hmac
import urllib.parse
import time

class KrakenConnector:
    base_http: str = 'https://api.kraken.com'
    base_ws: str = 'wss://ws.kraken.com'
    _offered_pairs: List[Tuple[str, str]]

    def __init__(self, api_key: str, api_priv: str):
        self.api_key = api_key
        self.api_priv = api_priv
        self._offered_pairs = []

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
