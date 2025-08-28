# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


from demo_data.models import User, Order


# Начало заказа
START_ORDER = (
    '🎂 <b>Добро пожаловать в кондитерскую BakeCake!</b>\n\n'
    'Здесь вы можете:\n'
    '• Заказать стандартный торт из нашего меню\n'
    '• Создать свой уникальный торт с помощью конструктора\n'
    '• Повторить предыдущий заказ\n\n'
    'Для начала работы необходимо пройти регистрацию.'
)

# Согласие на обработку персональных данных
PERSONAL_DATA_PROCESSING_CONSENT = (
    '<b>Согласие на обработку персональных данных</b>\n\n'
    'Для оформления заказа нам необходимо ваше согласие на обработку персональных данных.\n\n'
    'Мы обрабатываем ваши данные (имя, телефон, адрес) исключительно для:\n'
    '• Связи с вами по вопросам заказа\n'
    '• Организации доставки\n'
    '• Информирования о статусе заказа\n\n'
    'Нажимая «Принять», вы соглашаетесь:\n\n'
    '• Сбор и обработка ваших данных в соответствии с ФЗ-152\n'
    '• Получение уведомлений о статусе заказов\n'
    '• Использование cookies для работы сервиса\n\n'
    'Без принятия соглашения использование бота невозможно!'
    'Полную версию соглашения можно скачать по кнопке ниже.'
)

# Регистрация
INPUT_YOUR_NAME = 'Введите ваше имя'
FULL_NAME_IS_INCORRECT = (
    "❌ <b>Неверный формат имени!</b>\n\n"
    "Пожалуйста, введите имя и фамилию через пробел\n"
    "Например: <i>Иван Иванов</i>"
)
FULL_NAME_IS_CORRECT = (
    "✅ <b>Имя принято!</b>\n\n"
    "Отлично, {name}! Теперь введите ваш телефон в формате:\n"
    "<code>+7XXXYYYZZZZ</code> или <code>8XXXYYYZZZZ</code>"
)

INPUT_YOUR_PHONE = 'Введите телефон'
PHONE_IS_INCORRECT = (
    "❌ <b>Неверный формат телефона!</b>\n\n"
    "Пожалуйста, введите номер в формате:\n"
    "+7XXXXXXXXXX или 8XXXXXXXXXX\n"
    "Например: <i>+79161234567</i>"
)
PHONE_IS_CORRECT = (
    "✅ <b>Телефон подтверждён!</b>\n\n"
    "Теперь укажите адрес доставки в формате:\n"
    "<i>ул. Название, д. Номер, кв. Номер</i>"
)

INPUT_YOUR_ADDRESS = 'Введите адрес'
ADDRESS_IS_INCORRECT = (
    "❌ <b>Неверный формат адреса!</b>\n\n"
    "Пожалуйста, укажите полный адрес с номером дома\n"
    "Например: <i>ул. Ленина, д. 15, кв. 42</i>"
)
ADDRESS_IS_CORRECT = (
    "✅ <b>Адрес принят!</b>\n\n"
    "Все данные введены корректно. "
    "Проверьте информацию перед подтверждением регистрации."
)

# Торты
CAKES_LIST = '🎂 <b>Наши торты</b>\n\nВыберите понравившийся торт:'


def get_confirm_signup(full_name: str, phone: str, address: str):
    text = (
        f'{full_name}\n'
        f'{phone}\n'
        f'{address}\n'
        'Подтверждаете регистрацию?'
    )
    return text

def get_signup_complete(full_name: str):
    text = f'Пользователь {full_name} зарегистрирован'
    return text


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
)


def get_confirm_signup(full_name: str, phone: str, address: str):
    text = (
        f'{full_name}\n'
        f'{phone}\n'
        f'{address}\n'
        'Подтверждаете регистрацию?'
    )

    return text


def get_signup_complete(full_name: str):
    text = (
        f'Пользователь {full_name} зарегистрирован'
    )

    return text


# Главное меню
def get_main_menu(user: User):
    text = (
        '🏠 <b>Главное меню</b>\n\n'
        '• Заказать торт\n'
        '• Мои заказы\n'
        '• Профиль\n'
    )

    if user:
        text += f'<i>Пользователь:</i> <b>{user.full_name}</b>\n'
        text += f'<i>Телефон:</i> <b>{user.phone}</b>\n\n'
        text += 'Что бы вы хотели сделать?'

    return text


# Список заказов пользователя
def get_my_orders(orders: list[Order]):
    if not orders:
        return (
            '📦 <b>Ваши заказы</b>\n\n'
            'У вас пока нет заказов.\n\n'
            'Хотите создать свой первый торт?'
        )
    
    text = '📦 <b>Ваши заказы</b>\n\n'
    text += f'Всего заказов: {len(orders)}\n\n'

    for i, order in enumerate(orders, 1):
        text += f'<b>Заказ #{i}</b>\n'
        text += f'• Торт: {order.cake.title}\n'
        text += f'• Дата доставки: {order.delivery_date.strftime("%d.%m.%Y")}\n'
        text += f'• Время: {order.delivery_time.strftime("%H:%M")}\n'
        text += f'• Адрес: {order.address}\n'
        text += f'• Статус: В обработке\n\n'
    
    text += 'Выберите заказ для просмотра деталей или создания похожего.'
    
    return text


# Показ ингредиентов
def show_ingredients(category: str, items: list):
    text = f'<b>{category}:</b>\n\n'
    
    if not items:
        text += 'Нет доступных вариантов.\n'
        return text
    
    for item in items:
        text += f'• {item.title}'
        if hasattr(item, 'price') and item.price:
            text += f' — <b>{item.price} руб.</b>'
        text += '\n'
    
    text += '\nВыберите вариант или несколько (если возможно):'
    
    return text
