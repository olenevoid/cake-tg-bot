from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
import tg_bot.settings as settings
from demo_data.demo_db import (
    get_toppings,
    get_berries,
    get_decor,
    find_user,
)
from tg_bot.handlers.states import State


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
