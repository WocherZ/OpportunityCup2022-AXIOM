import pandas as pd
from direct_redis import DirectRedis
import json
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas.io.json import json_normalize
import redis

fraud_counter = redis.StrictRedis(host="localhost", port=6379, db=0)


# 1 Большое количество запросов в течение короткого промежутка времени (более 3-х операций за 15 минут)

def check_transacrtions_first(interval_in_minutes, table):
    second_check_table = table.groupby(by=['last_name', 'first_name', 'patronymic', 'card', 'date'], as_index=False)[
        'account_valid_to'].count()
    second_check_table = second_check_table.drop('account_valid_to', axis=1)
    second_check_table.sort_values(by=['last_name', 'first_name', 'patronymic', 'date'], inplace=True)

    fraud_operations = []
    time_interval = pd.Timedelta(interval_in_minutes, unit='minutes')
    for i in range(len(second_check_table.values) - 1):
        while all(second_check_table.values[i][0:3] == second_check_table.values[i + 1][0:3]) or all(
                second_check_table.values[i][0:3] == second_check_table.values[i - 1][0:3]) and all(
            second_check_table.values[i][0:3] != second_check_table.values[i + 1][0:3]):
            if ((abs(second_check_table.values[i][4] - second_check_table.values[i + 1][4]) < time_interval and all(
                    second_check_table.values[i][0:3] == second_check_table.values[i + 1][0:3])) or
                    (abs(second_check_table.values[i][4] - second_check_table.values[i - 1][4]) < time_interval and all(
                        second_check_table.values[i][0:3] == second_check_table.values[i - 1][0:3]) and all(
                        second_check_table.values[i][0:3] != second_check_table.values[i + 1][0:3]))):
                fraud_operations.append(second_check_table.values[i])
            break

    last_ind = len(second_check_table.values) - 1
    if abs(second_check_table.values[last_ind][4] - second_check_table.values[last_ind - 1][4]) < time_interval and all(
            second_check_table.values[last_ind][0:3] == second_check_table.values[last_ind - 1][0:3]):
        fraud_operations.append(second_check_table.values[last_ind])
    second_pattern = pd.DataFrame(data=fraud_operations,
                                  columns=['last_name', 'first_name', 'patronymic', 'card', 'date'])
    l_n = second_pattern['last_name'].copy()
    f_n = second_pattern['first_name'].copy()
    pat = second_pattern['patronymic'].copy()
    car = second_pattern['card'].copy()
    dat = second_pattern['date'].copy()

    second_res = table.query(
        'last_name in @l_n and first_name in @f_n and patronymic in @pat and card in @car and date in @dat')
    return second_res


def is_first(test_transactions_dataset, all_transactions_dataset):
    is_fraud_list = []
    tab = pd.concat([all_transactions_dataset, test_transactions_dataset])
    for trans_index in range(test_transactions_dataset.shape[0]):
        l_n = test_transactions_dataset.loc[trans_index, 'last_name']
        f_n = test_transactions_dataset.loc[trans_index, 'first_name']
        patr = test_transactions_dataset.loc[trans_index, 'patronymic']
        passp = test_transactions_dataset.loc[trans_index, 'passport']
        table_with_same_transactions = tab.query(
            'last_name in @l_n and first_name in @f_n and patronymic in @patr and passport in @passp')
        if table_with_same_transactions.shape[0] == 1:
            is_fraud = False
        else:
            fraud_check_table = check_transacrtions_first(2, table_with_same_transactions)
            if fraud_check_table.shape[0] == 1:
                is_fraud = False
            else:
                is_fraud = True
        is_fraud_list.append(is_fraud)
    return is_fraud_list


# Функция для форматирования индексов
def formating(val):
    st = str(val)
    st = st[0:9]
    return int(st)


