from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.settings import LAYERS
from tg_bot.handlers.states import State
from tg_bot.callbacks import parse_callback_data_string


async def start_creating_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = 'Тут что-то будет'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def select_layers(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = 'Количество слоев'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_layers(LAYERS),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def save_layers(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    layers = params.get('layers')

    if layers:
        context.user_data['layers'] = layers

    return await start_creating_cake(update, context)