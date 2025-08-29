from telegram.ext import ApplicationBuilder
from tg_bot.handlers.state_machines import get_main_conversation_handler
from tg_bot.settings import TG_BOT_TOKEN
from demo_data.create_test_data import create_test_json_files


def main():
    create_test_json_files()
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(get_main_conversation_handler())
    app.run_polling()


if __name__ == "__main__":
    main()
