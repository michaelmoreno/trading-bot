from websocket import WebSocketApp
from ..Handler import Handler

class HeartbeatMessage(Handler):
    def match(self, message: str):
        return message == '{"event":"heartbeat"}'

    def execute(self, ws: WebSocketApp, message: str):
        pass
    