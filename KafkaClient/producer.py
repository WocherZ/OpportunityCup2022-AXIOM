import json

# dict_data = {'Id': '21412421',
#              'Info': {'date': '2020-05-01T00:00:29',
#          'card': '59649132026167121328',
#          'account': '40817810000001139973',
#          'account_valid_to': '2036-01-16T00:00:00',
#          'client': '3-95179',
#          'last_name': 'Мисик',
#          'first_name': 'Сергей',
#          'patronymic': 'Николаевич',
#          'date_of_birth': '1938-06-25T00:00:00',
#          'passport': 7076445954,
#          'passport_valid_to': '2022-11-09T00:00:00',
#          'phone': '+79497481039',
#          'oper_type': 'Пополнение',
#          'amount': 31576.6,
#          'oper_result': 'Отказ',
#          'terminal': 'POS43792',
#          'terminal_type': 'POS',
#          'city': 'Славянск-на-Кубани',
#          'address': 'Славянск-на-Кубани, ул. Клецкая, д. 86'}
#
# }

dict_data = {"3649235840": {
			"date": "2020-05-04T00:00:04",
			"card": "50785425162189603667",
			"account": "7456771640",
			"account_valid_to": "2026-03-06",
			"client": "6-33721",
			"last_name": "\u041a\u0430\u0434\u0438\u043c\u043e\u0432",
			"first_name": "\u041a\u043e\u0440\u043d\u0435\u043b\u0438\u0443\u0441",
			"patronymic": "\u041a\u043e\u0432\u0430\u043b\u044c\u043a\u043e",
			"date_of_birth": "1993-09-17",
			"passport": "2300733597",
			"passport_valid_to": "2027-12-11",
			"phone": "+74304126656",
			"oper_type": "\u041e\u043f\u043b\u0430\u0442\u0430",
			"amount": 6734.1,
			"oper_result": "\u0423\u0441\u043f\u0435\u0448\u043d\u043e",
			"terminal": "POS43792",
			"terminal_type": "POS",
			"city": "\u041d\u0438\u0436\u043d\u0438\u0439 \u041d\u043e\u0432\u0433\u043e\u0440\u043e\u0434",
			"address": "\u041d\u0438\u0436\u043d\u0438\u0439 \u041d\u043e\u0432\u0433\u043e\u0440\u043e\u0434, \u0443\u043b. \u041a\u043e\u0440\u043e\u043b\u0435\u043d\u043a\u043e\u0432\u0441\u043a\u0430\u044f, \u0434. 5"
		}}

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(0, 10, 1)
)
topic_name = 'Test'

# print(producer.bootstrap_connected())

record_data = producer.send(
    topic_name,
    value=dict_data
)

print(dict_data)
producer.flush()
print(record_data)
print("Sended")
