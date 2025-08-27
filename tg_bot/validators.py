# Валидаторы для имени, номера телефона, адреса и т.д.


def is_phone(phone: str):
    #TODO: Добавить проверку, что введенный номер является корректным
    return len(phone) > 2


def is_valid_name(full_name: str):
    #TODO: Добавить проверку имени. Вполне возможно хватит проверки
    # на количество слов и отсутствие цифр
    return len(full_name) > 2


def is_address(address: str):
    #TODO: Наверное, можно вообще ничего не проверять, но пусть пока будет
    return len(address) > 2
