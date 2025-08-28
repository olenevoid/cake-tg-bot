from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State
from demo_data.demo_db import get_cakes


async def show_cakes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    #tg_id = update.effective_chat.id
    #user = find_user(tg_id)
    text = strings.CAKES_LIST # Использована строка из strings.py вместо "Торты"
    cakes = get_cakes()
    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_cake(cakes),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES
