from websocket import WebSocketApp
from ..Handler import Handler

class SubscribedMessage(Handler):
    def match(self, message: str):
        return '"event":"subscriptionStatus"' in message

    def execute(self, ws: WebSocketApp, message: str):
        print('---------------Sub-----------------')
    