def first_pattern(json_transaction):
    # big = makeDataFrame(big_json)

    names = json_transaction['Info'].values[0].keys()
    data = list()

    for i in range(len(json_transaction['Info'].values)):
        pr = list(json_transaction['Info'].values[i].values())
        data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    base_by_name = DirectRedis(host="localhost", port=6379, db=1)

    first_dataframe = pd.DataFrame(columns=names)
    for transaction in base_by_name.lrange(
            table.loc[[0], ['last_name', 'first_name', 'patronymic', 'passport']].to_json(orient='records'), 0, -1):
        first_dataframe = pd.concat([first_dataframe, transaction])

    sh1 = is_first(table, first_dataframe)[0]

    if sh1:
        fraud_counter.incr("counter_1")

        pattern_file = open("first_pattern.txt", 'a')
        pattern_file.write(json_transaction["Id"].iloc[0] + ", ")
        pattern_file.close()

    return sh1


# 2	Высокая активность пользователей ночью (12:00 - 6:00)

# Функции форматирования даты и времени
def for_time(date):
    return date.time()


def for_date(date):
    return date.date()


def check_transacrtions_second(night_operations_amount, table):
    third_table = table.groupby(by=['last_name', 'first_name', 'patronymic', 'date'], as_index=False)[
        'passport_valid_to'].count()
    third_table = third_table.drop('passport_valid_to', axis=1)
    third_table.sort_values(by=['last_name', 'first_name', 'patronymic', 'date'], inplace=True)
    third_table['time'] = third_table['date'].apply(for_time)
    third_table['dates'] = third_table['date'].apply(for_date)

    start = pd.Timestamp(year=2002, month=7, day=11, hour=0, minute=0, second=0).time()
    finish = pd.Timestamp(year=2002, month=7, day=11, hour=6, minute=0, second=0).time()
    third_table = third_table.query('date.dt.time > @start & date.dt.time < @finish')

    third_res = third_table.groupby(by=['last_name', 'first_name', 'patronymic', 'dates'], as_index=False)[
        'time'].count()
    third_res_last = third_res.loc[third_res['time'] > night_operations_amount]

    third_help = table.copy()
    third_help['only_date'] = third_help['date'].dt.date
    third_help['time'] = third_help['date'].dt.time

    l_n = third_res_last['last_name'].copy()
    f_n = third_res_last['first_name'].copy()
    pat = third_res_last['patronymic'].copy()
    dat = third_res_last['dates'].copy()
    tim = third_help['time'].copy()

    third_finish = third_help.query(
        'last_name in @l_n and first_name in @f_n and patronymic in @pat and only_date in @dat and time in @tim')
    return third_finish


def is_second(test_transactions_dataset, all_transactions_dataset):
    is_fraud_list = []
    tab = pd.concat([all_transactions_dataset, test_transactions_dataset]).drop_duplicates().reset_index(drop=True)
    for trans_index in range(test_transactions_dataset.shape[0]):
        l_n = test_transactions_dataset.loc[trans_index, 'last_name']
        f_n = test_transactions_dataset.loc[trans_index, 'first_name']
        patr = test_transactions_dataset.loc[trans_index, 'patronymic']
        passp = test_transactions_dataset.loc[trans_index, 'passport']
        table_with_same_transactions = tab.query(
            'last_name in @l_n and first_name in @f_n and patronymic in @patr and passport in @passp')
        if table_with_same_transactions.shape[0] == 1:
            is_fraud = False
        else:
            fraud_check_table = check_transacrtions_second(15, table_with_same_transactions)
            if fraud_check_table.shape[0] == 0:
                is_fraud = False
            else:
                is_fraud = True
        is_fraud_list.append(is_fraud)
    return is_fraud_list


def second_pattern(json_transaction):
    names = json_transaction['Info'].values[0].keys()
    data = list()

    for i in range(len(json_transaction['Info'].values)):
        pr = list(json_transaction['Info'].values[i].values())
        data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    base_by_name_and_time = DirectRedis(host="localhost", port=6379, db=3)

    table['date'] = pd.to_datetime(table['date'])
    table['account_valid_to'] = pd.to_datetime(table['account_valid_to'])
    table['date_of_birth'] = pd.to_datetime(table['date_of_birth'])
    table['passport_valid_to'] = pd.to_datetime(table['passport_valid_to'])

    first_dataframe = pd.DataFrame(columns=names)
    for transaction in base_by_name_and_time.lrange(
            table.loc[[0], ['last_name', 'first_name', 'patronymic']].to_json(orient='records'), 0, -1):
        first_dataframe = pd.concat([first_dataframe, transaction])

    sh2 = is_second(table, first_dataframe)[0]

    if sh2:
        fraud_counter.incr("counter_2")

        pattern_file = open("second_pattern.txt", 'a')
        pattern_file.write(json_transaction["Id"].iloc[0] + ", ")
        pattern_file.close()

    return sh2


