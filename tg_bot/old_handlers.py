from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext
)
from tg_bot.callbacks import Callback, parse_callback_data_string, get_pattern
import tg_bot.strings as strings
import tg_bot.settings as settings
from enum import Enum, auto
import tg_bot.validators as validators
from demo_data.demo_db import (
    get_toppings,
    get_berries,
    get_decor,
    find_user,
    add_customer,
    delete_user_from_db
)
from tg_bot.handlers.states import State


'''
class State(Enum):
    MAIN_MENU = auto()
    REGISTRATION = auto()
    PERSONAL_DATA_PROCESSING = auto()
    INPUT_NAME = auto()
    INPUT_ADDRESS = auto()
    INPUT_PHONE = auto()
    CONFIRM_SIGNUP = auto()

'''
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


async def start_registration(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.PERSONAL_DATA_PROCESSING_CONSENT
    tg_id = update.effective_chat.id
    # add_customer(tg_id)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.get_personal_data_keyboard(),
        parse_mode='HTML'
    )

    return State.REGISTRATION


async def send_personal_data_consent(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    
    #TODO: Добавить отправку файла с соглашением персональных данных
    
    return State.PERSONAL_DATA_PROCESSING


async def input_name(update: Update, context: CallbackContext):
    text = strings.INPUT_YOUR_NAME

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
    )

    return State.INPUT_NAME


async def validate_name(update: Update, context: CallbackContext):
    full_name = update.message.text
    if validators.is_valid_name(full_name)[0]:
        context.user_data['full_name'] = full_name
        await input_phone(update, context)
        return State.INPUT_PHONE

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=strings.FULL_NAME_IS_INCORRECT,
                parse_mode='HTML',
        )

        return State.INPUT_NAME


async def input_phone(update: Update, context: CallbackContext):
    text = strings.INPUT_YOUR_PHONE

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
    )


async def validate_phone(update: Update, context: CallbackContext):
    phone = update.message.text
    if validators.is_phone(phone)[0]:
        context.user_data['phone'] = phone
        await input_address(update, context)
        return State.INPUT_ADDRESS

    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=strings.PHONE_IS_INCORRECT,
                parse_mode='HTML',
        )

        return State.INPUT_PHONE


async def input_address(update: Update, context: CallbackContext):
    text = strings.INPUT_YOUR_ADDRESS

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
    )


async def validate_address(update: Update, context: CallbackContext):
    address = update.message.text
    if validators.is_address(address)[0]:
        context.user_data['address'] = address
        # Заготовка на будущее, чтобы во время заказа торта можно было
        # использовать эту же функцию
        mode = context.user_data.get('mode')
        if mode == 'make_order':
            return
        await confirm_signup(update, context)
        return State.CONFIRM_SIGNUP
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=strings.ADDRESS_IS_INCORRECT,
                parse_mode='HTML',
        )

        return State.INPUT_ADDRESS


async def confirm_signup(update: Update, context: CallbackContext):
    name = context.user_data.get('full_name')
    phone = context.user_data.get('phone')
    address = context.user_data.get('address')

    text = strings.get_confirm_signup(
        name,
        phone,
        address
    )

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboards.get_confirm_registration()
    )


async def signup_customer(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    name = context.user_data.get('full_name')
    phone = context.user_data.get('phone')
    address = context.user_data.get('address')
    add_customer(tg_id, name, address, phone)

    text = strings.get_signup_complete(name)

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboards.get_back_to_menu()
    )
    return State.MAIN_MENU


async def delete_user(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    delete_user_from_db(tg_id)
    await main_menu(update, context)


def get_handlers():

    registration_level = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(main_menu, get_pattern(Callback.NO)),
            CallbackQueryHandler(input_name, get_pattern(Callback.YES)),
            CallbackQueryHandler(
                send_personal_data_consent,
                Callback.DOWNLOAD
            )
        ],
        states={
            State.PERSONAL_DATA_PROCESSING: [
                CallbackQueryHandler(main_menu, get_pattern(Callback.NO)),
                CallbackQueryHandler(input_name, get_pattern(Callback.YES)),
                CallbackQueryHandler(
                    send_personal_data_consent,
                    Callback.DOWNLOAD
                )
            ],
            State.INPUT_NAME: [
                MessageHandler(filters.TEXT, validate_name),
            ],
            State.INPUT_PHONE: [
                MessageHandler(filters.TEXT, validate_phone)
            ],
            State.INPUT_ADDRESS: [
                MessageHandler(filters.TEXT, validate_address)
            ],
            State.CONFIRM_SIGNUP: [
                CallbackQueryHandler(signup_customer, Callback.YES),
                CallbackQueryHandler(input_name, Callback.REDO)
            ]
        },
        map_to_parent={
            State.MAIN_MENU: State.MAIN_MENU
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, get_pattern(Callback.MAIN_MENU))
        ]
    )

    return ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, get_pattern(Callback.MAIN_MENU))
        ],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(
                    order_cake,
                    get_pattern(Callback.ORDER_CAKE)
                ),
                CallbackQueryHandler(
                    show_pricelist,
                    get_pattern(Callback.SHOW_PRICELIST)
                ),
                CallbackQueryHandler(
                    my_orders,
                    get_pattern(Callback.MY_ORDERS)
                ),
                CallbackQueryHandler(
                    start_registration,
                    get_pattern(Callback.SIGNUP)
                ),
            ],
            State.REGISTRATION: [registration_level]

        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, get_pattern(Callback.MAIN_MENU)),
            CallbackQueryHandler(
                delete_user,
                get_pattern(Callback.DELETE_USER)
            ),
        ]
    )
