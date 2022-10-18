import json
from kafka import KafkaProducer

file = open("transactions_final.json")
json_data = json.load(file)
transactions = json_data.get('transactions')
if transactions:
    print("File was open")

keys = json_data.get('transactions').keys()


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8'),
    api_version=(0, 10, 1)
)
topic_name = 'Test'
# record_data = producer.send(
#     topic_name,
#     dict_data
# )

for key in keys:
    print(key, )
    producer.send(
        topic_name,
        value={
            key: transactions.get(key)
        }

    )

print("Sended")