# check_qiwi_auto
Не работает в 2025 году

Python-обёртка для работы с Qiwi API, включающая:
 - Создание и отслеживание счетов через Qiwi API
 - Проверку платежей в SQLite
 - Сокращение ссылок с помощью API
# Создание ключей доступа
Перед работой с модулем необходимо создать публичный и секретный ключи доступа.
Для этого переходим на p2p.qiwi.com, авторизумся и переходим к вкладке "Прием переводов -> API".
Затем нажимаем "Создать пару ключей и настроить" и сохраняем оба ключа.

![param](https://sun9-43.userapi.com/impg/LfY6qRfXaqG4D4jHg28WfIkuBhlVgCoy1N-TaQ/esWtXgZktLU.jpg?size=582x482&quality=96&sign=cbecbb4ea26c627d39ab9e0fa4afdbef&type=album)

После этого в папке с проектом необходимо создать файл ```config.txt```, и в первую его строчку вставить Public Key, а во вторую Secret Key.

# Список методов и классов

Class Check(): Класс для выставления счетов и проверки их оплаты;

     __init__(hmKey = 0): hmKey - опциональный строковый(внешность обманчива) параметр, который следует передавать, только если вы собираетесь использовать встроенный сократитель ссылок;

     create_paylink(amount, user, comment=' '): Возвращает полную ссылку на оплату, обязательные параметры amount: int, user: int и опциональный comment,
                                                user - идентификатор счёта, должен быть разным для всех пользователей, у которых одновременно не оплачен счёт;

     create_short_paylink(amount, user, comment=' '): то же, что и предыдущая функция, но возвращает ссылку, сокращенную через hm.ru;

     check_pay(user): Функция, котрая проверяет, оплачен ли счёт с идентификатором user. Возвращает True, если оплачен, и False в ином случае;


class Wallet(): Класс для просмотра своего Qiwi-профиля. Разработка класса еще не закончена;

     __init__(login: str, token: str): login - логин от аккаунта Qiwi, token - токен вашего аккаунта Qiwi;

     get_profile(): Возвращает всю информацию о профиле в JSON формате;

     history_payment(number=1, operation='ALL'): Возвращает информацию о number последних платежах в формате JSON. 
                                                 operation может принимать значения в формате строки:
                                                    ALL - все операции,
                                                    IN - только пополнения,
                                                    OUT - только платежи,
                                                    QIWI_CARD - только платежи по картам QIWI (QVC, QVP).
