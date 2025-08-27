# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


from demo_data.models import User, Order


# Пример статичного текста
START_ORDER = (
    'Текст начала заказа торта\n'
)


PERSONAL_DATA_PROCESSING_CONSENT = (
    'Короткий текст согласия на обработку персональных данных тут\n'
    'А снизу будет кнопка, по которой можно будет скачать полную версию\n'
    'Еще надо указать, что пользоваться нашим ботом можно только'
    'если принять согласие на обработку персональных данных\n'
    'Но пока что переход в это меню автоматически создает пользователя'
)


INPUT_YOUR_NAME = (
    'Введите ваше имя'
)


FULL_NAME_IS_INCORRECT = (
    'Текст при неверно введеном имени'
)


FULL_NAME_IS_CORRECT = (
    'Текст при правильно введеном имени '
    'и инструкция для следующего шага '
    'с вводом номера телефона'
)


INPUT_YOUR_PHONE = (
    'Введите телефон'
)


PHONE_IS_INCORRECT = (
    'Номер неправильный'
)


PHONE_IS_CORRECT = (
    'Номер правильный '
    'дальше просим ввести адрес'
)


INPUT_YOUR_ADDRESS = (
    'Введите адрес'
)


ADDRESS_IS_INCORRECT = (
    'Адрес неправильный'
)


ADDRESS_IS_CORRECT = (
    'Адрес правильный '
    'дальше подтверждение'
)



def get_main_menu(user: User):
    text = (
        'Текст главного меню\n'
        'В несколько строк\n'
        '<b>С форматированием</b>\n'        
    )

    if user:
        text += f'И именем пользователя: {user.full_name}\n'
        text += f'И id телеграма (только для тестирования): {user.tg_id}\n'

    return text


# Пример текста с условием
def get_my_orders(orders: list[Order]):
    text = 'Ваши заказы\n'

    if orders:
        text += f'Всего заказов: {len(orders)}'
    else:
        text += 'На текущий момент у вас нет заказов'

    return text


# Пример текста с циклом и условием
def show_ingredients(category: str, items: list):
    text = f'<b>{category}:</b>\n'
    if items:
        for item in items:
            text += f'<i>{item.title}</i>  –  <b>{item.price}</b> руб.\n'
        text += '\n'

    return text
