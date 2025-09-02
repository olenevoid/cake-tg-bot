from telegram import InlineKeyboardMarkup
from tg_bot.callbacks import Callback, CallbackButton
from utils import split_to_sublists
from demo_data.models import User, Cake, Shape, Berry, Topping, Decor
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
        if not cake.custom:
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


def get_select_layers(layers: dict):
    buttons = []

    for count, price in layers.items():
        button = CallbackButton(
            f'{count} за {price} р.',
            Callback.SAVE_LAYERS,
            layers=count
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_select_decor(decors: list[Decor]):
    buttons = []

    for decor in decors:
        button = CallbackButton(
            decor.title,
            Callback.ADD_DECOR,
            decor_pk=decor.pk
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_select_shape(shapes: list[Shape]):
    buttons = []

    for shape in shapes:
        button = CallbackButton(
            shape.title,
            Callback.ADD_SHAPE,
            shape_pk=shape.pk
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_select_topping(toppings: list[Topping]):
    buttons = []

    for topping in toppings:
        button = CallbackButton(
            topping.title,
            Callback.ADD_TOPPING,
            topping_pk=topping.pk
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_select_berry(berries: list[Berry]):
    buttons = []

    for berry in berries:
        button = CallbackButton(
            berry.title,
            Callback.ADD_BERRY,
            berry_pk=berry.pk
        )
        buttons.append(button)

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_confirm_create_cake():
    buttons = [
        static_buttons.SELECT_DECOR,
        static_buttons.SELECT_BERRY,
        static_buttons.ADD_SIGN
    ]

    buttons = split_to_sublists(buttons, 2)

    buttons.append([static_buttons.YES])
    buttons.append([static_buttons.MAIN_MENU])
    return InlineKeyboardMarkup(buttons)


def get_cake_created_menu():
    buttons = [
        static_buttons.SHOW_CART,
        static_buttons.MAIN_MENU
    ]

    buttons = split_to_sublists(buttons, 1)

    return InlineKeyboardMarkup(buttons)


def get_my_orders():
    pass
