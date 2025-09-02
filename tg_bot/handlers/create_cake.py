from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
from tg_bot.settings import LAYERS
from tg_bot.handlers.states import State
from tg_bot.callbacks import parse_callback_data_string
from demo_data import demo_db as db


async def start_creating_cake(update: Update, context: CallbackContext):
    layers = context.user_data.get('layers')
    shape = db.get_shape(context.user_data.get('shape_pk'))
    decor = db.get_decor(context.user_data.get('decor_pk'))
    berry_pk = context.user_data.get('berry_pk')
    berry = db.get_berry(berry_pk)
    topping = db.get_topping(context.user_data.get('topping_pk'))
    sign = context.user_data.get('sign')

    text = 'Тут что-то будет\n'

    if layers:
        text += f'Количество слоев: {layers} цена: {LAYERS.get(layers)}\n'

    if shape:
        text += f'Форма: {shape.title} цена: {shape.price}\n'

    if decor:
        text += f'Декор: {decor.title} цена: \n'

    if berry:
        text += f'Ягоды: {berry.title} цена: \n'

    if topping:
        text += f'Топпинг: {topping.title} цена: \n'

    if sign:
        text += f'Надпись: {sign}'

    text += 'Добавить торт в корзину?'

    keyboard = keyboards.get_confirm_create_cake()
    state = State.CREATE_CAKE
    if context.user_data.get('new_message'):
        context.user_data['new_message'] = False
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML',
        )
        return state

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    return state


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

    return await select_shape(update, context)


async def select_shape(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    shapes = db.get_shapes()
    text = 'Форма'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_shape(shapes),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def save_shape(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    shape_pk = params.get('shape_pk')

    if shape_pk:
        context.user_data['shape_pk'] = shape_pk

    return await select_topping(update, context)


async def select_topping(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    toppings = db.get_toppings()
    text = 'Форма'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_topping(toppings),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def save_topping(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    topping_pk = params.get('topping_pk')

    if topping_pk:
        context.user_data['topping_pk'] = topping_pk

    return await start_creating_cake(update, context)


async def select_decor(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    decor = db.get_decors()
    text = 'Декор'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_decor(decor),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def save_decor(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    decor_pk = params.get('decor_pk')

    if decor_pk:
        context.user_data['decor_pk'] = decor_pk

    return await start_creating_cake(update, context)


async def select_berry(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    berries = db.get_berries()
    text = 'Декор'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_select_berry(berries),
        parse_mode='HTML'
    )
    return State.CREATE_CAKE


async def save_berry(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    berry_pk = params.get('berry_pk')

    if berry_pk:
        context.user_data['berry_pk'] = berry_pk

    return await start_creating_cake(update, context)


async def input_sign(update: Update, context: CallbackContext):
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Ведите надпись',
            parse_mode='HTML',
    )

    return State.INPUT_SIGN


async def add_sign(update: Update, context: CallbackContext):
    sign = update.message.text
    context.user_data['sign'] = sign
    context.user_data['new_message'] = True
    return await start_creating_cake(update, context)


async def save_custom_cake(update: Update, context: CallbackContext):
    layers = context.user_data.get('layers')
    shape = db.get_shape(context.user_data.get('shape_pk'))
    decor = db.get_decor(context.user_data.get('decor_pk'))
    berry = db.get_berry(context.user_data.get('berry_pk'))
    topping = db.get_topping(context.user_data.get('topping_pk'))
    sign = context.user_data.get('sign')

    cake = db.add_cake(
        f'{shape.title} {topping.title}',
        None,
        None,
        topping.pk,
        shape.pk,
        layers,
        sign,
        [decor.pk],
        [berry.pk],
        True
    )

    cart = context.user_data.get('cart')
    if cart is None:
        cart = []

    cart.append(cake.get('pk'))
    context.user_data['cart'] = cart

    await update.callback_query.edit_message_text(
        'Торт создан и добавлен в корзину',
        reply_markup=keyboards.get_cake_created_menu(),
        parse_mode='HTML'
    )

    return State.ORDER_CAKE