# 3	Пользователь совершает операции из разных городов с одного и того же банковского счёта с интервалом менее часа с момента последней операции

def check_transacrtions_third(interval_in_hours, table):
    prom = table.groupby(by=['last_name', 'first_name', 'patronymic'], as_index=False)['city'].count()
    prom = prom.loc[prom['city'] >= 2]

    l_name = prom['last_name'].copy()
    f_name = prom['first_name'].copy()
    patr = prom['patronymic'].copy()

    users_from_some_cities = table.query('last_name in @l_name and first_name in @f_name and patronymic in @patr')
    m = users_from_some_cities.groupby(by=['last_name', 'first_name', 'patronymic', 'city', 'card', 'date'],
                                       as_index=False)['card'].count()
    m.sort_values(by=['last_name', 'first_name', 'patronymic', 'date'], inplace=True)

    time_interval = pd.Timedelta(interval_in_hours, unit='hours')
    fraud_names = []
    for i in range(len(m.values) - 1):
        while all(m.values[i][0:3] == m.values[i + 1][0:3]) or all(m.values[i][0:3] == m.values[i - 1][0:3]) and all(
                m.values[i][0:3] != m.values[i + 1][0:3]):  ####
            if (m.values[i][3] != m.values[i + 1][3] and
                abs(m.values[i][4] - m.values[i + 1][4]) < time_interval) and all(
                m.values[i][0:3] == m.values[i + 1][0:3]):  # если что поправать второе условие
                fraud_names.append(m.values[i][0:5])
            elif i > 0 and ((m.values[i][3] != m.values[i - 1][3] and abs(
                    m.values[i][4] - m.values[i - 1][4]) < time_interval)) and all(
                m.values[i][0:3] == m.values[i - 1][0:3]) and all(m.values[i][0:3] != m.values[i + 1][0:3]):
                fraud_names.append(m.values[i][0:5])
            break

    last_ind = len(m.values) - 1

    if (all(m.values[last_ind][0:3] == m.values[last_ind - 1][0:3]) and
            m.values[last_ind][3] != m.values[last_ind - 1][3] and abs(
                m.values[last_ind][4] - m.values[last_ind - 1][4]) < time_interval):
        fraud_names.append(m.values[last_ind][0:5])

    first_pattern = pd.DataFrame(data=fraud_names, columns=['last_name', 'first_name', 'patronymic', 'city', 'date'])
    l_n = first_pattern['last_name'].copy()
    f_n = first_pattern['first_name'].copy()
    pat = first_pattern['patronymic'].copy()
    cit = first_pattern['city'].copy()
    dat = first_pattern['date'].copy()

    first_res = table.query(
        'last_name in @l_n and first_name in @f_n and patronymic in @pat and city in @cit and date in @dat')

    return first_res


def is_third(test_transactions_dataset, all_transactions_dataset):
    is_fraud_list = []
    tab = pd.concat([all_transactions_dataset, test_transactions_dataset]).drop_duplicates().reset_index(drop=True)
    for trans_index in range(test_transactions_dataset.shape[0]):
        l_n = test_transactions_dataset.loc[trans_index, 'last_name']
        f_n = test_transactions_dataset.loc[trans_index, 'first_name']
        patr = test_transactions_dataset.loc[trans_index, 'patronymic']
        passp = test_transactions_dataset.loc[trans_index, 'passport']
        table_with_same_transactions = tab.query(
            'last_name in @l_n and first_name in @f_n and patronymic in @patr and passport in @passp')
        if table_with_same_transactions.shape[0] == 1:
            is_fraud = False
        else:
            fraud_check_table = check_transacrtions_third(0.5, table_with_same_transactions)
            if fraud_check_table.shape[0] == 0:
                is_fraud = False
            else:
                is_fraud = True
        is_fraud_list.append(is_fraud)
    return is_fraud_list


