from typing import Protocol
import requests

class Connector(Protocol):
    offered_pairs: property

    def request(self, uri_path: str, payload: dict) -> requests.models.Response:
        ...
