from demo_data import models
from datetime import datetime
from demo_data.models import (
    Cake,
    Topping,
    Berry,
    Decor,
    Shape,
    Role,
    User,
    Order,
    Promocode
)
from demo_data.utils import (
    find_value_in_dict,
    load_from_json,
    add_to_json,
    find_by_field
)
from os import path
from datetime import date, time


JSON_DIRECTORY = 'demo_data/json/'
USERS = path.join(JSON_DIRECTORY, 'users.json')
ROLES = path.join(JSON_DIRECTORY, 'roles.json')
PROMOCODES = path.join(JSON_DIRECTORY, 'promocodes.json')
TOPPINGS = path.join(JSON_DIRECTORY, 'toppings.json')
BERRIES = path.join(JSON_DIRECTORY, 'berries.json')
DECORS = path.join(JSON_DIRECTORY, 'decors.json')
SHAPES = path.join(JSON_DIRECTORY, 'shapes.json')
CAKES = path.join(JSON_DIRECTORY, 'cakes.json')
ORDERS = path.join(JSON_DIRECTORY, 'orders.json')


def _old_get_toppings():
    return [
        models.Topping(0, 'Без топпинга', 0),
        models.Topping(1, 'Белый соус', 200),
        models.Topping(2, 'Карамельный Сироп', 180),
        models.Topping(3, 'Клубничный Сироп', 300),
    ]


def _old_get_berries():
    return [
        models.Berry(0, 'Ежевика', 400),
        models.Berry(1, 'Малина', 300),
        models.Berry(2, 'Голубика', 450),
    ]


def _old_get_decor():
    return [
        models.Decor(0, 'Фисташки', 300),
        models.Decor(1, 'Безе', 400),
        models.Decor(2, 'Фундук', 350),
    ]


def _old_get_user():
    role = models.Role(1, 'Customer')
    return models.User(
        1,
        '11111111',
        'Иванов Иван Иванович',
        role,
        'ул. Ленина 10',
        '89224355343'
    )


def _old_get_promocodes():
    return [
        models.Promocode(0, 'SUPERCAKE20', True),
        models.Promocode(1, 'NEWYEAR', False),
        models.Promocode(2, 'PROMO10', True),
    ]


def find_user(tg_id: int) -> models.User | None:
    user = find_by_field(USERS, 'tg_id', tg_id)
    if user:
        return parse_user(user)
    return None


def find_promocode(promocode_title: str) -> Promocode | None:
    promocode = find_by_field(PROMOCODES, 'title', promocode_title)
    if promocode:
        return Promocode(
            promocode.get('pk'),
            promocode.get('title'),
            promocode.get('is_active')
        )
    return None


def add_cake(
        title: str,
        price: int | None,
        image: str,
        user: User,
        topping_pk: int,
        shape_pk: int,
        number_of_layers: int | None,
        sign: str | None,
        decor_pks: list[int],
        berry_pks: list[int]
):

    cake = {
        'pk': None,
        'title': title,
        'price': price,
        'image': image,
        'user': user.pk,
        'topping': topping_pk,
        'shape': shape_pk,
        'number_of_layers': number_of_layers,
        'sign': sign,
        'decor': decor_pks,
        'berries': berry_pks
    }

    add_to_json(CAKES, cake)


def add_order(
        user: User,
        cake_pks: list[int],
        address: str,
        delivery_date: date | str,
        delivery_time: time | str,
        promocode: Promocode = None,
        comment: str = ''
):
    if not address:
        address = user.address

    promocode_pk = None

    if promocode:
        promocode_pk = promocode.pk

    order = {
        'pk': None,
        'customer': user.pk,
        'cakes': cake_pks,
        'address': address,
        'delivery_date': delivery_date,
        'delivery_time': delivery_time,
        'promocode': promocode_pk,
        'comment': comment
    }

    add_to_json(ORDERS, order)


#TODO: Удалить значения по умолчанию ближе к концу разработки
def add_customer(
    tg_id: int,
    full_name: str = 'Иван Иванов',
    address: str = 'ул. Ленина 10',
    phone: str = '89001234567'
):
    customer_role_pk = 1

    user = {
        'pk': None,
        'tg_id': tg_id,
        'full_name': full_name,
        'role': customer_role_pk,
        'address': address,
        'phone': phone
    }

    add_to_json(USERS, user)
    return


