from decimal import Decimal
from typing import Dict
from orderbook.Orderbook import Orderbook
from connectors.Connector import Connector

class Exchange:
    connector: Connector
    orderbooks: Dict[str, Orderbook]

    def __init__(self, connector: Connector):
        self.connector = connector
    
    @property
    def balance(self) -> Dict[str, Decimal]:
        return self.connector.get_balance()

    @property
    def trades_history(self):
        return self.connector.get_trade_history()

    @property
    def offered_pairs(self):
        return self.connector.get_offered_pairs()
