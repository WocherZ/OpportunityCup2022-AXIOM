import json

from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import *


class WSConsumerTransactions(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({'statis': 'OK'}))
        print("Connect")


    def send_data(self, text_data=None, bytes_data=None, close=False):
        print("Send message")
        self.send(json.dumps({'statis': 'Connected'}))


    def receive(self, text_data=None, bytes_data=None):
        print("Recived message")
        print(text_data)
        pass


    def disconnect(self, code):
        print("Disconnect")
