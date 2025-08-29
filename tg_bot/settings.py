from environs import env


env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
BUTTONS_PER_PAGE = 4

# Цены за уровни торта
LEVEL_1_PRICE = env.int("LEVEL_1_PRICE")
LEVEL_2_PRICE = env.int("LEVEL_2_PRICE")
LEVEL_3_PRICE = env.int("LEVEL_3_PRICE")