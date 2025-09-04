from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
import tg_bot.settings as settings
import demo_data.demo_db as db
from tg_bot.handlers.states import State


async def start(update: Update, context: CallbackContext):
    await update.message.delete()
    tg_id = update.effective_chat.id
    user = db.find_user(tg_id)

    await update.message.reply_text(
        strings.get_main_menu(user),
        reply_markup=keyboards.get_main_menu(user),
        parse_mode='HTML'
    )
    return State.MAIN_MENU


async def show_main_menu(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    user = db.find_user(tg_id)
    text = strings.get_main_menu(user)
    keyboard = keyboards.get_main_menu(user)

    if context.user_data.get('new_message'):
        context.user_data['new_message'] = False
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    return State.MAIN_MENU


async def order_cake(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.START_ORDER

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_order_cake(),
        parse_mode='HTML'
    )

    return State.ORDER_CAKE


async def my_orders(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    user = db.find_user(tg_id)
    if not user:
        return

    all_orders = db.get_orders()
    text = ''
    if user.role.title == 'customer':
        orders = [order for order in all_orders if order.customer == user]
        text = strings.get_my_orders(orders)

    if user.role.title == 'admin':
        orders = all_orders
        text = strings.get_all_orders(orders)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )


async def show_pricelist(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    toppings = db.get_toppings()
    decor = db.get_decors()
    berries = db.get_berries()
    shapes = db.get_shapes()

    text = strings.show_pricelist(
        settings.LAYERS,
        shapes,
        toppings,
        decor,
        berries
    )

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_back_to_menu(),
        parse_mode='HTML'
    )


async def change_role(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    user = db.find_user(tg_id)

    if user.role.title == 'customer':
        role_pk = 2
    if user.role.title == 'admin':
        role_pk = 1

    db.delete_user_from_db(tg_id)
    db.add_user(
        user.tg_id,
        user.full_name,
        user.address,
        user.phone,
        role_pk
    )

    return await show_main_menu(update, context)
