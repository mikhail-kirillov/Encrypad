"""
Файл с классами для работы с файлами
"""
import hashlib
import os

from python.database import request

HAVE_NOT_OPEN_FILE = 'Нет открытого файла'
FILE_DOES_NOT_EXIST = 'Файл не существует'
PASSWORD_DOES_EXIST = 'Пароль уже существует'
WRONG_FILE_FORMAT = 'Неверный формат файла'
FILE_NOT_OPENED = 'Вы не открыли ни одного файла'


def get_password(password):
    """
    Нормализация пароля
    :param password: пароль (str)
    :return: пароль (str)
    """
    return password.strip()


def get_hash(string):
    """
    Хеширование пароля
    :param string: пароль (str)
    :return: хэш (str)
    """
    return hashlib.sha256(string.encode()).hexdigest()


class File:
    """
    Класс для работы с файлами
    """

    def __init__(self, path=None):
        self.path = path
        self.sign = None

    def set_path(self, path):
        """
        Установка пути файла
        :param path: путь (str)
        """
        if path == '' or path is None:
            self.path = None
        else:
            self.path = path.strip()

    def set_sign(self, sign):
        """
        Установка сигнатуры файла
        :param sign: сигнатура (str)
        """
        if sign == '' or sign is None:
            self.sign = None
        else:
            self.sign = sign.strip()

    def get_path(self):
        """
        Взять путь файла
        :return: путь (str)
        """
        return self.path

    def get_sign(self):
        """
        Взять сигнатуру файла
        :return: сигнатура (str)
        """
        return self.sign

    def check_sign(self):
        """
        Проверка существования сигнатуры в БД
        :return: True/False в случае нахождения/неудачи
        """
        if len(
                request(
                    """SELECT * FROM signatures WHERE sign = '{sign}'""".format(sign=self.get_sign()),
                    read_flag=True
                )
        ) > 0:
            return True
        return False

    def check_password(self, password):
        """
        Проверка соответствия пароля файлу
        :param password: пароль (str)
        :return: True/False в случае успеха/неудачи
        """
        if len(
                request(
                    """SELECT * FROM signatures WHERE sign = '{sign}' 
                AND p_id = (SELECT id FROM passwords 
                WHERE hash = '{hash}')""".format(sign=self.get_sign(), hash=get_hash(get_password(password))),
                    read_flag=True
                )
        ) > 0:
            return True
        return False

    def create(self, password):
        """
        Создание записей о файле в БД
        :param password: пароль (str)
        :return: True/Str в случае успеха/неудачи
        """
        if len(
                request(
                    """SELECT id FROM passwords 
                WHERE hash = '{hash}'""".format(hash=get_hash(get_password(password))),
                    read_flag=True
                )
        ) > 0:
            return PASSWORD_DOES_EXIST
        else:
            self.set_sign(get_hash(get_password(password))[::2])
            request(
                """INSERT INTO passwords(hash) 
                VALUES('{hash}')""".format(hash=get_hash(get_password(password))),
                read_flag=False
            )
            request(
                """INSERT INTO signatures(p_id, sign) 
                VALUES((SELECT id FROM passwords WHERE hash = '{hash}'), 
                '{sign}')""".format(hash=get_hash(get_password(password)), sign=self.get_sign()),
                read_flag=False
            )
            return True

    def read(self):
        """
        Чтение файла
        :return: текст из файла/ошибка/False в случае успеха/неудачи/отсутствия пути
        """
        if self.path is not None:
            with open(self.path, 'r', encoding='utf-8') as file:
                try:
                    self.set_sign(file.readline())
                except UnicodeDecodeError:
                    raise FileError(WRONG_FILE_FORMAT)
                except FileNotFoundError:
                    raise FileError(FILE_NOT_OPENED)
                return ''.join(file.readlines()[:])
        return False

    def write(self, text):
        """
        Запись в файл
        :param text: текст (str)
        """
        if self.path is not None:
            with open(self.path, 'w', encoding='utf-8') as file:
                file.writelines(self.sign + '\n')
                file.writelines(text)

    def delete(self):
        """
        Удаление файла
        :return: True/текст в случае успеха/неудачи
        """
        if self.path is not None:
            if os.path.isfile(self.path):
                os.remove(self.path)
                request(
                    """DELETE from passwords 
                    WHERE id = (SELECT p_id from signatures 
                    WHERE sign = '{sign}')""".format(sign=self.get_sign()),
                    read_flag=False
                )
                request(
                    """DELETE from signatures 
                    WHERE sign = '{sign}'""".format(sign=self.get_sign()),
                    read_flag=False
                )
                return True
            else:
                return FILE_DOES_NOT_EXIST
        else:
            return HAVE_NOT_OPEN_FILE


class FileError(Exception):
    """
    Класс-заглушка для обработки ошибок в работе с файлами
    """
    pass
