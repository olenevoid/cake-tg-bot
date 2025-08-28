from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from tg_bot.callbacks import Callback, get_pattern
from tg_bot.handlers.states import State
from tg_bot.handlers import main_menu, registration, order_cake


def get_order_cake_conversation_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                order_cake.show_cakes,
                get_pattern(Callback.SHOW_CAKES)
            )
        ],
        states={
            State.SHOW_CAKES: [
                CallbackQueryHandler(
                    order_cake.show_cake,
                    get_pattern(Callback.SHOW_CAKE)
                ),
            ],
        },
        map_to_parent={
            State.MAIN_MENU: State.MAIN_MENU
        },
        fallbacks=[
            CommandHandler("start", main_menu.start),
            CallbackQueryHandler(
                main_menu.show_main_menu,
                get_pattern(Callback.MAIN_MENU)
            )
        ]
    )


def get_registration_conversation_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                main_menu.show_main_menu,
                get_pattern(Callback.NO)
            ),
            CallbackQueryHandler(
                registration.input_name,
                get_pattern(Callback.YES)
            ),
            CallbackQueryHandler(
                registration.send_personal_data_consent,
                Callback.DOWNLOAD
            )
        ],
        states={
            State.PERSONAL_DATA_PROCESSING: [
                CallbackQueryHandler(
                    main_menu.show_main_menu,
                    get_pattern(Callback.NO)
                ),
                CallbackQueryHandler(
                    registration.input_name,
                    get_pattern(Callback.YES)
                ),
                CallbackQueryHandler(
                    registration.send_personal_data_consent,
                    Callback.DOWNLOAD
                )
            ],
            State.INPUT_NAME: [
                MessageHandler(filters.TEXT, registration.validate_name),
            ],
            State.INPUT_PHONE: [
                MessageHandler(filters.TEXT, registration.validate_phone)
            ],
            State.INPUT_ADDRESS: [
                MessageHandler(filters.TEXT, registration.validate_address)
            ],
            State.CONFIRM_SIGNUP: [
                CallbackQueryHandler(
                    registration.signup_customer,
                    Callback.YES
                ),
                CallbackQueryHandler(registration.input_name, Callback.REDO)
            ]
        },
        map_to_parent={
            State.MAIN_MENU: State.MAIN_MENU
        },
        fallbacks=[
            CommandHandler("start", main_menu.start),
            CallbackQueryHandler(
                main_menu.show_main_menu,
                get_pattern(Callback.MAIN_MENU)
            )
        ]
    )


def get_main_conversation_handler():

    registration_level = get_registration_conversation_handler()
    order_cake_level = get_order_cake_conversation_handler()

    return ConversationHandler(
        entry_points=[
            CommandHandler("start", main_menu.start),
            CallbackQueryHandler(
                main_menu.show_main_menu,
                get_pattern(Callback.MAIN_MENU)
            )
        ],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(
                    main_menu.order_cake,
                    get_pattern(Callback.ORDER_CAKE)
                ),
                CallbackQueryHandler(
                    main_menu.show_pricelist,
                    get_pattern(Callback.SHOW_PRICELIST)
                ),
                CallbackQueryHandler(
                    main_menu.my_orders,
                    get_pattern(Callback.MY_ORDERS)
                ),
                CallbackQueryHandler(
                    registration.start_registration,
                    get_pattern(Callback.SIGNUP)
                ),
            ],
            State.REGISTRATION: [registration_level],
            State.ORDER_CAKE: [order_cake_level]

        },
        fallbacks=[
            CommandHandler("start", main_menu.start),
            CallbackQueryHandler(
                main_menu.show_main_menu,
                get_pattern(Callback.MAIN_MENU)
            ),
            CallbackQueryHandler(
                registration.delete_user,
                get_pattern(Callback.DELETE_USER)
            ),
        ]
    )
