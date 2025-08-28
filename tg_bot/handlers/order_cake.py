from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State
from demo_data.demo_db import get_cakes, get_cake, find_user
from tg_bot.callbacks import parse_callback_data_string


async def show_cakes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    cakes = get_cakes()
    cart = context.user_data.get('cart')

    ### в strings
    text = 'Торты\n'
    if cart:
        text +=f'Тортов в корзине: {len(cart)}'
    ###

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_cake(cakes),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES


async def show_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    #tg_id = update.effective_chat.id
    #user = find_user(tg_id)
    params = parse_callback_data_string(update.callback_query.data).params
    cake_pk = params.get('cake_pk')
    cake = get_cake(cake_pk)
    text = f'Торт {cake.title} за {cake.get_price()}'
    
    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_cake_menu(cake),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES


async def add_to_cart(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    cake_pk = params.get('cake_pk')
    cart = context.user_data.get('cart')
    if cart is None:
        cart = []

    cart.append(cake_pk)
    
    context.user_data['cart'] = cart

    return await show_cakes(update, context)

