from environs import env


env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
BUTTONS_PER_PAGE = 4