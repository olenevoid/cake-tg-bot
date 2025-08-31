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
ADD_PROMO = CallbackButton('Добавить промокод', Callback.ADD_PROMO)
ADD_COMMENT = CallbackButton('Добавить комментарий', Callback.ADD_COMMENT)
SELECT_DATE = CallbackButton('Изменить дату и время', Callback.SELECT_DATE)
CONFIRM_CREATE_ORDER = CallbackButton('Создать заказ', Callback.YES)
CUSTOM_CAKE = CallbackButton(
    'Сделать свой',
    Callback.CREATE_CAKE
)
DELETE_USER = CallbackButton(
    'Удалить пользователя (для тестов)',
    Callback.DELETE_USER
)
