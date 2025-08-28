from demo_data import models
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
from demo_data.utils import find_value_in_dict, load_from_json


def get_toppings():
    return [
        models.Topping(0, 'Без топпинга', 0),
        models.Topping(1, 'Белый соус', 200),
        models.Topping(2, 'Карамельный Сироп', 180),
        models.Topping(3, 'Клубничный Сироп', 300),
    ]


def get_berries():
    return [
        models.Berry(0, 'Ежевика', 400),
        models.Berry(1, 'Малина', 300),
        models.Berry(2, 'Голубика', 450),
    ]


def get_decor():
    return [
        models.Decor(0, 'Фисташки', 300),
        models.Decor(1, 'Безе', 400),
        models.Decor(2, 'Фундук', 350),
    ]


def get_user():
    role = models.Role(1, "Customer")
    return models.User(
        1,
        "11111111",
        "Иванов Иван Иванович",
        role,
        "ул. Ленина 10",
        "89224355343"
    )


def get_promocodes():
    return [
        models.Promocode(0, 'SUPERCAKE20', True),
        models.Promocode(1, 'NEWYEAR', False),
        models.Promocode(2, 'PROMO10', True),
    ]


users: list[models.User] = []


def find_user(tg_id: int) -> models.User | None:
    if not users:
        return None

    for user in users:
        if user.tg_id == tg_id:
            return user

    return None


#TODO: Удалить значения по умолчанию ближе к концу разработки
def add_customer(
    tg_id: int,
    full_name: str = 'Иван Иванов',
    address: str = 'ул. Ленина 10',
    phone: str = '89001234567'
):
    role = models.Role(1, 'Customer')
    if not users:
        pk = 0
    else:
        pk = len(users)

    user = models.User(
        pk,
        tg_id,
        full_name,
        role,
        address,
        phone
    )

    if not find_user(tg_id):
        users.append(user)


def delete_user_from_db(tg_id):
    user = find_user(tg_id)
    if user:
        users.remove(user)
        

def get_topping(pk) -> Topping:
    topping = find_value_in_dict(pk, 'demo_data/json/toppings.json')
    return Topping(
        topping.get('pk'),
        topping.get('title'),
        topping.get('price')
    )


def get_decor(pk) -> Decor:
    decor = find_value_in_dict(pk, 'demo_data/json/decors.json')
    return Decor(
        decor.get('pk'),
        decor.get('title'),
        decor.get('price')
    )


def get_shape(pk) -> Shape:
    shape = find_value_in_dict(pk, 'demo_data/json/shapes.json')
    return Shape(
        shape.get('pk'),
        shape.get('title'),
        shape.get('price')
    )


def get_berry(pk) -> Berry:
    berry = find_value_in_dict(pk, 'demo_data/json/berries.json')
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
    topping = get_topping(cake.get('topping'))
    decors = get_ingredients(get_decor, cake.get('decor'))
    berries = get_ingredients(get_berry, cake.get('berries'))
    shape = get_shape(cake.get('shape'))

    parsed_cake = Cake(
        cake.get('pk'),
        cake.get('title'),
        topping,
        shape,
        cake.get('number_of_layers'),
        cake.get('sign'),
        decors,
        berries
    )
    
    return parsed_cake


def get_cake(pk: int) -> Cake:
    cake: dict = find_value_in_dict(pk, 'demo_data/json/cakes.json')
    return parse_cake(cake)


def get_cakes() -> list[Cake]:
    cakes: dict = load_from_json('demo_data/json/cakes.json')
    parsed_cakes = []

    for _, cake in cakes.items():
        parsed_cake = parse_cake(cake)
        parsed_cakes. append(parsed_cake)
    return parsed_cakes