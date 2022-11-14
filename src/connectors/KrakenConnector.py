from typing import List, Tuple
import requests

class KrakenConnector:
    base_http: str = 'https://api.kraken.com'
    base_ws: str = 'wss://ws.kraken.com'
    _offered_pairs: List[Tuple[str, str]]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._offered_pairs = []

    @property 
    def offered_pairs(self) -> List[Tuple[str, str]]:
        return self._offered_pairs or self.get_offered_pairs()

    def get_offered_pairs(self) -> List[Tuple[str, str]]:
        result = requests.get(f'{self.base_http}/0/public/AssetPairs').json()['result']
        return [(pair['base'], pair['quote']) for pair in result.values()]
