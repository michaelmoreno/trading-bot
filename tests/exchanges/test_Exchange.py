from exchanges.Exchange import Exchange
from connectors.KrakenConnector import KrakenConnector
from connectors.ws_handlers.messages.SubscribedMessage import SubscribedMessage
from typing import Dict, List, Tuple
from dotenv import dotenv_values

config: Dict[str, str] = dotenv_values(".env") # type: ignore

def test_exchange():
    connector = KrakenConnector(
        config['KRAKEN_API'],
        config['KRAKEN_PRIV'],
        [SubscribedMessage()],
        [('XBT', 'USD')]
        )
    exchange = Exchange(connector)
    assert exchange.balance['error'] == []
    assert exchange.trades_history['error'] == []

    offered_pairs = exchange.offered_pairs
    assert type(offered_pairs) == list
    assert len(offered_pairs) > 0
    assert all([type(pair) == tuple and len(pair) == 2 for pair in offered_pairs])
    assert all([type(base) == str and type(quote) == str for base, quote in offered_pairs])
    