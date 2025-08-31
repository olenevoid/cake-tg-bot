from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State


async def start_creating_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = 'Тут что-то будет'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE
