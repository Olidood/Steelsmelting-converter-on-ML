import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
import pymysql.cursors

from nnn import Network
from adminform import AdminForm
from authformui import Ui_AuthForm

import hashlib
# Точка входа в программу
class StartUpper(QtWidgets.QMainWindow):
    def __init__(self):
        #Конструктор класса
        super(StartUpper, self).__init__()
        #Инициализвация формы авторизации
        self.ui = Ui_AuthForm()
        self.ui.setupUi(self)
        self.initUI()
        #Инициализация форм пользователя и администратора
        self.dialogUser = Network(parent=self)
        self.dialogAdmin = AdminForm(parent=self)

    #Ставим название окна и иконку + задаем кликлисенер
    def initUI(self):
        self.setWindowTitle('Авторизация')
        self.setWindowIcon(QIcon('icon.png'))
        self.ui.pushButton.clicked.connect(self.authCheck)

    # Проверка логина + пароля
    def authCheck(self):
        try:
            #Заираем логин и пароль, введенные пользователем
            inUserName = self.ui.lineEdit.text()
            inPassword = self.ui.lineEdit_2.text()

            #Проверяем не были ли поля пустыми
            if inUserName == "":
                raise Exception
            elif inPassword == "":
                raise  Exception
            inPassword = hashlib.md5(inPassword.encode())
            inPassword = inPassword.hexdigest()
            inPassword = str(inPassword)
           # inPassword = ('admin')
            #оздаем подклбчение к базе данных и курсор(считыватель информации)
            connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
            cursor = connection.cursor()
            #Пишем запрос на нахождения пользователя в базе
            query = ("SELECT username, password, role FROM users WHERE username = %s")

            #Обрабатываем запрос
            cursor.execute(query, inUserName)

            #Если найден пользователь
            if cursor.rowcount != 0:
                #В цикле по найденным пользователям
                for (username, password, role) in cursor:
                    #Проверяем, малоли это админ
                    if role == "admin" and username == inUserName and password == inPassword:
                        self.dialogAdmin.show()
                        self.hide()
                    #Если это обычный пользователь и пароль верный, то запускаем его рабочее окно
                    elif role == "user" and username == inUserName and password == inPassword:
                        self.dialogUser.show()
                        self.hide()
                    #Если ничего из вышеперечисленного то
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Неправильный пароль")
                        msg.setInformativeText("Вы ввели неправильный пароль.")
                        msg.setWindowTitle("Ошибка!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
            #Если ошибки с подключением или запросом к БД
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Пользователь с данным именем не найден!")
                msg.setInformativeText("Возможно вы опечатались.")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

            #ЗАкрываем курсор и соединение
            cursor.close()
            connection.close()

        #Если пользователь ввел невалидные данные, буквы и прочее
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не валидные данные!")
            msg.setInformativeText("Возможно вы не ввели логин или пароль.")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            #return


#Запуск приложеия
app = QtWidgets.QApplication([])
application = StartUpper()
application.show()
sys.exit(app.exec())
