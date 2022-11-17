from typing import List, NamedTuple, Tuple


class Order(NamedTuple):
    price: float
    size: float


class Orderbook:
    market: Tuple[str, str]
    bids: List[Order]
    asks: List[Order]
    depth: int

    def __init__(self, bids: List[Order], asks: List[Order], depth: int):
        self.bids = bids[:depth]
        self.asks = asks[:depth]
        self.depth = depth
    
    @property
    def top_bid(self) -> Order:
        return self.bids[0]
    
    @property
    def top_ask(self) -> Order:
        return self.asks[0]
    
    @property
    def spread(self) -> float:
        return self.top_ask.price - self.top_bid.price
