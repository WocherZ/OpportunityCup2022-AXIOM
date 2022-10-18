# OpportunityCup2022-AXIOM

## Django project - веб-сервер, написанный для обработки транзакций на паттерны фрода.

- Принимает транзакции из Apache Kafka

- Обрабатывает транзакции на основе паттернов

- Логирует все транзакции в PostgreSQL, которая легко масштабируется

- Сохраняет часть транзакций в Redis для быстрого доступа


## Frontend project - сделан на Vue.js, служит для отрисовки диаграмм


## Kafka client - python-скрипт, имитирующий работу клиента, посылающего транзакции

- producer_script - клиент, отправляющий множество операций, находящихся в json

- producer - клиент, отправляющий одну транзакцию
