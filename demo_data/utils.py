import json
from demo_data.models import Order
from utils import is_within_24_hours
from tg_bot.settings import DELIVERY_WITHIN_24H_SURCHARGE


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


def delete_from_json(json_filepath, pk):
    """Удаляет запись по первичному ключу из JSON-файла."""
    data = load_from_json(json_filepath)
    
    # Проверяем, существует ли запись с таким PK
    if str(pk) not in data:
        return False
    
    # Удаляем запись
    del data[str(pk)]
    
    # Сохраняем обновленные данные
    save_readable_json(data, json_filepath)
    return True


def calculate_order_total_price(order: Order) -> int:
    """Рассчитывает общую стоимость заказа с учетом:
    - стоимости всех тортов
    - срочной доставки (если менее 24 часов)
    - примененных промокодов
    """
    # Суммируем стоимость всех тортов в заказе
    total = sum(cake.get_price() for cake in order.cakes)

    # Проверяем, является ли доставка срочной
    if is_within_24_hours(order.delivery_date, order.delivery_time):
        total = total * (1 + DELIVERY_WITHIN_24H_SURCHARGE / 100)

    # Применяем скидку по промокоду
    if order.promocode and order.promocode.is_active:
        total = total  * (1 - order.promocode.discount / 100)

    return total
