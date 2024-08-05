"""
Файл с GUI классом главного окна
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    """
    GUI класс главного окна
    """

    def __init__(self):
        self.statusbar = None
        self.file = None
        self.menubar = None
        self.plainTextEdit = None
        self.gridLayout_2 = None
        self.centralwidget = None
        self.delete_file = None
        self.settings = None
        self.save = None
        self.open = None

    def setupUi(self, MainWindow):
        """
        Создание UI
        """
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(909, 569)
        MainWindow.setWindowTitle(u"Encrypad")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.open = QAction(MainWindow)
        self.open.setObjectName(u"open")
        self.save = QAction(MainWindow)
        self.save.setObjectName(u"save")
        self.settings = QAction(MainWindow)
        self.settings.setObjectName(u"settings")
        self.delete_file = QAction(MainWindow)
        self.delete_file.setObjectName(u"delete_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_2.addWidget(self.plainTextEdit, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 909, 21))
        self.file = QMenu(self.menubar)
        self.file.setObjectName(u"file")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.file.menuAction())
        self.file.addAction(self.open)
        self.file.addAction(self.save)
        self.file.addAction(self.delete_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Текст для объектов
        """
        self.open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.save.setText(
            QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None)
        )
        self.settings.setText(
            QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0438\u0442\u044c", None)
        )
        self.delete_file.setText(
            QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None)
        )
        self.file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        pass
