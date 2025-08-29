from enum import Enum, auto


class State(Enum):
    MAIN_MENU = auto()
    REGISTRATION = auto()
    PERSONAL_DATA_PROCESSING = auto()
    INPUT_NAME = auto()
    INPUT_ADDRESS = auto()
    INPUT_PHONE = auto()
    CONFIRM_SIGNUP = auto()
    SHOW_CAKES = auto()
    SHOW_CAKE = auto()
    SHOW_CART = auto()
    ORDER_CAKE = auto()