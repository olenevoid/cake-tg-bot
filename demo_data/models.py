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
    custom: bool
    topping: Topping
    shape: Shape
    number_of_layers: int
    sign: str
    decor: list[Decor] = field(default_factory=list[Decor])
    berries: list[Berry] = field(default_factory=list[Berry])

    def get_price(self):
        # Считаем сумму со всех элементов и выводим
        return 1337


@dataclass
class Order:
    pk: int
    customer: User
    cake: Cake
    address: str  # Если не указан, то загружаем от пользователя
    delivery_date: date
    delivery_time: time | None
    promocode: Promocode | None
    comment: str
