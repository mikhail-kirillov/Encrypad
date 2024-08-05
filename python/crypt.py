"""
Использовать encrypt и decrypt
для шифрования и дешифровки соответственно
"""


def text_to_ord_list(text):
    """
    Создаёт из строки список с номерами
    :param text: строка текста (str)
    :return: список чисел (list)
    """
    return [ord(i) for i in text]


def ord_list_to_text(num_list):
    """
    Создаёт из списка бит строку
    :param num_list: список чисел (list)
    :return: строка (str)
    """
    return ''.join(chr(i) for i in num_list)


def function(text, password, crypt_flag=True):
    """
    Преобразует текст по данному паролю
    :param crypt_flag: шифрование/дешифровка (bool)
    :param text: текст (str)
    :param password: пароль (str)
    :return: преобразованный текст (str)
    """
    password_num_list = text_to_ord_list(password)
    text_num_list = text_to_ord_list(text)
    result = list()
    if crypt_flag:
        for i in range(len(text_num_list)):
            result.append(text_num_list[i] + password_num_list[i % len(password)])
    else:
        for i in range(len(text_num_list)):
            result.append(text_num_list[i] - password_num_list[i % len(password)])
    return ord_list_to_text(result)


def encrypt(text, password):
    """
    Шифрует текст по заданному паролю
    :param text: строка исходного текста (str)
    :param password: пароль (str)
    :return: строка зашифрованного текста (str)
    """
    return function(text, password)


def decrypt(text, password):
    """
    Дешифрует текст по заданному паролю
    :param text: строка (str)
    :param password: пароль (str)
    :return: строка исходного текста (str)
    """
    return function(text, password, False)