def third_pattern(json_transaction):
    names = json_transaction['Info'].values[0].keys()
    data = list()

    for i in range(len(json_transaction['Info'].values)):
        pr = list(json_transaction['Info'].values[i].values())
        data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    base_by_name_and_time_city = DirectRedis(host="localhost", port=6379, db=3)

    table['date'] = pd.to_datetime(table['date'])
    table['account_valid_to'] = pd.to_datetime(table['account_valid_to'])
    table['date_of_birth'] = pd.to_datetime(table['date_of_birth'])
    table['passport_valid_to'] = pd.to_datetime(table['passport_valid_to'])

    third_dataframe = pd.DataFrame(columns=names)
    for transaction in base_by_name_and_time_city.lrange(
            table.loc[[0], ['last_name', 'first_name', 'patronymic']].to_json(orient='records'), 0, -1):
        third_dataframe = pd.concat([third_dataframe, transaction.reset_index(drop=True)])

    sh3 = is_third(table, third_dataframe)[0]

    if sh3:
        fraud_counter.incr("counter_3")

        pattern_file = open("third_pattern.txt", 'a')
        pattern_file.write(json_transaction["Id"].iloc[0] + ", ")
        pattern_file.close()

    return sh3


# 4	Промежуток времени с того момента, как аккаунт утратил актуальность превышает десять лет

def fourth_pattern(df):
    names = df['Info'].values[0].keys()

    data = []
    pr = list(df['Info'].values[0].values())
    data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    pr = table.values[0].tolist()
    transaction_date = datetime.strptime(pr[0], '%Y-%m-%dT%H:%M:%S')
    try:
        account_valid_date = datetime.strptime(pr[3], '%Y-%m-%dT%H:%M:%S')
    except:
        account_valid_date = datetime.strptime(pr[3], '%Y-%m-%d')
    if account_valid_date < transaction_date:

        fraud_counter.incr("counter_4")

        pattern_file = open('forth_pattern.txt', 'a')
        pattern_file.write(df['Id'].iloc[0] + ", ")
        pattern_file.close()
        return True
    else:
        return False


# 5	Разность между датой рождения и датой утраты паспортом актуальности меньше четырнадцати лет

def fifth_pattern(df):
    names = df['Info'].values[0].keys()

    data = []
    pr = list(df['Info'].values[0].values())
    data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    pr = table.values[0].tolist()
    transaction_date = datetime.strptime(pr[0], '%Y-%m-%dT%H:%M:%S')
    try:
        passport_valid_date = datetime.strptime(pr[10], '%Y-%m-%dT%H:%M:%S')
    except:
        passport_valid_date = datetime.strptime(pr[10], '%Y-%m-%d')
    if passport_valid_date < transaction_date:

        fraud_counter.incr("counter_5")

        pattern_file = open('fifth_pattern.txt', 'a')
        pattern_file.write(df['Id'].iloc[0] + ", ")
        pattern_file.close()
        return True
    else:
        return False


# 6	Большое количество транзакций (около 700) и значительное количество адресов в сравнении с остальными терминалами для аппаратов POS43792, POS75616, POS28311

def sixth_pattern(input_df):
    names = input_df['Info'].values[0].keys()

    data = []
    pr = list(input_df['Info'].values[0].values())
    data.append(pr)
    table = pd.DataFrame(data=data, columns=names)

    base_by_terminal = DirectRedis(host="localhost", port=6379, db=6)

    df = pd.concat([table, base_by_terminal.lrange(table.loc[[0], ['terminal']].to_json(orient='records'), 0, 0)[0]])

    pr1 = df.values[0].tolist()
    pr2 = df.values[1].tolist()

    transaction_date1 = datetime.strptime(pr1[0], '%Y-%m-%dT%H:%M:%S')
    transaction_date2 = pr2[0]

    if transaction_date2 - relativedelta(hours=1) < transaction_date1 and pr1[18] != pr2[18]:

        fraud_counter.incr("counter_6")

        pattern_file = open('sixth_pattern.txt', 'a')
        pattern_file.write(input_df['Id'][0] + ", ")
        pattern_file.close()

        return True
    else:
        return False