def delete_user_from_db(tg_id):
    user = find_user(tg_id)
    if user:
        users.remove(user)


def get_role(pk) -> Role:
    role = find_value_in_dict(pk, ROLES)
    return Role(
        role.get('pk'),
        role.get('title')
    )


def get_user(pk) -> User:
    user = find_value_in_dict(pk, USERS)
    return parse_user(user)


def get_promocode(pk) -> Promocode:
    promocode = find_value_in_dict(pk, PROMOCODES)
    return Promocode(
        promocode.get('pk'),
        promocode.get('title'),
        promocode.get('is_active')
    )


def parse_user(user: dict):
    role = get_role(user.get('role'))
    return User(
        user.get('pk'),
        user.get('tg_id'),
        user.get('full_name'),
        role,
        user.get('address'),
        user.get('phone')
    )


def parse_order(order: dict) -> Order:
    customer = get_user(order.get('customer'))
    cake = get_cake(order.get('cake'))
    promocode_id = order.get('promocode')
    promocode = get_promocode(promocode_id) if promocode_id else None

    # Преобразуем дату и время из строк в объекты
    delivery_date = datetime.strptime(order.get('delivery_date'), '%Y-%m-%d').date()
    delivery_time = datetime.strptime(order.get('delivery_time'), '%H:%M').time() if order.get('delivery_time') else None

    return Order(
        order.get('pk'),
        customer,
        [cake],
        order.get('address'),
        delivery_date,
        delivery_time,
        promocode,
        order.get('comment')
    )


def get_order(pk: int) -> Order:
    order = find_value_in_dict(pk, ORDERS)
    return parse_order(order)


def get_orders() -> list[Order]:
    orders_data = load_from_json(ORDERS)
    parsed_orders = []
    for _, order_data in orders_data.items():
        parsed_orders.append(parse_order(order_data))
    return parsed_orders


def get_topping(pk) -> Topping:
    topping = find_value_in_dict(pk, TOPPINGS)
    return Topping(
        topping.get('pk'),
        topping.get('title'),
        topping.get('price')
    )


def get_decor(pk) -> Decor:
    decor = find_value_in_dict(pk, DECORS)
    return Decor(
        decor.get('pk'),
        decor.get('title'),
        decor.get('price')
    )


def get_shape(pk) -> Shape:
    shape = find_value_in_dict(pk, SHAPES)
    return Shape(
        shape.get('pk'),
        shape.get('title'),
        shape.get('price')
    )


def get_berry(pk) -> Berry:
    berry = find_value_in_dict(pk, BERRIES)
    return Berry(
        berry.get('pk'),
        berry.get('title'),
        berry.get('price')
    )


def get_ingredients(get_ingredient: callable, pks: list[int]) -> list:
    ingredients = []
    for pk in pks:
        ingredients.append(get_ingredient(pk))
    return ingredients


def parse_cake(cake: dict) -> Cake:
    # Для типовых тортов некоторые поля могут отсутствовать (быть null)
    # Получаем значения, если они есть
    topping_id = cake.get('topping')
    topping = get_topping(topping_id) if topping_id is not None else None

    shape_id = cake.get('shape')
    shape = get_shape(shape_id) if shape_id is not None else None

    number_of_layers = cake.get('number_of_layers')
    sign = cake.get('sign')

    decor_ids = cake.get('decor', [])
    decors = get_ingredients(get_decor, decor_ids) if decor_ids else []

    berries_ids = cake.get('berries', [])
    berries = get_ingredients(get_berry, berries_ids) if berries_ids else []

    # Получаем цену и изображение, если они есть
    price = cake.get('price')
    image = cake.get('image')

    parsed_cake = Cake(
        cake.get('pk'),
        cake.get('title'),
        price,
        image,
        topping,
        shape,
        number_of_layers,
        sign,
        False,  # custom - по умолчанию False
        decors,
        berries
    )
    
    return parsed_cake


def get_cake(pk: int) -> Cake:
    cake: dict = find_value_in_dict(pk, CAKES)
    return parse_cake(cake)


def get_cakes() -> list[Cake]:
    cakes: dict = load_from_json(CAKES)
    parsed_cakes = []

    for _, cake in cakes.items():
        parsed_cake = parse_cake(cake)
        parsed_cakes. append(parsed_cake)
    return parsed_cakes