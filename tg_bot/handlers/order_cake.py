from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State
from demo_data.demo_db import get_cakes, get_cake, find_user
from tg_bot.callbacks import parse_callback_data_string, CallbackData


async def show_cakes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    text = 'Торты'
    cakes = get_cakes()
    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_cake(cakes),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES


async def show_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    user = find_user(tg_id)
    params = parse_callback_data_string(update.callback_query.data).params
    cake_pk = params.get('cake_pk')
    cake = get_cake(cake_pk)
    text = f'Торт {cake.title}'
    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES
