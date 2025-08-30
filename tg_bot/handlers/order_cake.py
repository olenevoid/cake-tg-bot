from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State
from demo_data.demo_db import get_cakes, get_cake, find_user
from tg_bot.callbacks import parse_callback_data_string
import tg_bot.handlers.registration as registration
import tg_bot.validators as validators


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
    return State.SHOW_CAKE


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


async def show_cart(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    cart = context.user_data.get('cart')
    cakes = []

    if cart:
        cakes = [get_cake(cake_pk) for cake_pk in cart]

    ### в strings
    if not cart:
        text = 'Корзина пуста'
    else:
        text = (
            f'Позиций в корзине: {len(cart)}\n'
            'Тут список тортов\n'
            'Нажмите на кнопку с названием торта чтобы удалить из корзины'
        )
    ###

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_cart_menu(cakes),
        parse_mode='HTML'
    )

    return State.SHOW_CART


async def remove_cake_from_cart(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    cake_pk = params.get('cake_pk')
    cart: list = context.user_data.get('cart')
    if cart:
        cart.remove(cake_pk)

    return await show_cart(update, context)


async def clear_cart(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    context.user_data['cart'] = []

    return await show_cart(update, context)


async def create_order(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    user = find_user(tg_id)

    if not user:
        return await registration.start_registration(update, context)

    cart = context.user_data.get('cart')
    cakes = []

    promocode = context.user_data.get('promocode')
    comment = context.user_data.get('comment')

    if cart:
        cakes = [get_cake(cake_pk) for cake_pk in cart]

    text = (
        'Подтвердите создание заказа\n'
        f'Всего {len(cakes)} позиций\n'
        'Список\n'
    )

    if promocode:
        text += f'Использован промокод {promocode}\n'
        
    if comment:
        text += (
            'Комментарий заказчика:\n'
            f'{comment}\n'
        )

    if context.user_data.get('new_message'):
        context.user_data['new_message'] = False
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=keyboards.get_create_order_menu(),
            parse_mode='HTML',
        )

    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=keyboards.get_create_order_menu(),
            parse_mode='HTML'
        )

    return State.CREATE_ORDER


async def input_promocode(update: Update, context: CallbackContext):
    text = 'Введите промокод'

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
    )

    return State.INPUT_PROMOCODE


async def validate_promocode(update: Update, context: CallbackContext):
    promocode = update.message.text
    if validators.is_valid_promocode(promocode):
        context.user_data['promocode'] = promocode
        context.user_data['new_message'] = True
        return await create_order(update, context)

    else:

        text = 'Такого промокода нет'

        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode='HTML',
        )

        return State.INPUT_PROMOCODE


async def input_comment(update: Update, context: CallbackContext):
    text = 'Введите комментарий'

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
    )

    return State.INPUT_COMMENT


async def add_comment(update: Update, context: CallbackContext):
    comment = update.message.text
    context.user_data['comment'] = comment
    context.user_data['new_message'] = True
    return await create_order(update, context)
