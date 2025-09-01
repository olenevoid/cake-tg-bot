from enum import StrEnum, auto
from telegram import InlineKeyboardButton


NAME_SEPARATOR = '__'
PARAM_SEPARATOR = ','


class Callback(StrEnum):
    MAIN_MENU = auto()
    ORDER_CAKE = auto()
    SHOW_CAKES = auto()
    SHOW_CAKE = auto()
    SHOW_CART = auto()
    ADD_TO_CART = auto()
    REMOVE_FROM_CART = auto()
    CLEAR_CART = auto()
    CREATE_ORDER = auto()
    CREATE_CAKE = auto()
    SELECT_DATE = auto()
    ADD_DATE = auto()
    ADD_TIME = auto()
    ADD_PROMO = auto()
    ADD_COMMENT = auto()
    SELECT_LAYERS = auto()
    SAVE_LAYERS = auto()
    MY_ORDERS = auto()
    SHOW_PRICELIST = auto()
    SIGNUP = auto()
    ALL_ORDERS = auto()
    YES = auto()
    NO = auto()
    BACK = auto()
    REDO = auto()
    DOWNLOAD = auto()
    DELETE_USER = auto()


# Класс для создания строки коллбэков с параметрами 
class CallbackData:
    def __init__(self, name: Callback, params: dict = {}):
        self.name: Callback = name
        self.params: dict = params

    @property
    def param_string(self,) -> str:
        if not self.params:
            return ''

        param_string = ''
        for name, value in self.params.items():
            param_string += f'{name}={value}{PARAM_SEPARATOR}'

        return param_string

    def to_str(self) -> str:
        if self.param_string:
            return f'{self.name.value}{NAME_SEPARATOR}{self.param_string}'

        return self.name.value


# Кнопка бота для коллбеков с параметрами
class CallbackButton(InlineKeyboardButton):
    def __init__(self, text: str, callback_name: Callback, **params):

        callback_data = CallbackData(callback_name, params).to_str()

        super().__init__(
            text,
            callback_data=callback_data,
        )


def get_pattern(callback_name: Callback):
    return f'^({callback_name.value})(?:__.*)?$'


# Парсит строку в класс CallbackData
def parse_callback_data_string(callback_data: str) -> CallbackData:
    parsed_callback = callback_data.split(NAME_SEPARATOR)
    callback_name = Callback(parsed_callback[0])
    callback_params = {}

    if len(parsed_callback) > 1:
        param_pairs = parsed_callback[1].split(PARAM_SEPARATOR)

        for param_pair in param_pairs:
            if param_pair:
                name, value = _parse_param_pair(param_pair)
                callback_params[name] = value

    return CallbackData(callback_name, callback_params)


def _parse_param_pair(param_pair: str) -> tuple:
    name, value = param_pair.split('=')

    if value.isnumeric():
        value = int(value)

    return (name, value)
