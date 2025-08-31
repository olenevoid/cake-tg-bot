# Валидаторы для имени, номера телефона, адреса, времени доставки
import re
from typing import Tuple
from datetime import date, time, datetime, timedelta


def is_phone(phone: str) -> Tuple[bool, str]:
    """Проверяет, соответствует ли номер российскому формату:
    +7XXXXXXXXXX, 8XXXXXXXXXX или 7XXXXXXXXXX
    """
    # Убираем все нецифровые символы, кроме плюса
    cleaned_phone = re.sub(r"[^\d+]", "", phone)

    # Проверяем основные форматы российских номеров
    pattern = r"^(\+7|8|7)\d{10}$"

    if not re.match(pattern, cleaned_phone):
        return (
            False,
            "Номер телефона должен быть в формате +7XXXXXXXXXX, 8XXXXXXXXXX или 7XXXXXXXXXX (11 цифр после кода страны)",
        )

    return True, ""


def is_valid_name(full_name: str) -> Tuple[bool, str]:
    """Проверяет валидность полного имени.
    Возвращает (True, "") если имя валидно, (False, "сообщение об ошибке") если нет.
    """
    # Удаляем лишние пробелы
    full_name = full_name.strip()

    # Проверка минимальной и максимальной длины
    if len(full_name) < 4:
        return False, "Слишком короткое имя. Введите имя и фамилию."
    if len(full_name) > 60:
        return False, "Слишком длинное имя. Максимум 60 символов."

    # Проверка допустимых символов (буквы, пробелы, дефисы)
    if not re.fullmatch(r"^[а-яА-ЯёЁa-zA-Z\s-]+$", full_name):
        return False, "Можно использовать только буквы, пробелы и дефис."

    # Разделение на части
    parts = full_name.split()

    # Проверка количества частей
    if len(parts) < 2:
        return False, "Введите и имя, и фамилию через пробел."
    if len(parts) > 3:
        return False, "Слишком много частей в имени. Максимум: имя, отчество и фамилия."

    # Проверка каждой части
    for part in parts:
        # Длина части
        if len(part) < 2:
            return False, f"Часть '{part}' слишком короткая. Минимум 2 буквы."
        if len(part) > 20:
            return False, f"Часть '{part}' слишком длинная. Максимум 20 букв."

        # Проверка символов в части (только буквы и дефисы)
        if not re.match(r"^[а-яА-ЯёЁa-zA-Z-]+$", part):
            return False, f"Часть '{part}' содержит недопустимые символы."

    return True, ""


def is_address(address: str) -> Tuple[bool, str]:
    """Проверяет валидность адреса доставки."""
    address = address.strip()

    # Проверка длины
    if len(address) < 5:
        return False, "Адрес слишком короткий. Укажите, пожалуйста, полный адрес."

    # Проверка наличия цифр (номера дома)
    if not re.search(r"\d", address):
        return False, "Укажите, пожалуйста, номер дома в адресе."

    return True, ""


def is_valid_delivery_date(delivery_date: date) -> Tuple[bool, str]:
    """Проверяет что дата доставки:
    - Не раньше сегодняшнего дня
    - Не позднее чем через 3 дня
    """
    today = date.today()

    if delivery_date < today:
        return False, "Дата доставки не может быть в прошлом"

    if delivery_date > today + timedelta(days=3):
        return False, "Максимальный срок доставки — 3 дня"

    return True, ""


def is_valid_delivery_time(delivery_time: time, delivery_date: date = None) -> Tuple[bool, str]:
    """Проверяет что время доставки:
    - В промежутке 09:00-21:00
    - Если доставка на сегодня, то время должно быть как минимум на 2 часа позже текущего
    """
    now = datetime.now()

    # Проверка временного окна
    if not (time(9, 0) <= delivery_time <= time(21, 0)):
        return False, "Доставка осуществляется с 09:00 до 21:00"

    # Если дата доставки - сегодня, проверяем чтобы время было в будущем
    if delivery_date and delivery_date == now.date():
        min_delivery_time = (now + timedelta(hours=2)).time()
        if delivery_time < min_delivery_time:
            return False, "Доставка возможна минимум через 2 часа от текущего времени"

    return True, ""
