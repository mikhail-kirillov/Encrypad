"""
Файл с методом для работы с базой данных
"""
import sqlite3
from sqlite3 import OperationalError

DATABASE_PATH = 'files/database.db'
DATABASE_NOT_EXIST = 'База данных отсутствует'
ERROR_IN_REQUEST = 'Ошибка в запросе'


class DatabaseError(Exception):
    """
    Класс-заглушка для обработки ошибок в работе с БД
    """
    pass


def request(sql=None, read_flag=None):
    """
    Используется для запросов в базу данных
    :param sql: запрос (str)
    :param read_flag: флаг чтения (bool)
    :return: True/False/DatabaseError в случае успеха/неудачи/ошибки
    """
    try:
        connect = sqlite3.connect(DATABASE_PATH)
        cursor = connect.cursor()
    except OperationalError:
        raise DatabaseError(DATABASE_NOT_EXIST)
    try:
        if sql is not None:
            if read_flag:
                result = cursor.execute(sql).fetchall()
                cursor.close()
                connect.close()
                return result
            else:
                cursor.execute(sql)
                connect.commit()
                cursor.close()
                connect.close()
                return True
        return False
    except OperationalError:
        raise DatabaseError(ERROR_IN_REQUEST)
