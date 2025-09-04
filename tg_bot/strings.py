# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


from demo_data.models import (
    User,
    Order,
    Cake,
    Promocode,
    Shape,
    Topping,
    Decor,
    Berry
)
from datetime import date, time


# Начало заказа
START_ORDER = (
    '🎂 <b>Добро пожаловать в кондитерскую BakeCake!</b>\n\n'
    '✨ Здесь вы можете заказать вкуснейшие торты на любой праздник!\n'
    '• 🎁 <b>Готовые торты</b> из нашего меню\n'
    '• ✨ <b>Создать свой уникальный торт</b> с помощью конструктора\n'
    '• 🔄 <b>Повторить предыдущий заказ</b>\n\n'
    '🎯 Для начала работы необходимо пройти быструю регистрацию!'
)

# Согласие на обработку персональных данных
PERSONAL_DATA_PROCESSING_CONSENT = (
    '📋 <b>Согласие на обработку персональных данных</b>\n\n'
    'Для оформления заказа нам необходимо ваше согласие на обработку персональных данных.\n\n'
    '🔒 <b>Мы гарантируем:</b>\n'
    '• Конфиденциальность ваших данных\n'
    '• Использование только для обработки заказов\n'
    '• Соответствие требованиям ФЗ-152\n\n'
    '📝 <b>Нажимая «Принять», вы соглашаетесь:</b>\n'
    '• ✅ На сбор и обработку ваших данных\n'
    '• ✅ На получение уведомлений о заказах\n'
    '• ✅ На использование cookies для работы сервиса\n\n'
    '💫 Полную версию соглашения можно скачать по кнопке ниже!'
)

# Регистрация
INPUT_YOUR_NAME = '👤 Введите ваше имя'
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

INPUT_YOUR_PHONE = '📞 Введите телефон'
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

INPUT_YOUR_ADDRESS = '🏠 Введите адрес'
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


INPUT_PROMO = (
    '<b>Ввод промокода</b>\n\n'
    'Если у вас есть промокод, введите его.\n'
)


PROMO_DOES_NOT_EXIST = (
    '❌ <b>Промокод не найден</b>\n\n'
    'Введенный промокод недействителен или уже использован.\n'
    'Попробуйте ввести другой или пропустите этот шаг.'
)


INPUT_COMMENT = (
    '📝 <b>Комментарий к заказу</b>\n\n'
    'Если у вас есть особые пожелания или комментарии к заказу, '
    'напишите их ниже.\n\n'
    'Или нажмите "Пропустить", если комментариев нет.'
)


SELECT_DATE = (
    '📅 <b>Выбор даты доставки</b>\n\n'
    'Пожалуйста, выберите дату доставки из предложенных ниже.'
)


SELECT_TIME = (
    '⏰ <b>Выбор времени доставки</b>\n\n'
    'Выберите удобное время доставки.'
)


ORDER_CREATED = (
    '✅ <b>Заказ создан успешно!</b>\n\n'
    'Ваш заказ успешно оформлен и передан в работу.\n'
    'Скоро с вами свяжется наш менеджер для подтверждения.\n\n'
    'Хотите сделать еще один заказ?'
)


# Торты
CAKES_LIST = '🎂 <b>Наши торты</b>\n\nВыберите понравившийся торт:'


INPUT_SIGN = (
    '✏️ <b>Добавление надписи</b>\n\n'
    'Напишите текст, который должен быть на торте.\n'
    'Или нажмите "Пропустить", если надпись не нужна.\n\n'
    '<i>Надпись добавляет 500 руб. к стоимости торта</i>'
)


CAKE_CREATED = (
    '✅ <b>Торт создан!</b>\n\n'
    'Ваш торт добавлен в корзину.\n'
    'Вы можете продолжить покупки или перейти к оформлению заказа.'
)

def get_confirm_signup(full_name: str, phone: str, address: str):
    text = (
        '📋 <b>Подтверждение регистрации</b>\n\n'
        'Пожалуйста, проверьте введенные данные:\n\n'
        f'👤 <b>Имя:</b> {full_name}\n'
        f'📞 <b>Телефон:</b> {phone}\n'
        f'🏠 <b>Адрес:</b> {address}\n\n'
        'Все верно?'
    )
    return text


def get_signup_complete(full_name: str):
    text = (
        '✅ <b>Регистрация завершена!</b>\n\n'
        f'Пользователь {full_name} успешно зарегистрирован.\n'
        'Теперь вы можете делать заказы!'
    )
    return text


