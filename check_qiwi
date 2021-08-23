"""
Модуль для выставления счетов и их автоматической проверки через QiwiAPI.
Ключи доступа можно получить на p2p.qiwi.com
"""
import sqlite3
import requests
from random import choice


class Check():

    def __init__(self, publicKey, secret_key):
        """Для авторизации нужно указать publicKey и secretKey, созданные заранее на p2p.qiwi.com"""
        self.publicKey = publicKey
        self.secret_key = secret_key

    def __generate_billid(self, user):
        library = list()
        for i in range(0, 26):
            character = ord('a')
            library.append(chr(character + i))
        result = ''
        for i in range(0, 30):
            result += choice(library)
        con = sqlite3.connect('bill_ids.sqlite3')
        cur = con.cursor()
        cur.execute('create table if not exists Users (user INTEGER UNIQUE, bill TEXT)')
        cur.execute('insert or ignore into Users values(?, ?)', (user, result))
        con.commit()
        cur.close()
        con.close()
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
        bill = cur.execute('SELECT bill FROM Users WHERE user = (?)', (user,)).fetchall()[0][0]
        r = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{bill}',
                         headers={'accept': 'application/json', 'Authorization': f'Bearer {self.secret_key}'})
        if r.json()['status']['value'] == 'PAID':
            cur.execute(f'DELETE FROM Users WHERE user = {user}')
            con.commit()
            cur.close()
            con.close()
            return True
        else:
            cur.close()
            con.close()
            return False
