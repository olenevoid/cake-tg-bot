import json
from datetime import datetime, timedelta


def save_readable_json(dictionary, filepath):
    """Сохраняет словарь в читаемом JSON-формате."""
    json_string = json.dumps(dictionary, indent=4, ensure_ascii=False)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json_string)


def load_from_json(filepath):
    """Загружает данные из JSON-файла."""
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()
        return json.loads(data)


def find_value_in_dict(pk, json_filepath):
    """Находит значение по первичному ключу в JSON-файле."""
    dictionary = load_from_json(json_filepath)
    return dictionary.get(str(pk))


def find_by_field(json_filepath, field, value):
    """Ищет запись по значению конкретного поля в JSON-файле."""
    data = load_from_json(json_filepath)
    for item in data.values():
        if item.get(field) == value:
            return item
    return None


def add_to_json(json_filepath, new_data):
    """Добавляет новую запись в JSON-файл с автоматической генерацией PK."""
    data = load_from_json(json_filepath)
    new_pk = max(map(int, data.keys())) + 1 if data else 1
    new_data['pk'] = new_pk
    data[str(new_pk)] = new_data
    save_readable_json(data, json_filepath)
    return new_data


def calculate_order_total_price(order: 'Order') -> int:
    """Рассчитывает общую стоимость заказа с учетом:
    - стоимости всех тортов
    - срочной доставки (если менее 24 часов)
    - примененных промокодов
    """
    # Суммируем стоимость всех тортов в заказе
    total = sum(cake.get_price() for cake in order.cakes)

    # Проверяем, является ли доставка срочной
    if order.delivery_time:
        delivery_datetime = datetime.combine(
            order.delivery_date, 
            order.delivery_time
        )
        time_until_delivery = delivery_datetime - datetime.now()

        # Если доставка в течение 24 часов, добавляем наценку 20%
        if time_until_delivery <= timedelta(hours=24):
            total *= 1.2

    # Применяем скидку по промокоду
    if order.promocode and order.promocode.is_active:
        if order.promocode.title == "ПЕРВЫЙ ЗАКАЗ":
            total *= 0.9  # 10% скидка
        elif order.promocode.title == "ДЕНЬ РОЖДЕНИЯ":
            total *= 0.85  # 15% скидка

    return round(total)
