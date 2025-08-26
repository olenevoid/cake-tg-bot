from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext
)
from tg_bot.callbacks import Callback, parse_callback_data_string, get_pattern
import tg_bot.strings as strings
import tg_bot.settings as settings
from enum import Enum, auto

from demo_data.demo_db import (get_user,
                               get_toppings,
                               get_berries,
                               get_decor,
                               find_user,
                               add_user,
                               delete_user_from_db
)


class State(Enum):
    MAIN_MENU = auto()
    PERSONAL_DATA_PROCESSING = auto()


async def start(update: Update, context: CallbackContext):
    await update.message.delete()
    tg_id = update.effective_chat.id
    user = find_user(tg_id)

    await update.message.reply_text(
        strings.get_main_menu(user),
        reply_markup=keyboards.get_main_menu(user),
        parse_mode='HTML'
    )
    return State.MAIN_MENU


async def main_menu(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    #user = get_user()
    tg_id = update.effective_chat.id
    user = find_user(tg_id)
    text = strings.get_main_menu(user)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_main_menu(user),
        parse_mode='HTML'
    )
    return State.MAIN_MENU


async def order_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.START_ORDER

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )


async def my_orders(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    orders = []
    text = strings.get_my_orders(orders)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )


async def show_pricelist(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    toppings = get_toppings()
    decor = get_decor()
    berries = get_berries()

    text = strings.show_ingredients('Топпинги', toppings)
    text += strings.show_ingredients('Декор', decor)
    text += strings.show_ingredients('Ягоды', berries)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )


async def start_registration(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.PERSONAL_DATA_PROCESSING_CONSENT
    tg_id = update.effective_chat.id
    add_user(tg_id)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )

    return State.PERSONAL_DATA_PROCESSING


async def delete_user(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    delete_user_from_db(tg_id)
    await main_menu(update, context)


def get_handlers():
    return ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, get_pattern(Callback.MAIN_MENU))
        ],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(
                    order_cake,
                    get_pattern(Callback.ORDER_CAKE)
                ),
                CallbackQueryHandler(
                    show_pricelist,
                    get_pattern(Callback.SHOW_PRICELIST)
                ),
                CallbackQueryHandler(
                    my_orders,
                    get_pattern(Callback.MY_ORDERS)
                ),
                CallbackQueryHandler(
                    start_registration,
                    get_pattern(Callback.SIGNUP)
                ),
            ],
            State.PERSONAL_DATA_PROCESSING: [

            ]
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, get_pattern(Callback.MAIN_MENU)),
            CallbackQueryHandler(
                delete_user,
                get_pattern(Callback.DELETE_USER)
            ),
        ]
    )
