from typing import List
from connectors.Connector import Connector
from orderbook.Orderbook import Orderbook


class Monitor:
    connectors: List[Connector]
    orderbooks: List[Orderbook]
    