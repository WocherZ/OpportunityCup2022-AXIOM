import json
import time

import redis
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import *


class WSConsumerTransactions(WebsocketConsumer):
    def connect(self):
        self.accept()
        # self.send(json.dumps({'statis': 'OK'}))
        self.send_data()
        print("Connect")


    def send_data(self, text_data=None, bytes_data=None, close=False):
        result_dictionary = {}
        result_dictionary['action'] = 'create'
        result_dictionary['num'] = 10
        result_dictionary['data'] = Transaction.get_last_n_records(Transaction, 10)
        redis_counter = redis.StrictRedis(host="localhost", port=6379, db=0)
        result_dictionary['first_hist'] = {
            'frod': int(redis_counter.get("fraud")),
            'notfrod': int(redis_counter.get("no_fraud"))
        }
        result_dictionary['second_hist'] = {
            'notfrod': int(redis_counter.get("no_fraud")),
            'pattern1': int(redis_counter.get("counter_1")),
            'pattern2': int(redis_counter.get("counter_2")),
            'pattern3': int(redis_counter.get("counter_3")),
            'pattern4': int(redis_counter.get("counter_4")),
            'pattern5': int(redis_counter.get("counter_5")),
            'pattern6': int(redis_counter.get("counter_6"))
        }
        print("Send message")
        self.send(json.dumps(result_dictionary))


    def receive(self, text_data=None, bytes_data=None):
        print("Recived message")
        print(text_data)
        if text_data == "DATA":
            time.sleep((1))
            self.send_data()
            print("Отправлено")




    def disconnect(self, code):
        print("Disconnect")
