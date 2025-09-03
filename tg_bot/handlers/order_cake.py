from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.handlers.states import State
from demo_data.demo_db import (
    get_cakes,
    get_cake,
    find_user,
    add_order,
    get_promocode,
    find_promocode
)
from tg_bot.callbacks import parse_callback_data_string
import tg_bot.handlers.registration as registration
from tg_bot.settings import DELIVERY_WITHIN_24H_SURCHARGE
from utils import get_available_dates, get_available_times, is_within_24_hours
from datetime import date, time


async def show_cakes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    cakes = get_cakes()
    cart = context.user_data.get('cart')

    await update.callback_query.edit_message_text(
        strings.get_show_cakes(cart),
        reply_markup=keyboards.get_select_cake(cakes),
        parse_mode='HTML'
    )
    return State.SHOW_CAKES


async def show_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    cake_pk = params.get('cake_pk')
    cake = get_cake(cake_pk)

    await update.callback_query.edit_message_text(
        strings.get_cake_details(cake),
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

    await update.callback_query.edit_message_text(
        strings.get_cart_details(cakes),
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


async def confirm_create_order(update: Update, context: CallbackContext):
    cart = context.user_data.get('cart')
    cakes = []
    promocode = None

    promocode_pk = context.user_data.get('promocode')
    comment = context.user_data.get('comment')
    delivery_date = date.fromisoformat(context.user_data.get('date'))
    delivery_time = time.fromisoformat(context.user_data.get('time'))

    if cart:
        cakes = [get_cake(cake_pk) for cake_pk in cart]

    if promocode_pk:
        promocode = get_promocode(promocode_pk)
        
    total_price = 0
    urgent_delivery_price = None
    discount_price = None
    for cake in cakes:
        total_price += cake.get_price()

    if is_within_24_hours(delivery_date, delivery_time):
        urgent_delivery_price = total_price * (1 + DELIVERY_WITHIN_24H_SURCHARGE / 100)

    if promocode:
        discount_price = total_price  * (1 - promocode.discount / 100)

    text = strings.get_confirm_create_order(
        cakes,
        delivery_date,
        delivery_time,
        promocode,
        comment,
        total_price,
        urgent_delivery_price,
        discount_price
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
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=strings.INPUT_PROMO,
            parse_mode='HTML',
    )

    return State.INPUT_PROMOCODE


async def validate_promocode(update: Update, context: CallbackContext):
    promocode_text = update.message.text
    promocode = find_promocode(promocode_text)
    if promocode and promocode.is_active:
        context.user_data['promocode'] = promocode.pk
        context.user_data['new_message'] = True
        return await confirm_create_order(update, context)
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=strings.PROMO_DOES_NOT_EXIST,
                parse_mode='HTML',
        )

        return State.INPUT_PROMOCODE


async def input_comment(update: Update, context: CallbackContext):
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=strings.INPUT_COMMENT,
            parse_mode='HTML',
    )

    return State.INPUT_COMMENT


async def add_comment(update: Update, context: CallbackContext):
    comment = update.message.text
    context.user_data['comment'] = comment
    context.user_data['new_message'] = True
    return await confirm_create_order(update, context)


async def select_date(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    user = find_user(tg_id)

    if not user:
        return await registration.start_registration(update, context)

    dates = get_available_dates()

    await update.callback_query.edit_message_text(
        strings.SELECT_DATE,
        reply_markup=keyboards.get_select_date_menu(dates),
        parse_mode='HTML'
    )

    return State.CREATE_ORDER


async def add_date(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    date = params.get('date')
    context.user_data['date'] = date

    return await select_time(update, context)


async def select_time(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    delivery_date = context.user_data.get('date')
    times = get_available_times(date.fromisoformat(delivery_date))

    await update.callback_query.edit_message_text(
        strings.SELECT_TIME,
        reply_markup=keyboards.get_select_time_menu(times),
        parse_mode='HTML'
    )

    return State.CREATE_ORDER


async def add_time(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    time = params.get('time')
    context.user_data['time'] = time

    return await confirm_create_order(update, context)


async def create_order(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    user = find_user(tg_id)
    delivery_date = context.user_data.get('date')
    delivery_time = context. user_data.get('time')
    promocode_pk = context.user_data.get('promocode')
    promocode = find_promocode(promocode_pk)
    comment = context.user_data.get('comment')

    cakes = context.user_data.get('cart')
    add_order(
        user,
        cakes,
        user.address,
        delivery_date,
        delivery_time,
        promocode,
        comment
    )

    await update.callback_query.edit_message_text(
        strings.ORDER_CREATED,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )

    return State.CREATE_ORDER
