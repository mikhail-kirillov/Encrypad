"""
Файл с классом главного окна
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QMainWindow, QMessageBox

from python.crypt import decrypt, encrypt
from python.database import DatabaseError
from python.file import File, FileError
from python.ui.main import Ui_MainWindow

DO_NOT_CHOOSE_PATH = 'Не указан путь файла'
CHOOSE_FILE = 'Выберите файл'
FILE_NOT_ENCRYPTED = 'Файл не является зашифрованным'
WRONG_PASSWORD = 'Неверный пароль'
ENTER_PASSWORD = "Введите пароль:"
OPEN_FILE = "Открытие файла"
CONFIRM_EDITS = "Подтверждение изменений"
WARNING_EDITS = "Вы собираетесь изменить файл!\nДля этого введите пароль:"
SAVE_FILE = 'Сохраните файл'
GOOD_DEL = 'Успешно удалено'
ERROR_DEL = 'При удалении произошла ошибка.'
DEL_MESSAGE = 'Удаление'
YOU_SERIOUSLY = 'Вы действительно хотите удалить файл?'
CANCEL = 'Отменено'
SAVED = 'Сохранено'
CREATE_FILE = 'Создание файла'


def except_hook(cls, exception, traceback):
    """
    Обработка вывода ошибок
    """
    sys.__excepthook__(cls, exception, traceback)


class Main(QMainWindow, Ui_MainWindow):
    """
    Класс главного окна
    """

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.file = File()
        self.open.triggered.connect(self.open_f)
        self.save.triggered.connect(self.save_f)
        self.delete_file.triggered.connect(self.delete_f)

    def open_window(self, text):
        """
        Окно ввода пароля
        :param text: текст из файла (str)
        """
        password, ok_button = QInputDialog.getText(self, OPEN_FILE, ENTER_PASSWORD)
        if ok_button:
            if self.file.check_password(password):
                self.set_plain_text(decrypt(text=text, password=password))
            else:
                self.set_status_bar(WRONG_PASSWORD)

    def delete_window(self):
        """
        Окно подтверждения удаления файла
        :return: True/False в случае удалить/оставить
        """
        button_answer = QMessageBox.question(
            self,
            DEL_MESSAGE,
            YOU_SERIOUSLY,
            QMessageBox.Ok,
            QMessageBox.Cancel
        )
        if button_answer == QMessageBox.Ok:
            return True
        if button_answer == QMessageBox.Cancel:
            return True

    def create_window(self):
        """
        Окно создания файла и ввода пароля
        """
        password, ok_button = QInputDialog.getText(self, CREATE_FILE, ENTER_PASSWORD)
        if ok_button:
            result = self.file.create(password)
            if result is True:
                self.file.write(encrypt(text=self.get_plain_text(), password=password))
            else:
                self.set_status_bar(result)

    def get_file_window(self, text):
        """
        Открытие окна выбора файла и запись его пути (чтение)
        :param text: текст заголовка (str)
        """
        self.file.set_path(QFileDialog.getOpenFileName(self, text)[0])

    def set_file_window(self, text):
        """
        Открытие окна выбора файла и запись его пути (сохранение)
        :param text: текст заголовка (str)
        """
        self.file.set_path(QFileDialog.getSaveFileName(self, text)[0])

    def get_plain_text(self):
        """
        Взять текст из текстового редактора
        :return: текст (str)
        """
        return self.plainTextEdit.toPlainText()

    def set_plain_text(self, text):
        """
        Установить текст в текстовый редактор
        :param text: текст (str)
        """
        self.plainTextEdit.setPlainText(text)

    def set_status_bar(self, text):
        """
        Установить текст в статус-бар
        :param text: текст (str)
        """
        self.statusbar.showMessage(text, 5000)

    def open_f(self):
        """
        Открытие файла
        :return: False в случае неудачи
        """
        self.get_file_window(CHOOSE_FILE)
        if self.file.get_path() is None:
            self.set_status_bar(DO_NOT_CHOOSE_PATH)
            self.file.set_path(None)
            return False
        try:
            text = self.file.read()
            if not text:
                self.set_status_bar(FILE_NOT_ENCRYPTED)
                self.file.set_path(None)
                return False
        except FileError as fe:
            self.set_status_bar(fe.__str__())
            self.file.set_path(None)
            return False
        try:
            result = self.file.check_sign()
        except DatabaseError:
            result = False
        if result:
            self.open_window(text)
        else:
            self.set_status_bar(FILE_NOT_ENCRYPTED)
            self.file.set_path(None)
            return False

    def save_f(self):
        """
        Сохранение файла
        """
        if self.file.get_path() is not None:
            password, ok_button = QInputDialog.getText(self, CONFIRM_EDITS, WARNING_EDITS)
            if ok_button and self.file.check_password(password):
                self.file.write(encrypt(text=self.get_plain_text(), password=password))
                self.set_status_bar(SAVED)
        else:
            self.set_file_window(SAVE_FILE)
            if self.file.path is not None:
                self.create_window()

    def delete_f(self):
        """
        Удаление файла
        """
        result = self.file.delete()
        if result is True:
            delete = self.delete_window()
            if delete:
                self.set_status_bar(GOOD_DEL)
                self.set_plain_text('')
                self.file.set_path(None)
            else:
                self.set_status_bar(CANCEL)
        else:
            self.set_status_bar(ERROR_DEL + ' ' + result)

    def keyPressEvent(self, event):
        """
        Обработка нажатия сочетания клавиш
        :param event: событие (event)
        """
        if int(event.modifiers()) == Qt.CTRL:
            if event.key() == Qt.Key_S:
                self.save_f()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
