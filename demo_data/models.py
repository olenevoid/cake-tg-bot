#TODO Сделать модели в ДБ по образу
from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Role:
    pk: int
    title: str


@dataclass
class User:
    pk: int
    tg_id: int
    full_name: str
    role: Role
    address: str
    phone: str


@dataclass
class Topping:
    pk: int
    title: str
    price: int


@dataclass
class Shape:
    pk: int
    title: str
    price: int


@dataclass
class Berry:
    pk: int
    title: str
    price: int


@dataclass
class Decor:
    pk: int
    title: str
    price: int


@dataclass
class Promocode:
    pk: int
    title: str
    is_active: bool


@dataclass
class Cake:
    pk: int
    title: str
    topping: Topping
    shape: Shape
    number_of_layers: int
    sign: str
    custom: bool = False  # Новое поле
    decor: list[Decor] = field(default_factory=list[Decor])
    berries: list[Berry] = field(default_factory=list[Berry])

    def get_price(self):
        # Цена за количество уровней
        level_prices = {1: 400, 2: 750, 3: 1100}
        price = level_prices.get(self.number_of_layers, 400)  # по умолчанию 400р за 1 уровень

        # Цена формы
        price += self.shape.price
        
        # Цена топпинга
        price += self.topping.price

        # Цена ягод
        for berry in self.berries:
            price += berry.price

        # Цена декора
        for decor_item in self.decor:
            price += decor_item.price

        # Цена надписи
        if self.sign and self.sign.strip():  # проверяем, что надпись не пустая
            price += 500
        
        return price


@dataclass
class Order:
    pk: int
    customer: User
    cakes: list[Cake]
    address: str  # Если не указан, то загружаем от пользователя
    delivery_date: date
    delivery_time: time | None
    promocode: Promocode | None
    comment: str
