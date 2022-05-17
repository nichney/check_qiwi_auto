"""
Модуль для выставления счетов и их автоматической проверки через QiwiAPI.
Ключи доступа можно получить на p2p.qiwi.com
"""
import sqlite3
import requests
from uuid import uuid4


class Check():

    def __init__(self):
        """Для авторизации нужно указать publicKey и secretKey, созданные заранее на p2p.qiwi.com"""
        f = open("config.txt")
        f = f.read().split("\n")
        self.publicKey = f[0]
        self.secret_key = f[1]

    def __generate_billid(self, user):
        result = str(uuid4())
        con = sqlite3.connect('bill_ids.sqlite3')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Users (user INTEGER UNIQUE, bill TEXT)')
        cur.execute('INSERT OR IGNORE INTO Users values(?, ?)', (user, result))
        con.commit()
        return result

    def create_paylink(self, amount, user, comment=' '):
        """Возвращает ссылку на оплату.
        Принимает стоимость счёта в рублях(amount),
                  комментарий для счёта(comment),
                  уникальный номер пользователя, который должен оплатить счёт. Генерируется на вашей стороне."""
        return f'https://oplata.qiwi.com/create?publicKey={self.publicKey}&amount={amount}&billId={self.__generate_billid(user)}&comment={comment}'

    def check_pay(self, user):
        """
        Проверка платежа по id пользователя, который вы указали при создании ссылки.
        Возвращает True, если счёт оплачен, и False, если не оплачен.
        """
        con = sqlite3.connect('bill_ids.sqlite3')
        cur = con.cursor()
        bill = cur.execute('SELECT bill FROM Users WHERE user = (?)', (user,)).fetchone()[0]
        r = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{bill}',
                         headers={'accept': 'application/json', 'Authorization': f'Bearer {self.secret_key}'})
        if r.json()['status']['value'] == 'PAID':
            cur.execute(f'DELETE FROM Users WHERE user = {user}')
            con.commit()
            return True
        else:
            return False


class Wallet():

    def __init__(self, login, token):
        self.login = login
        self.token = token

    def get_profile(self):
        """Возвращает информацию о профиле Qiwi кошелька в формате json."""
        return requests.get('https://edge.qiwi.com/person-profile/v1/profile/current',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {self.token}'}
                            ).json()

    def history_payment(self, number=1, operation='ALL'):
        """Возвращает историю платежей, опционально можно задать number(кол-во платежей) и
        operation, которое может принимать значения в формате строки:
        ALL - все операции,
        IN - только пополнения,
        OUT - только платежи,
        QIWI_CARD - только платежи по картам QIWI (QVC, QVP).
        """
        return requests.get(f'https://edge.qiwi.com/payment-history/v2/persons/{self.login}/payments',
                         headers={'accept': 'application/json', 'Authorization': f'Bearer {self.token}'},
                         params={'rows': number,
                                 'operation': operation,
                                 }).json()['data']
