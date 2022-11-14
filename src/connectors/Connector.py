from typing import Protocol

class Connector(Protocol):
    offered_pairs: property
    