from django.shortcuts import render

from .models import Transaction, Pattern, clear_base

from kafka import KafkaConsumer
from json import loads
import json

# Kafka logic
print("Kafka started from service")
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

    df = pd.DataFrame(data={message.value['Id']: message.value['Info']}.items(), columns=['Id', 'Info'])
    print(df)
    print(type(df))
    transaction = df.copy()
    # print(first_pattern(transaction))
    print(second_pattern(transaction))
    print(third_pattern(transaction))
    finded_patterns = []
    if fourth_pattern(df):
        finded_patterns.append(4)
    if fifth_pattern(df):
        finded_patterns.append(5)
    if sixth_pattern(df):
        finded_patterns.append(6)

    no_fraud = redis.StrictRedis(host="localhost", port=6379, db=0)
    if len(finded_patterns) == 0:
        no_fraud.incr("no_fraud")
    else:
        no_fraud.incr("fraud")
    print("End of fucking patterns")
    Transaction.create_transaction(transaction, message.value['Info'], finded_patterns)