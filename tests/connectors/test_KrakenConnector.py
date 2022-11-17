from src.connectors.KrakenConnector import KrakenConnector
from typing import Dict
from dotenv import dotenv_values

config: Dict[str,str] = dotenv_values(".env") # type: ignore

def test_request():
    connector = KrakenConnector(config['KRAKEN_API'], config['KRAKEN_PRIV'])
    data = {}
    res = connector.request('/0/private/Balance', data).json()
    assert res['error'] == []