# Главное меню
def get_main_menu(user: User):
    text = (
        '🏠 <b>Главное меню</b>\n\n'
        'Выберите действие:\n'
        '• 🎂 Заказать торт\n'
        '• 📦 Мои заказы\n'
        '• 👤 Профиль\n\n'
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
        text += f'• 🎂 Тортов: {len(order.cakes)}\n'
        text += f'• 📅 Дата доставки: {order.delivery_date.strftime("%d.%m.%Y")}\n'
        text += f'• ⏰ Время: {order.delivery_time.strftime("%H:%M")}\n'
        text += f'• 🏠 Адрес: {order.address}\n'
        text += f'• 📊 Статус: В обработке\n\n'
    
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

    return text


def get_show_cakes(cart: list[int]):
    text = '🎂 <b>Наши торты</b>\n\n'
    if cart:
        text += f'🛒 Тортов в корзине: {len(cart)}'
    text += 'Выберите понравившийся торт:'

    return text


def get_cake_details(cake: Cake):
    text = (
        f'🎂 <b>{cake.title}</b>\n\n'
        f'<b>Цена:</b> {cake.get_price()} руб.\n\n'
    )

    if cake.image:
        text += f'<a href="{cake.image}">🖼 Посмотреть фото</a>\n\n'
    
    text += 'Добавить в корзину?'

    return text


def get_cart_details(cakes: list[Cake]):
    if not cakes:
        text = '🛒 <b>Корзина пуста</b>\n\nДобавьте торты в корзину, чтобы оформить заказ.'
    
    else:
        text = (
        f'🛒 <b>Корзина</b>\n\n'
        f'Позиций в корзине: {len(cakes)}\n\n'
    )

    return text


def get_confirm_create_order(
        cakes: list[Cake],
        delivery_date: date,
        delivery_time: time,
        promocode: Promocode,
        comment: str,
        total_price: int,
        urgent_delivery_price: int | None = None,
        discount_price: int | None = None
):
    text = (
        '✅ <b>Подтверждение заказа</b>\n\n'
        f'Всего позиций: {len(cakes)}\n'
        'Список\n'
    )

    for cake in cakes:
        text += f'{cake.title} – {cake.get_price()} р.\n'

    if delivery_date:
        text += f'Дата: {delivery_date.strftime('%d-%m-%Y')}\n'

    if delivery_time:
        text += f'Время: {delivery_time.strftime('%H:%M')}\n'

    if urgent_delivery_price:
        price_with_delivery = (
            f'<s>{total_price}</s> <b>{urgent_delivery_price}</b>'
        )
        text += (
            f'Наценка за доставку в течение 24 часов: {price_with_delivery}\n'
        )
        total_price = urgent_delivery_price

    if promocode and discount_price:
        text += f'Использован промокод {promocode.title} размер скидки в {promocode.discount}%\n'
        price = f'<s>{total_price}</s> <b>{discount_price}</b>\n'
    else:
        price = f'{total_price}'

    text += f'Цена: {price}\n'

    if comment:
        text += (
            'Комментарий заказчика:\n'
            f'{comment}\n'
        )

    text += 'Создать заказ?'

    return text


def get_custom_cake(
        layers,
        layers_price,
        shape,
        decor,
        berry,
        topping,
        sign
):
    text = (
        '<b>Ваш торт</b>\n\n'
        'Состав вашего торта:\n\n'
    )

    if layers:
        text += f'<b>Количество слоев:</b> {layers} цена: {layers_price} руб.\n'

    if shape:
        text += f'<b>Форма:</b> {shape.title} цена: {shape.price} руб.\n'

    if decor:
        text += f'<b>Декор:</b> {decor.title} цена: {decor.price} руб.\n'

    if berry:
        text += f'<b>Ягоды:</b> {berry.title} цена: {berry.price} руб.\n'

    if topping:
        text += f'<b>Топпинг:</b> {topping.title} цена: {topping.price} руб.\n'

    if sign:
        text += f'<b>Надпись:</b> {sign} цена: 500 руб.\n'

    text += 'Добавить торт в корзину?'

    return text


def get_number_of_layers(layers: dict):
    text = (
        '🍰 <b>Выбор количества коржей</b>\n\n'
        'Выберите количество слоев для вашего торта:\n\n'
    )

    for number, price in layers.items():
        text += f'Слоев: {number} цена: {price}\n'

    return text


def get_shapes(shapes: list[Shape]):
    text = (
        '🔷 <b>Выбор формы торта</b>\n\n'
        'Выберите форму для вашего торта:\n\n'
    )

    for shape in shapes:
        text += f'{shape.title} {shape.price}\n'

    return text


def get_toppings(toppings: list[Topping]):
    text = (
        '🧁 <b>Выбор топпинга</b>\n\n'
        'Выберите топпинг для вашего торта:\n\n'
    )

    for topping in toppings:
        text += f'{topping.title} {topping.price}\n'

    return text


def get_decor(decors: list[Decor]):
    text = (
        '✨ <b>Выбор декора</b>\n\n'
        'Выберите декор для вашего торта:\n\n'
    )

    for decor in decors:
        text += f'{decor.title} {decor.price}\n'

    return text


def get_berries(berries: list[Berry]):
    text = (
        '🍓 <b>Выбор ягод</b>\n\n'
        'Выберите ягоды для вашего торта:\n\n'
    )

    for berry in berries:
        text += f'{berry.title} {berry.price}\n'

    return text


def show_pricelist(
        layers: dict,
        shapes: list[Shape],
        toppings: list[Topping],
        decor: list[Decor],
        berries: list[Berry]
):
    text = '<b>Расценки при покупке торта на заказ:</b>\n\n'

    text += '<b>Количество коржей:</b> \n\n'
    for number, price in layers.items():
        text += f'{number} — <b>{price} руб.</b>\n'

    text += '\n'
    text += show_ingredients('Формы', shapes)
    text += '\n'
    text += show_ingredients('Топпинги', toppings)
    text += '\n'
    text += show_ingredients('Декор', decor)
    text += '\n'
    text += show_ingredients('Ягоды', berries)

    return text
