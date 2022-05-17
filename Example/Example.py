"""Пример использования модуля. """
import check_qiwi
from random import randint

Check = check_qiwi.Check()
user = randint(1, 999999)
print(Check.create_paylink(amount=49, comment='За вкусный кофе', user=user))
input('Нажмите любую клавишу для проверки оплаты')
if Check.check_pay(user):
    print('Счёт успешно оплачен')
else:
    print('Счёт не был оплачен!')
