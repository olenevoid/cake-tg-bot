import json
from pathlib import Path


def create_test_json_files():
    base_dir = Path(__file__).parent
    json_dir = base_dir / "json"
    json_dir.mkdir(exist_ok=True)
    
    test_data = {
        "berries.json": {
            "1": {"pk": 1, "title": "Ежевика", "price": 400},
            "2": {"pk": 2, "title": "Малина", "price": 300},
            "3": {"pk": 3, "title": "Голубика", "price": 450},
            "4": {"pk": 4, "title": "Клубника", "price": 500}
        },
        "cakes.json": {
            "1": {
                "pk": 1,
                "title": "Ягодный торт Марии",
                "price": 2500,
                "image": "static/images/berry_cake.jpg",
                "user": 2,
                "topping": 5,
                "shape": 1,
                "number_of_layers": 2,
                "sign": "С днем рождения!",
                "decor": [2, 5],
                "berries": [2, 4],
                "custom": False
            },
            "2": {
                "pk": 2,
                "title": "Шоколадный торт Ивана",
                "price": 2200,
                "image": "static/images/chocolate_cake.jpg",
                "user": 1,
                "topping": 7,
                "shape": 2,
                "number_of_layers": 1,
                "sign": "",
                "decor": [3],
                "berries": [],
                "custom": False
            },
            "3": {
                "pk": 3,
                "title": "Красный бархат",
                "price": 2000,
                "image": "static/images/red_velvet.jpg",
                "user": None,
                "topping": None,
                "shape": None,
                "number_of_layers": None,
                "sign": None,
                "decor": [],
                "berries": [],
                "custom": False
            },
            "4": {
                "pk": 4,
                "title": "Медовик",
                "price": 2300,
                "image": "static/images/medovik.jpg",
                "user": None,
                "topping": None,
                "shape": None,
                "number_of_layers": None,
                "sign": None,
                "decor": [],
                "berries": [],
                "custom": False
            },
            "5": {
                "pk": 5,
                "title": "Чизкейк Нью-Йорк",
                "price": 2700,
                "image": "static/images/cheesecake.jpg",
                "user": None,
                "topping": None,
                "shape": None,
                "number_of_layers": None,
                "sign": None,
                "decor": [],
                "berries": [],
                "custom": False
            },
            "6": {
                "pk": 6,
                "title": "Фруктовый рай",
                "price": 2600,
                "image": "static/images/fruit_cake.jpg",
                "user": None,
                "topping": None,
                "shape": None,
                "number_of_layers": None,
                "sign": None,
                "decor": [],
                "berries": [],
                "custom": False
            }
        },
        "decors.json": {
            "1": {"pk": 1, "title": "Фисташки", "price": 300},
            "2": {"pk": 2, "title": "Безе", "price": 400},
            "3": {"pk": 3, "title": "Фундук", "price": 350},
            "4": {"pk": 4, "title": "Пекан", "price": 300},
            "5": {"pk": 5, "title": "Маршмеллоу", "price": 200},
            "6": {"pk": 6, "title": "Марципан", "price": 280}
        },
        "orders.json": {
            "1": {
                "pk": 1,
                "customer": 2,
                "cakes": [1],
                "address": "пр. Ленина, д. 42",
                "delivery_date": "2024-07-15",
                "delivery_time": "14:00",
                "promocode": 2,
                "comment": "Позвонить за 15 минут до прибытия"
            },
            "2": {
                "pk": 2,
                "customer": 1,
                "cakes": [2],
                "address": "ул. Пушкина, д. 10, кв. 25",
                "delivery_date": "2024-07-16",
                "delivery_time": "18:30",
                "promocode": None,
                "comment": ""
            }
        },
        "promocodes.json": {
            "1": {"pk": 1, "title": "ПЕРВЫЙЗАКАЗ", "discount": 10, "is_active": True},
            "2": {"pk": 2, "title": "ДЕНЬРОЖДЕНИЯ", "discount": 15, "is_active": True},
            "3": {"pk": 3, "title": "ИЮНЬ2025", "discount": 5, "is_active": False}
        },
        "roles.json": {
            "1": {"pk": 1, "title": "customer"},
            "2": {"pk": 2, "title": "admin"}
        },
        "shapes.json": {
            "1": {"pk": 1, "title": "Круг", "price": 400},
            "2": {"pk": 2, "title": "Квадрат", "price": 600},
            "3": {"pk": 3, "title": "Прямоугольник", "price": 1000}
        },
        "toppings.json": {
            "1": {"pk": 1, "title": "Без топпинга", "price": 0},
            "2": {"pk": 2, "title": "Белый соус", "price": 200},
            "3": {"pk": 3, "title": "Карамельный сироп", "price": 180},
            "4": {"pk": 4, "title": "Кленовый сироп", "price": 200},
            "5": {"pk": 5, "title": "Клубничный сироп", "price": 300},
            "6": {"pk": 6, "title": "Черничный сироп", "price": 350},
            "7": {"pk": 7, "title": "Молочный шоколад", "price": 200}
        },
        "users.json": {
            "1": {
                "pk": 1,
                "tg_id": 123456789,
                "full_name": "Иван Иванов",
                "role": 1,
                "address": "ул. Пушкина, д. 10, кв. 25",
                "phone": "+79111234567"
            },
            "2": {
                "pk": 2,
                "tg_id": 987654321,
                "full_name": "Мария Петрова",
                "role": 1,
                "address": "пр. Ленина, д. 42",
                "phone": "+79219876543"
            }
        }
    }

    for filename, data in test_data.items():
        file_path = json_dir / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    create_test_json_files()
