from django.shortcuts import render

from .models import Transaction, Pattern, clear_base

from kafka import KafkaConsumer
from json import loads
import json

# Kafka logic
# print("Kafka started from service")
# clear_base()
# topic_name = 'TestKafka'
# consumer = KafkaConsumer(topic_name,
#                          bootstrap_servers=['localhost:9092'],
#                          value_deserializer=lambda v: json.loads(v.decode('utf-8')),
#                          group_id='group_id',
#                          auto_offset_reset='earliest',
#                          api_version=(0, 10, 1)
#                          )
#
# for message in consumer:
#     print("Kafka work:", message.value)
#     # Patterns
#     Transaction.create_by_dict(Transaction, message.value)