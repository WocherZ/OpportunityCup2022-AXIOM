def start_redis_database():
    import redis
    import pandas as pd
    from direct_redis import DirectRedis

    # стартуем df (грузим 1000)
    df = pd.read_json('transactions.json')
    names = df['transactions'].values[0].keys()

    data = []
    for i in range(len(df['transactions'].values)):
        pr = list(df['transactions'].values[i].values())
        data.append(pr)

    table = pd.DataFrame(data=data, columns=names)

    table['date'] = pd.to_datetime(table['date'])
    table['account_valid_to'] = pd.to_datetime(table['account_valid_to'])
    table['date_of_birth'] = pd.to_datetime(table['date_of_birth'])
    table['passport_valid_to'] = pd.to_datetime(table['passport_valid_to'])
    #

    # база для подсчета количества фрода
    fraud_counter = redis.StrictRedis(host="localhost", port=6379, db=0)
    fraud_counter.flushdb()
    for i in range(6):
        fraud_counter.set("counter_" + str(i + 1), 0)

    fraud_counter.set("not_fraud", 0)
    fraud_counter.set("fraud", 0)

    # база для 1 паттерна
    base_by_name = DirectRedis(host="localhost", port=6379, db=1)
    base_by_name.flushdb()

    for i in range(table.shape[0]):
        base_by_name.lpush(
            table.loc[[i], ['last_name', 'first_name', 'patronymic', 'passport']].to_json(orient='records'),
            table.loc[[i], :])

    # база для 2 паттерна
    base_by_name_and_time = DirectRedis(host="localhost", port=6379, db=2)
    base_by_name_and_time.flushdb()

    for i in range(table.shape[0]):
        base_by_name_and_time.lpush(
            table.loc[[i], ['last_name', 'first_name', 'patronymic', 'date']].to_json(orient='records'),
            table.loc[[i], :])

    # база для 3 паттерна
    base_by_name_and_time_city = DirectRedis(host="localhost", port=6379, db=3)
    base_by_name_and_time_city.flushdb()

    for i in range(table.shape[0]):
        base_by_name_and_time_city.lpush(
            table.loc[[i], ['last_name', 'first_name', 'patronymic']].to_json(orient='records'),
            table.loc[[i], :])

    # база для 6 паттерна
    base_by_terminal = DirectRedis(host="localhost", port=6379, db=6)
    base_by_terminal.flushdb()

    for i in range(table.shape[0]):
        base_by_terminal.lpush(table.loc[[i], ['terminal']].to_json(orient='records'), table.loc[[i], :])

