#TODO Сделать модели в ДБ по образу
from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional
from .utils import calculate_order_total_price


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
    discount: int = 10
    is_active: bool = True


@dataclass
class Cake:
    pk: int
    title: str
    price: Optional[int] = None  # Новое поле: цена для типовых тортов
    image: Optional[str] = None  # Новое поле: ссылка на изображение
    topping: Optional[Topping] = None
    shape: Optional[Shape] = None
    number_of_layers: Optional[int] = None
    sign: Optional[str] = None
    custom: bool = False
    decor: list[Decor] = field(default_factory=list[Decor])
    berries: list[Berry] = field(default_factory=list[Berry])

    def get_price(self):
        # Если цена задана напрямую, возвращаем ее
        if self.price is not None:
            return self.price

        # Иначе вычисляем цену для кастомного торта
        # Проверяем, что все необходимые поля заданы
        if self.topping is None:
            raise ValueError("Topping is required for custom cake")
        if self.shape is None:
            raise ValueError("Shape is required for custom cake")
        if self.number_of_layers is None:
            raise ValueError("Number of layers is required for custom cake")
        if self.sign is None:
            raise ValueError("Sign is required for custom cake")

        # Цена за количество уровней из настроек
        from tg_bot import settings

        level_prices = {
            1: settings.LEVEL_1_PRICE,
            2: settings.LEVEL_2_PRICE,
            3: settings.LEVEL_3_PRICE,
        }
        price = level_prices.get(self.number_of_layers)

        if price is None:
            # Если количество уровней не 1,2,3, используем цену за 1 уровень
            price = settings.LEVEL_1_PRICE

        # Цена формы
        price += self.shape.price

        # Цена топпинга
        price += self.topping.price

        # Цена ягод (если есть)
        for berry in self.berries:
            price += berry.price

        # Цена декора (если есть)
        for decor_item in self.decor:
            price += decor_item.price

        # Цена надписи (если есть текст)
        if self.sign.strip():
            price += 500

        return price


@dataclass
class Order:
    pk: int
    customer: User
    cakes: list[Cake]
    address: str  # Если не указан, то загружаем от пользователя
    delivery_date: date
    delivery_time: Optional[time] = None
    promocode: Optional[Promocode] = None
    comment: Optional[str] = None

    def get_total_price(self):
        from .utils import calculate_order_total_price
        return calculate_order_total_price(self)
