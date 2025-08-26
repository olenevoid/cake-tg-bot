from demo_data import models


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


def add_user(tg_id: int):
    role = models.Role(1, "Customer")
    if not users:
        pk = 0
    else:
        pk = len(users)

    user = models.User(
        pk,
        tg_id,
        "Иванов Иван Иванович",
        role,
        "ул. Ленина 10",
        "89224355343"
    )

    if not find_user(tg_id):
        users.append(user)


def delete_user_from_db(tg_id):
    user = find_user(tg_id)
    if user:
        users.remove(user)