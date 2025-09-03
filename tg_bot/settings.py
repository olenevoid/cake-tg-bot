from environs import env


env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")


# Цены за уровни торта
LEVEL_1_PRICE = env.int("LEVEL_1_PRICE")
LEVEL_2_PRICE = env.int("LEVEL_2_PRICE")
LEVEL_3_PRICE = env.int("LEVEL_3_PRICE")

DELIVERY_WITHIN_24H_SURCHARGE = 20

LAYERS = {
    1: LEVEL_1_PRICE,
    2: LEVEL_2_PRICE,
    3: LEVEL_3_PRICE
}


# Переменные для времени
EVENING_HOUR = env.int("EVENING_HOUR", 18)  # По умолчанию 18:00
WORK_HOURS_START = env.int("WORK_HOURS_START", 8)  # Начало рабочего дня
WORK_HOURS_END = env.int("WORK_HOURS_END", 21)  # Конец рабочего дня
MIN_PREPARATION_TIME_HOURS = env.int("MIN_PREPARATION_TIME_HOURS", 2)  # Минимальное время приготовления
MIN_DELIVERY_TIME_HOURS = env.int("MIN_DELIVERY_TIME_HOURS", 1)  # Минимальное время доставки