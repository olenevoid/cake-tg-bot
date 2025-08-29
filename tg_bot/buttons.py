from tg_bot.callbacks import Callback, CallbackButton


MAIN_MENU = CallbackButton('В меню', Callback.MAIN_MENU)
SIGNUP = CallbackButton('Регистрация', Callback.SIGNUP)
ORDER_CAKE = CallbackButton('Заказать торт', Callback.ORDER_CAKE)
SHOW_PRICELIST = CallbackButton('Показать цены', Callback.SHOW_PRICELIST)
MY_ORDERS = CallbackButton('Мои заказы', Callback.MY_ORDERS)
ALL_ORDERS = CallbackButton('Заказы', Callback.ALL_ORDERS)
DOWNLOAD = CallbackButton('Скачать', Callback.DOWNLOAD)
YES = CallbackButton('Да', Callback.YES)
NO = CallbackButton('Нет', Callback.NO)
REDO = CallbackButton('Изменить',Callback.REDO)
SHOW_CAKES = CallbackButton('Готовые торты', Callback.SHOW_CAKES)
BACK = CallbackButton('Назад', Callback.BACK)
SHOW_CART = CallbackButton('Открыть корзину', Callback.SHOW_CART)
CLEAR_CART = CallbackButton('Очистить корзину', Callback.CLEAR_CART)
CREATE_ORDER = CallbackButton('Создать заказ', Callback.CREATE_ORDER)
CUSTOM_CAKE = CallbackButton(
    'Заказать новый (не работает)',
    Callback.MAIN_MENU
)
DELETE_USER = CallbackButton(
    'Удалить пользователя (для тестов)',
    Callback.DELETE_USER
)
