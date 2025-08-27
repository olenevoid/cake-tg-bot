from telegram import InlineKeyboardMarkup
from tg_bot.callbacks import Callback, CallbackButton
from utils import split_to_sublists
from demo_data.models import User


def get_main_menu(user: User):
    buttons = [
        CallbackButton(
            'Заказать торт',
            Callback.ORDER_CAKE
        ),
        CallbackButton(
            'Показать цены',
            Callback.SHOW_PRICELIST
        ),
    ]

    if not user:
        buttons.append(
            CallbackButton(
                'Регистрация',
                Callback.SIGNUP
            )
        )

    if user and user.role.title == "Customer":
        buttons.append(
            CallbackButton(
                'Мои заказы',
                Callback.MY_ORDERS
            )
        )

    if user and user.role.title == "Admin":
        buttons.append(
            CallbackButton(
                'Заказы',
                Callback.ALL_ORDERS
            )
        )

    if user:
        buttons.append(
            CallbackButton(
                'Удалить пользователя (для тестов)',
                Callback.DELETE_USER
            )
        )

    buttons = split_to_sublists(buttons, 1)

    return InlineKeyboardMarkup(buttons)


def get_back_to_menu():
    buttons = [
        [
            CallbackButton(
                'В меню',
                Callback.MAIN_MENU
            )
         ]
    ]

    return InlineKeyboardMarkup(buttons)


def get_personal_data_keyboard():
    buttons = [
        CallbackButton(
            'Да',
            Callback.YES
        ),
        CallbackButton(
            'Нет',
            Callback.NO
        )
    ]
    
    buttons = split_to_sublists(buttons, 2)
    
    buttons.append(
        [
            CallbackButton(
                'Скачать',
                Callback.DOWNLOAD
            )
        ]
    )
    
    return InlineKeyboardMarkup(buttons)
    
    
def get_confirm_registration():
    buttons = [
        CallbackButton(
            'Да',
            Callback.YES
        ),
        CallbackButton(
            'Изменить',
            Callback.REDO
        ),
    ]
    
    buttons = split_to_sublists(buttons, 2)
    
    buttons.append(
        [
            CallbackButton(
                'В меню',
                Callback.MAIN_MENU
            )
        ]
    )
    
    return InlineKeyboardMarkup(buttons)


def get_my_orders():
    pass
