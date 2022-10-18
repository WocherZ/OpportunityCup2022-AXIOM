import pandas as pd
import redis
from django.shortcuts import render
from django.http import HttpResponse

from .models import Transaction, Pattern, clear_base
from .patterns import first_pattern, second_pattern, third_pattern, fourth_pattern, fifth_pattern, sixth_pattern

from .redis_work import start_redis_database
from kafka import KafkaConsumer
from json import loads
import json
import asyncio
import threading

# Initialize at startup Django
print("Django started")
if Pattern.is_empty(): Pattern.set_default_records()
# start_redis_database()
# print("Redis started")


# Kafka logic
print("Kafka started")


# clear_base()


#def kafka_work():


topic_name = 'TestKafk'
consumer = KafkaConsumer(topic_name,
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                         group_id='group_id',
                         auto_offset_reset='earliest',
                         api_version=(0, 10, 1)
                         )
# print("Запущена функция kafka work")
# for message in consumer:  # message.value == dictionary of transaction
#     print("Kafka work:", message)
#     # Patterns
#
#     df = pd.DataFrame(data={message.value['Id']: message.value['Info']}.items(), columns=['Id', 'Info'])
#     print(df)
#     print(type(df))
#     transaction = df.copy()
#     # print(first_pattern(transaction))
#     print(second_pattern(transaction))
#     print(third_pattern(transaction))
#     finded_patterns = []
#     if fourth_pattern(df):
#         finded_patterns.append(4)
#     if fifth_pattern(df):
#         finded_patterns.append(5)
#     if sixth_pattern(df):
#         finded_patterns.append(6)
#
#     no_fraud = redis.StrictRedis(host="localhost", port=6379, db=0)
#     if len(finded_patterns) == 0:
#         no_fraud.incr("no_fraud")
#     else:
#         no_fraud.incr("fraud")
#     print("End of fucking patterns")
#     Transaction.create_transaction(transaction, message.value['Info'], finded_patterns)


# tr = threading.Thread(target=kafka_work())
# tr.start()
# for message in consumer: # message.value == dictionary of transaction
#     print("Kafka work:", message.value)
#     # Patterns
#     ...
#     Transaction.create_by_dict(Transaction, message.value)


# Views function
def home(request):
    # clear_base()
    json = [{'date': '2020-05-01T00:00:29',
             'card': '59649132026167121328',
             'account': '40817810000001139973',
             'account_valid_to': '2036-01-16T00:00:00',
             'client': '3-95179',
             'last_name': 'Мисик',
             'first_name': 'Сергей',
             'patronymic': 'Николаевич',
             'date_of_birth': '1938-06-25T00:00:00',
             'passport': 7076445954,
             'passport_valid_to': '2022-11-09T00:00:00',
             'phone': '+79497481039',
             'oper_type': 'Пополнение',
             'amount': 31576.6,
             'oper_result': 'Отказ',
             'terminal': 'POS43792',
             'terminal_type': 'POS',
             'city': 'Славянск-на-Кубани',
             'address': 'Славянск-на-Кубани, ул. Клецкая, д. 86'}]
    # Transaction.save_data_from_json(json)
    return render(request, 'home.html')
