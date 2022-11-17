from src.connectors.Connector import Connector

class Exchange:
    connector: Connector

    def __init__(self, connector: Connector):
        self.connector = connector
    
    @property
    def balance(self):
        return self.connector.request('/0/private/Balance', {}).json()

    @property
    def trades_history(self):
        return self.connector.request('/0/private/TradesHistory', {}).json()

    @property
    def offered_pairs(self):
        return self.connector.offered_pairs
