from telegram import InlineKeyboardMarkup
from tg_bot.callbacks import Callback, CallbackButton
from utils import split_to_sublists
from demo_data.models import User, Cake


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


def get_order_cake():
    buttons = [
        CallbackButton(
            'Готовые торты',
            Callback.SHOW_CAKES
        ),
        CallbackButton(
            'Заказать новый (не работает)',
            Callback.MAIN_MENU
        )
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

    buttons.append(
        [
            CallbackButton(
                'В меню',
                Callback.MAIN_MENU
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


def get_cake_menu(cake: Cake):

    buttons = [
        CallbackButton(
            'Добавить в корзину',
            Callback.ADD_TO_CART,
            cake_pk=cake.pk
        ),
        CallbackButton(
            'Назад',
            Callback.SHOW_CAKES
        )
    ]

    buttons = split_to_sublists(buttons, 1)

    buttons.append(
        [
            CallbackButton(
                'В меню',
                Callback.MAIN_MENU
            )
        ]
    )

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

    buttons.append([static_buttons.CLEAR_CART])
    buttons.append([static_buttons.BACK])
    buttons.append([static_buttons.MAIN_MENU])

    return InlineKeyboardMarkup(buttons)


def get_my_orders():
    pass
