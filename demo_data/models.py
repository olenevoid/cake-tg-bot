#TODO Сделать модели в ДБ по образу
from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional
from tg_bot.settings import LAYERS
from utils import is_within_24_hours
from tg_bot.settings import DELIVERY_WITHIN_24H_SURCHARGE


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
    image_path: Optional[str] = None  # Новое поле: ссылка на изображение
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

        # Цена за количество уровней из настроек
        price = LAYERS.get(self.number_of_layers)

        if price is None:
            # Если количество уровней не 1,2,3, используем цену за 1 уровень
            price = LAYERS.get(1)

        # Цена формы
        price += self.shape.price

        # Цена топпинга
        price += self.topping.price

        # Цена ягод (если есть)
        if self.berries:
            for berry in self.berries:
                price += berry.price

        # Цена декора (если есть)
        if self.decor:
            for decor_item in self.decor:
                price += decor_item.price

        # Цена надписи (если есть текст)
        if self.sign and self.sign.strip():
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
        return calculate_order_total_price(self)


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
