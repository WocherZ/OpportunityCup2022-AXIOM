from django.shortcuts import render
from django.http import HttpResponse

from .models import Transaction, Pattern, clear_base

from kafka import KafkaConsumer
from json import loads
import json


# Kafka logic
print("Kafka started")
clear_base()
topic_name = 'TestKafka'
consumer = KafkaConsumer(topic_name,
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                         group_id='group_id',
                         auto_offset_reset='earliest',
                         api_version=(0, 10, 1)
                         )

for message in consumer:
    print("Kafka work:", message.value)
    # Patterns
    Transaction.create_by_dict(Transaction, message.value)










# Views function
def home(request):
    clear_base()
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
    print(Pattern.is_empty())
    if Pattern.is_empty(): Pattern.set_default_records()
    return render(request, 'home.html')

def Mock(request):
    return HttpResponse("trap")
