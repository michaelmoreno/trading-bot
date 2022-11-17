from typing import Dict
from decimal import Decimal
from strategies.Strategy import Strategy


class Bot:
    strategy: Strategy
    inventory: Dict[str, Decimal]

    def __init__(self, strategy: Strategy):
        self.strategy = strategy
    
    def setStrategy(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def executeStrategy(self) -> None:
        self.strategy.execute()