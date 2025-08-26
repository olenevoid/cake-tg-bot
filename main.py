from telegram.ext import ApplicationBuilder
from tg_bot.handlers import get_handlers
from tg_bot.settings import TG_BOT_TOKEN


def main():
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(get_handlers())
    app.run_polling()


if __name__ == "__main__":
    main()
