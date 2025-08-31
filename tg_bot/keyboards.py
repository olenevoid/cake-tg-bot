from telegram import InlineKeyboardMarkup
from tg_bot.callbacks import Callback, CallbackButton
from utils import split_to_sublists
from demo_data.models import User, Cake
import tg_bot.buttons as static_buttons
from datetime import date, time


def get_main_menu(user: User):
    buttons = [
        static_buttons.ORDER_CAKE,
        static_buttons.SHOW_PRICELIST,
    ]

    if not user:
        buttons.append(static_buttons.SIGNUP)

    if user and user.role.title == "customer":
        buttons.append(static_buttons.MY_ORDERS)

    if user and user.role.title == "admin":
        buttons.append(static_buttons.ALL_ORDERS)

    if user:
        buttons.append(static_buttons.DELETE_USER)

    buttons = split_to_sublists(buttons, 1)

    return InlineKeyboardMarkup(buttons)


def get_back_to_menu():
    buttons = [
        [static_buttons.MAIN_MENU]
    ]

    return InlineKeyboardMarkup(buttons)


def get_personal_data_keyboard():
    buttons = [
        static_buttons.YES,
        static_buttons.NO
    ]
    
    buttons = split_to_sublists(buttons, 2)
    
    buttons.append(
        [static_buttons.DOWNLOAD]
    )
    
    return InlineKeyboardMarkup(buttons)
    
    
def get_confirm_registration():
    buttons = [
        static_buttons.YES,
        static_buttons.REDO,
    ]
    
    buttons = split_to_sublists(buttons, 2)
    
    buttons.append([static_buttons.MAIN_MENU])
    
    return InlineKeyboardMarkup(buttons)


def get_order_cake():
    buttons = [
        static_buttons.SHOW_CAKES,
        static_buttons.CUSTOM_CAKE
    ]

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_select_cake(cakes: list[Cake], cakes_per_row: int = 2):
    
    buttons = []
    
    for cake in cakes:
        button = CallbackButton(
            cake.title,
            Callback.SHOW_CAKE,
            cake_pk=cake.pk
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, cakes_per_row)

    buttons.append([static_buttons.SHOW_CART])

    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_cake_menu(cake: Cake):

    buttons = [
        CallbackButton(
            'Добавить в корзину',
            Callback.ADD_TO_CART,
            cake_pk=cake.pk
        ),
        static_buttons.BACK
    ]

    buttons = split_to_sublists(buttons, 1)

    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_cart_menu(cakes: list[Cake]):

    buttons = []
    for cake in cakes:
        button = CallbackButton(
            cake.title,
            Callback.REMOVE_FROM_CART,
            cake_pk=cake.pk
        )

        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.CREATE_ORDER, static_buttons.CLEAR_CART])
    buttons.append([static_buttons.BACK, static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_signup_complete_menu(cart: list[Cake]):
    buttons = []
    
    if cart:
        buttons.append(
            [static_buttons.CREATE_ORDER]
        )

    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_create_order_menu():
    buttons = [
        static_buttons.ADD_PROMO,
        static_buttons.ADD_COMMENT
    ]

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.SELECT_DATE])
    buttons.append([static_buttons.CONFIRM_CREATE_ORDER])
    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_select_date_menu(dates: list[date]):

    buttons = []

    for date_ in dates:
        button = CallbackButton(
            f'{date_.day}.{date_.month}',
            Callback.ADD_DATE,
            date=date_.isoformat()
        )

        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)
    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_select_time_menu(times: list[time]):

    buttons = []

    for time_ in times:
        button = CallbackButton(
            f'{time_.hour}:{time_.minute}',
            Callback.ADD_TIME,
            time=time_.isoformat()
        )

        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)
    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_my_orders():
    pass
