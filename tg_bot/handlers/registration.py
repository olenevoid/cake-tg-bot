from telegram import Update
import tg_bot.keyboards as keyboards
from telegram.ext import CallbackContext
import tg_bot.strings as strings
import tg_bot.settings as settings
import tg_bot.validators as validators
from demo_data.demo_db import add_customer, delete_user_from_db
from tg_bot.handlers.states import State
import tg_bot.handlers.main_menu as main_menu


async def start_registration(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    text = strings.PERSONAL_DATA_PROCESSING_CONSENT
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
        return await input_phone(update, context)

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
    
    return State.INPUT_PHONE


async def validate_phone(update: Update, context: CallbackContext):
    phone = update.message.text
    if validators.is_phone(phone)[0]:
        context.user_data['phone'] = phone
        return await input_address(update, context)

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

    return State.INPUT_ADDRESS


async def validate_address(update: Update, context: CallbackContext):
    address = update.message.text
    if validators.is_address(address)[0]:
        context.user_data['address'] = address
        return await confirm_signup(update, context)

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

    return State.CONFIRM_SIGNUP


async def signup_customer(update: Update, context: CallbackContext):
    tg_id = update.effective_chat.id
    name = context.user_data.get('full_name')
    phone = context.user_data.get('phone')
    address = context.user_data.get('address')
    add_customer(tg_id, name, address, phone)
    text = strings.get_signup_complete(name)

    cart = context.user_data.get('cart')

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboards.get_signup_complete_menu(cart)
    )
    return State.CONFIRM_SIGNUP


async def delete_user(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    tg_id = update.effective_chat.id
    delete_user_from_db(tg_id)
    return await main_menu.show_main_menu(update, context)
