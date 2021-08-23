"""Пример использования модуля. """
import check_qiwi
from random import randint

secret_key = <MY_SECRET_KEY_FROM_p2p.qiwi.com>
public_key = <MY_PUBLIC_KEY_FROM_p2p.qiwi.com>

Check = check_qiwi.Check(public_key, secret_key)
user = randint(100000, 999999)
print(Check.create_paylink(amount=49, comment='За вкусный кофе', user=user))
input('Нажмите любую клавишу для проверки оплаты')
if Check.check_pay(user):
    print('Счёт успешно оплачен')
else:
    print('Счёт не был оплачен!')
