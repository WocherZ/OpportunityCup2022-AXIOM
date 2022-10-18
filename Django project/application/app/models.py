from django.db import models

class Pattern(models.Model):
    number = models.IntegerField()
    description = models.CharField(max_length=128)

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = 'Паттерн'
        verbose_name_plural = 'Паттерны'

    def is_empty():
        p = Pattern.objects.all()
        if p.exists():
            return False
        else:
            return True

    def set_default_records():
        default_patters = {
            0: "Не является фродом",
            1: "Много транзакций в короткое время",
            2: "Высокая активность ночью",
            3: "Операции из разных городов",
            4: "Аккаунт был просрочен",
            5: "Паспорт был просрочен",
            6: "Операции с одного терминала из разных городов",
        }
        for key, value in default_patters.items():
            pattern = Pattern.objects.create(number=key, description=value)
            pattern.save()

    def delete_everything():
        Transaction.objects.all().delete()

OPER_TYPE = (
    (1, "Пополнение"),
    (2, "Снятие"),
    (3, "Оплата")
)

OPER_RESULT = (
    (1, "Отказ"),
    (2, "Успешно")
)

TERMINAL_TYPE = (
    (1, "POS"),
    (2, "ATM")
)


class Transaction(models.Model):
    date = models.TextField()
    card = models.TextField()
    account = models.TextField()
    account_valid_to = models.TextField()
    client = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    patronymic = models.TextField()
    date_of_birth = models.TextField()
    passport = models.TextField()
    passport_valid_to = models.TextField()
    phone = models.TextField()
    oper_type = models.CharField(choices=OPER_TYPE, max_length=10)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    oper_result = models.CharField(choices=OPER_RESULT, max_length=7)
    terminal = models.TextField()
    terminal_type = models.CharField(choices=TERMINAL_TYPE, max_length=3)
    city = models.TextField()
    address = models.TextField()

    patterns = models.ManyToManyField(Pattern)

    class Meta:
        verbose_name = 'Тразнакция'
        verbose_name_plural = 'Транзакции'

    def save_data_from_json(json):
        for transaction in json:
            one_transaction = Transaction.objects.create(
                date = transaction.get('date'),
                card = transaction.get('card'),
                account = transaction.get('account'),
                account_valid_to = transaction.get('account_valid_to'),
                client = transaction.get('client'),
                last_name = transaction.get('last_name'),
                first_name = transaction.get('first_name'),
                patronymic = transaction.get('patronymic'),
                date_of_birth = transaction.get('date_of_birth'),
                passport = transaction.get('passport'),
                passport_valid_to = transaction.get('passport_valid_to'),
                phone = transaction.get('phone'),
                oper_type = transaction.get('oper_type'),
                amount = transaction.get('amount'),
                oper_result = transaction.get('oper_result'),
                terminal = transaction.get('terminal'),
                terminal_type = transaction.get('terminal_type'),
                city = transaction.get('city'),
                address = transaction.get('address')
            )
            one_transaction.save()

    def delete_everything():
        Transaction.objects.all().delete()


    def create_by_dict(self, dict):
        one_transaction = Transaction.objects.create(
            date=dict.get('date'),
            card=dict.get('card'),
            account=dict.get('account'),
            account_valid_to=dict.get('account_valid_to'),
            client=dict.get('client'),
            last_name=dict.get('last_name'),
            first_name=dict.get('first_name'),
            patronymic=dict.get('patronymic'),
            date_of_birth=dict.get('date_of_birth'),
            passport=dict.get('passport'),
            passport_valid_to=dict.get('passport_valid_to'),
            phone=dict.get('phone'),
            oper_type=dict.get('oper_type'),
            amount=dict.get('amount'),
            oper_result=dict.get('oper_result'),
            terminal=dict.get('terminal'),
            terminal_type=dict.get('terminal_type'),
            city=dict.get('city'),
            address=dict.get('address')
        )
        one_transaction.patterns.add(Pattern.objects.get(id=1))
        one_transaction.save()

    def create_transaction(self, dict, patterns=[]):
        one_transaction = Transaction.objects.create(
            date=dict.get('date'),
            card=dict.get('card'),
            account=dict.get('account'),
            account_valid_to=dict.get('account_valid_to'),
            client=dict.get('client'),
            last_name=dict.get('last_name'),
            first_name=dict.get('first_name'),
            patronymic=dict.get('patronymic'),
            date_of_birth=dict.get('date_of_birth'),
            passport=dict.get('passport'),
            passport_valid_to=dict.get('passport_valid_to'),
            phone=dict.get('phone'),
            oper_type=dict.get('oper_type'),
            amount=dict.get('amount'),
            oper_result=dict.get('oper_result'),
            terminal=dict.get('terminal'),
            terminal_type=dict.get('terminal_type'),
            city=dict.get('city'),
            address=dict.get('address')
        )
        for pattern in patterns:  # pattern - номер паттерна по таблице
            one_transaction.patterns.add(Pattern.objects.get(id=pattern))
        one_transaction.save()

    def get_last_n_records(self, n):
        result = []
        result
        last_n = Transaction.objects.all().order_by('-id')[0:n][::-1]
        for transaction in last_n:
            # transaction = transaction.first()
            result.append({
                #'date': getattr(transaction,'date'),
                    #transaction.object.values('date'),
                'last_name': getattr(transaction,'last_name'),
                'first_name': getattr(transaction,'first_name'),
                #'patronymic': getattr(transaction,'patronymic'),
                #'passport': getattr(transaction,'passport'),
                #'phone': getattr(transaction,'phone'),
                #'oper_type': getattr(transaction,'oper_type'),
                #'amount': str(getattr(transaction,'amount')),
                #'pattern': "Да" if transaction.patterns else "Нет",
                #'pattern_description': [str(x) for x in transaction.patterns.all()]
            })
        return result

# General methods

def clear_base():
    Pattern.delete_everything()
    Transaction.delete_everything()