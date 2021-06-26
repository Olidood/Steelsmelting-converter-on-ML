from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import pymysql.cursors
from csv import reader
import tkinter as tk
from tkinter import filedialog
import numpy as np
import hashlib
from adminintls import Ui_AdminForm


def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

class AdminForm(QtWidgets.QMainWindow):
    def __init__(self, parent):
        #Конструктор класса
        super(AdminForm, self).__init__()
        #Инициализвация формы авторизации
        self.ui = Ui_AdminForm()
        self.ui.setupUi(self)
        self.initUI()
        self.returnToParent = parent
        self.inputOk = False
        self.outputOk = False

    #Ставим название окна и иконку
    def initUI(self):
        self.setWindowTitle('Администрирование')
        self.setWindowIcon(QIcon('icon.png'))
        #Инициализиуем клик листенеры
        self.ui.inAddBtn.clicked.connect(self.AddDataToInputsTable)
        self.ui.inDeleteBtn.clicked.connect(self.DeleteDataFromInputsTable)
        self.ui.inChangeBtn.clicked.connect(self.ChangeInputsTable)
        self.ui.inConfirmChangeBtn.clicked.connect(self.ConfirmChangeInputsTable)

        self.ui.outAddBtn.clicked.connect(self.AddDataToOutputsTable)
        self.ui.outDeleteBtn.clicked.connect(self.DeleteDataFromOutputsTable)
        self.ui.outChangeBtn.clicked.connect(self.ChangeOutputsTable)
        self.ui.outConfirmChangeBtn.clicked.connect(self.ConfirmChangeOutputsTable)

        self.ui.usersAddBtn.clicked.connect(self.AddDataToUsersTable)
        self.ui.usersDeleteBtn.clicked.connect(self.DeleteDataFromUsersTable)
        self.ui.usersChangeBtn.clicked.connect(self.ChangeUsersTable)
        self.ui.usersConfirmChangeBtn.clicked.connect(self.ConfirmChangeUsersTable)

        self.ui.pushButton_outadmin.clicked.connect(self.Logout)
        self.ui.pushButton_outadmin_2.clicked.connect(self.Logout)
        self.ui.pushButton_outadmin_3.clicked.connect(self.Logout)

        self.ui.pushButtonInFile.clicked.connect(self.OpenFileIn)
        self.ui.pushButtonOutFile.clicked.connect(self.OpenFileOut)

        self.LoadInputsFromDBToTable()
        self.LoadOutputsFromDBToTable()
        self.LoadUsersFromDBToTable()

    def LoadInputsFromDBToTable(self):
        connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
        cursor = connection.cursor()
        query = ("SELECT * FROM input_params")

        cursor.execute(query)

        if cursor.rowcount != 0:
            data = list()
            data.extend(cursor.fetchall())
            for row in data:
                rowPosition = self.ui.inputTable.rowCount()
                self.ui.inputTable.insertRow(rowPosition)
                colIterator = 0
                for col in row:
                    self.ui.inputTable.setItem(rowPosition, colIterator, QTableWidgetItem(str(round(col, 3))))
                    colIterator += 1

        cursor.close()
        connection.close()

    def LoadOutputsFromDBToTable(self):
        connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
        cursor = connection.cursor()
        query = ("SELECT * FROM output_params")

        cursor.execute(query)

        if cursor.rowcount != 0:
            data = list()
            data.extend(cursor.fetchall())
            for row in data:
                rowPosition = self.ui.outputTable.rowCount()
                self.ui.outputTable.insertRow(rowPosition)
                colIterator = 0
                for col in row:
                    self.ui.outputTable.setItem(rowPosition, colIterator, QTableWidgetItem(str(round(col, 3))))
                    colIterator += 1

        cursor.close()
        connection.close()

    def LoadUsersFromDBToTable(self):
        connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
        cursor = connection.cursor()
        query = ("SELECT * FROM users")

        cursor.execute(query)

        if cursor.rowcount != 0:
            data = list()
            data.extend(cursor.fetchall())
            for row in data:
                rowPosition = self.ui.usersTable.rowCount()
                self.ui.usersTable.insertRow(rowPosition)
                colIterator = 0
                for col in row:
                    self.ui.usersTable.setItem(rowPosition, colIterator, QTableWidgetItem(str(col)))
                    colIterator += 1

        cursor.close()
        connection.close()

    def AddDataToInputsTable(self):
        self.inputOk = True
        self.AddCheck()

    def AddDataToOutputsTable(self):
        self.outputOk = True
        self.AddCheck()


    def AddCheck(self):

        if self.inputOk & self.outputOk:
            #входные
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("Вы хотите добавить данные?")
            msg.setWindowTitle("Добавление!")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg.exec_()

            if result == QMessageBox.Yes:
                try:
                    connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                    cursor = connection.cursor()
                    query = (
                        "INSERT INTO input_params (weight_chugun, temperature_chugun, si_weight_percent, mn_weight_percent, c_weight_percent, p_weight_percent, "
                        "s_weiht_percent, weight_lom, si_lom_weight_percent, mn_lom_weight_percent, c_lom_weight_percent, p_lom_weight_percent,"
                        " s_lom_weight_percent, flus_1, flus_2, flus_3, flus_4, mixer_slag, v_d, t_d) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

                    Gch = float(self.ui.chugunWeightLE.text())
                    Tch = float(self.ui.temperatureCugunLE.text())
                    SIch = float(self.ui.inChugunSiLE.text())
                    MNch = float(self.ui.inChugunMnLE.text())
                    Cch = float(self.ui.inChugunCLE.text())
                    Pch = float(self.ui.inChugunPLE.text())
                    Sch = float(self.ui.inChugunSLE.text())
                    GNm = float(self.ui.metalWeightLE.text())
                    SIm = float(self.ui.inMetalSiLE.text())
                    MNm = float(self.ui.inMetalMnLE.text())
                    Cm = float(self.ui.inMetalCLE.text())
                    Pm = float(self.ui.inMetalPLE.text())
                    Sm = float(self.ui.inMetalSLE.text())
                    F1 = float(self.ui.flus1LE.text())
                    F2 = float(self.ui.flus2LE.text())
                    F3 = float(self.ui.flus3LE.text())
                    F4 = float(self.ui.flus4LE.text())
                    Gmsh = float(self.ui.inMixerSlugLE.text())
                    Vd = float(self.ui.inVdutLE.text())
                    Td = float(self.ui.inVremDutLE.text())
                    tst = list()
                    tryPerc =list()

                    MeW = float(self.ui.outMeWeightLE.text())
                    MeT = float(self.ui.outTempMeLE.text())
                    MeSi = float(self.ui.outMeWPSiLE.text())
                    MeMn = float(self.ui.outMeWPMnLE.text())
                    MeC = float(self.ui.outMeWPCLE.text())
                    MeP = float(self.ui.outMeWPPLE.text())
                    MeS = float(self.ui.outMeWPSLE.text())
                    MeManufacturingTime = float(self.ui.outManufactureMetallTime.text())
                    SW = float(self.ui.outSlugWeightLE.text())
                    SCaO = float(self.ui.outSlugWPCaOLE.text())
                    SSiO2 = float(self.ui.outSlugWPSiO2LE.text())
                    SMgO = float(self.ui.outSlugWPMgOLE.text())
                    SFeO = float(self.ui.outSlugWPFeOLE.text())
                    SAl2O3 = float(self.ui.outSlugWPAl2O3LE.text())
                    SMnO = float(self.ui.outSlugWPMnOLE.text())
                    SP2O5 = float(self.ui.outSlugWPP2O5LE.text())
                    SS = float(self.ui.outSlugWPSLE.text())
                    tstout = list()

                    try:
                        tst.append([Gch, Tch, SIch, MNch, Cch, Pch, Sch, GNm, SIm, MNm, Cm, Pm, Sm, F1, F2, F3, F4, Gmsh, Vd, Td])
                        tt = tst[0]
                        for a in range(len(tt)):
                            if tt[a] < 0:
                                raise Exception
                        """tryPerc.append([SIch, MNch, Cch, Pch, Sch, SIm, MNm, Cm, Pm, Sm])
                        tryPerc = tryPerc[0]
                        for b in range(len(tryPerc)):
                            if tryPerc[b] > 100:
                                raise Exception"""
                    except Exception:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Данные не могут быть меньше 0, проценты не могут быть больше 100")
                        msg.setWindowTitle("Ошибка!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        retval = msg.exec_()
                        return

                    try:
                        tstout.append(
                            [MeW, MeT, MeSi, MeMn, MeC, MeP, MeS, MeManufacturingTime, SW, SCaO, SSiO2, SMgO, SFeO,
                             SAl2O3, SMnO, SP2O5, SS])
                        tto = tstout[0]
                        for i in range(len(tto)):
                            if tto[i] < 0:
                                raise Exception
                        tryPerc.append([MeSi, MeMn, MeC, MeP, MeS, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS])
                        tryPerc = tryPerc[0]
                        for b in range(len(tryPerc)):
                            if tryPerc[b] > 100:
                                raise Exception
                    except Exception:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Данные не могут быть меньше 0, проценты не могут быть больше 100")
                        msg.setWindowTitle("Ошибка!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        retval = msg.exec_()
                        return
                    """
                    try:
                        tryPerc.append([MeSi, MeMn, MeC, MeP, MeS, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS])
                        tryPerc = tryPerc[0]
                        for b in range(len(tryPerc)):
                            if tryPerc[b] > 100:
                                raise Exception

                    except Exception:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Проценты не могут быть больше 100")
                        msg.setWindowTitle("Ошибка!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        retval = msg.exec_()
                        return"""
                    cursor.execute(query, (Gch, Tch, SIch, MNch, Cch, Pch, Sch, GNm, SIm, MNm, Cm, Pm, Sm, F1, F2, F3, F4, Gmsh, Vd, Td))

                    rowPosition = self.ui.inputTable.rowCount()
                    self.ui.inputTable.insertRow(rowPosition)
                    self.ui.inputTable.setItem(rowPosition, 1, QTableWidgetItem(str(Gch)))
                    self.ui.inputTable.setItem(rowPosition, 2, QTableWidgetItem(str(Tch)))
                    self.ui.inputTable.setItem(rowPosition, 3, QTableWidgetItem(str(SIch)))
                    self.ui.inputTable.setItem(rowPosition, 4, QTableWidgetItem(str(MNch)))
                    self.ui.inputTable.setItem(rowPosition, 5, QTableWidgetItem(str(Cch)))
                    self.ui.inputTable.setItem(rowPosition, 6, QTableWidgetItem(str(Pch)))
                    self.ui.inputTable.setItem(rowPosition, 7, QTableWidgetItem(str(Sch)))
                    self.ui.inputTable.setItem(rowPosition, 8, QTableWidgetItem(str(GNm)))
                    self.ui.inputTable.setItem(rowPosition, 9, QTableWidgetItem(str(SIm)))
                    self.ui.inputTable.setItem(rowPosition, 10, QTableWidgetItem(str(MNm)))
                    self.ui.inputTable.setItem(rowPosition, 11, QTableWidgetItem(str(Cm)))
                    self.ui.inputTable.setItem(rowPosition, 12, QTableWidgetItem(str(Pm)))
                    self.ui.inputTable.setItem(rowPosition, 13, QTableWidgetItem(str(Sm)))
                    self.ui.inputTable.setItem(rowPosition, 14, QTableWidgetItem(str(F1)))
                    self.ui.inputTable.setItem(rowPosition, 15, QTableWidgetItem(str(F2)))
                    self.ui.inputTable.setItem(rowPosition, 16, QTableWidgetItem(str(F3)))
                    self.ui.inputTable.setItem(rowPosition, 17, QTableWidgetItem(str(F4)))
                    self.ui.inputTable.setItem(rowPosition, 18, QTableWidgetItem(str(Gmsh)))
                    self.ui.inputTable.setItem(rowPosition, 19, QTableWidgetItem(str(Vd)))
                    self.ui.inputTable.setItem(rowPosition, 20, QTableWidgetItem(str(Td)))

                    connection.commit()

                    query = ("SELECT max(idinput_params) FROM input_params")
                    cursor.execute(query)
                    maxId = cursor.fetchone()
                    self.ui.inputTable.setItem(rowPosition, 0, QTableWidgetItem(str(maxId[0])))

                    cursor.close()
                    connection.close()


            #выходные
                    connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                    cursor = connection.cursor()
                    query = (
                        "INSERT INTO output_params (metal_weight, metal_temperature, si_metal_weight_percent, mn_metal_weight_percent, c_metal_weight_percent, "
                        "p_metal_weight_percent, s_metal_weight_percent, metal_output_time, slag_weight, cao_slag_weight_percent, "
                        "sio2_slag_weight_percent, mgo_slag_weight_percent, feo_slag_weight_percent, al2o3_slag_weight_percent, "
                        "mno_slag_weight_percent, p2o5_slag_weight_percent, s_slag_weight_percent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")



                    cursor.execute(query, (MeW, MeT, MeSi, MeMn, MeC, MeP, MeS, MeManufacturingTime, SW, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS))

                    rowPosition = self.ui.outputTable.rowCount()
                    self.ui.outputTable.insertRow(rowPosition)
                    self.ui.outputTable.setItem(rowPosition, 1, QTableWidgetItem(str(MeW)))
                    self.ui.outputTable.setItem(rowPosition, 2, QTableWidgetItem(str(MeT)))
                    self.ui.outputTable.setItem(rowPosition, 3, QTableWidgetItem(str(MeSi)))
                    self.ui.outputTable.setItem(rowPosition, 4, QTableWidgetItem(str(MeMn)))
                    self.ui.outputTable.setItem(rowPosition, 5, QTableWidgetItem(str(MeC)))
                    self.ui.outputTable.setItem(rowPosition, 6, QTableWidgetItem(str(MeP)))
                    self.ui.outputTable.setItem(rowPosition, 7, QTableWidgetItem(str(MeS)))
                    self.ui.outputTable.setItem(rowPosition, 8, QTableWidgetItem(str(MeManufacturingTime)))
                    self.ui.outputTable.setItem(rowPosition, 9, QTableWidgetItem(str(SW)))
                    self.ui.outputTable.setItem(rowPosition, 10, QTableWidgetItem(str(SCaO)))
                    self.ui.outputTable.setItem(rowPosition, 11, QTableWidgetItem(str(SSiO2)))
                    self.ui.outputTable.setItem(rowPosition, 12, QTableWidgetItem(str(SMgO)))
                    self.ui.outputTable.setItem(rowPosition, 13, QTableWidgetItem(str(SFeO)))
                    self.ui.outputTable.setItem(rowPosition, 14, QTableWidgetItem(str(SAl2O3)))
                    self.ui.outputTable.setItem(rowPosition, 15, QTableWidgetItem(str(SMnO)))
                    self.ui.outputTable.setItem(rowPosition, 16, QTableWidgetItem(str(SP2O5)))
                    self.ui.outputTable.setItem(rowPosition, 17, QTableWidgetItem(str(SS)))

                    connection.commit()

                    query = ("SELECT max(idoutput_params) FROM output_params")
                    cursor.execute(query)
                    maxId = cursor.fetchone()
                    self.ui.outputTable.setItem(rowPosition, 0, QTableWidgetItem(str(maxId[0])))

                    cursor.close()
                    connection.close()
                except Exception:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Ошибка!")
                    msg.setInformativeText("Ошибка!")
                    msg.setWindowTitle("Ошибка!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Данные добавлены")
                msg.setWindowTitle("Успех!")
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()

            self.inputOk = False
            self.outputOk = False
        elif self.inputOk:
            #ругаться что бы ввели оутпут
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Введите выходные данные!")
            msg.setInformativeText("Введите данные в таблицу выходных параметров и нажмите там кнопку 'Добавить' !")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        elif self.outputOk:
            # ввести инпут
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Введите входные данные!")
            msg.setInformativeText("Введите данные в таблицу входных параметров и нажмите там кнопку 'Добавить' !")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

    def AddDataToUsersTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите добавить данные?")
        msg.setWindowTitle("Добавление!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                query = ("INSERT INTO users (username, password, role) VALUES (%s, %s, %s);")

                username = self.ui.usersUserNameLE.text()
                password = self.ui.usersPasswordLE.text()
                userRole = self.ui.usersRoleLE.text()
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                cursor.execute(query, (username, password, userRole))

                rowPosition = self.ui.usersTable.rowCount()
                self.ui.usersTable.insertRow(rowPosition)
                self.ui.usersTable.setItem(rowPosition, 1, QTableWidgetItem(str(username)))
                self.ui.usersTable.setItem(rowPosition, 2, QTableWidgetItem(str(password)))
                self.ui.usersTable.setItem(rowPosition, 3, QTableWidgetItem(str(userRole)))

                connection.commit()

                query = ("SELECT max(idusers) FROM users")
                cursor.execute(query)
                maxId = cursor.fetchone()
                self.ui.usersTable.setItem(rowPosition, 0, QTableWidgetItem(str(maxId[0])))

                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные добавлены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def DeleteDataFromInputsTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите удалить данные?\n Данные с этим id будут удалены из обеих таблиц")
        msg.setWindowTitle("Удаление!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                index = self.ui.inputTable.currentRow().__int__()
                deleteId = int(self.ui.inputTable.item(index, 0).text())

                query = ("DELETE FROM input_params WHERE idinput_params=%s")
                query2 = ("DELETE FROM output_params WHERE idoutput_params=%s")

                cursor.execute(query, str(int(deleteId)))
                cursor.execute(query2, str(int(deleteId)))

                self.ui.outputTable.removeRow(index)
                self.ui.inputTable.removeRow(index)

                connection.commit()
                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные удалены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def DeleteDataFromOutputsTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите удалить данные?\n Данные с этим id будут удалены из обеих таблиц")
        msg.setWindowTitle("Удаление!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                index = self.ui.outputTable.currentRow().__int__()
                deleteId = int(self.ui.outputTable.item(index, 0).text())

                query = ("DELETE FROM output_params WHERE idoutput_params=%s")
                query2 = ("DELETE FROM input_params WHERE idinput_params=%s")

                cursor.execute(query, str(int(deleteId)))
                cursor.execute(query2, str(int(deleteId)))

                self.ui.outputTable.removeRow(index)
                self.ui.inputTable.removeRow(index)


                connection.commit()
                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные удалены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()



    def DeleteDataFromUsersTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите удалить данные?")
        msg.setWindowTitle("Удаление!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                index = self.ui.usersTable.currentRow().__int__()
                deleteId = int(self.ui.usersTable.item(index, 0).text())

                query = ("DELETE FROM users WHERE idusers=%s")

                cursor.execute(query, str(int(deleteId)))

                self.ui.usersTable.removeRow(index)

                connection.commit()
                cursor.close()
                connection.close()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Данные удалены")
                msg.setWindowTitle("Успех!")
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

    def ChangeInputsTable(self):
        try:
            index = self.ui.inputTable.currentRow().__int__()
            Gch = self.ui.inputTable.item(index, 1).text()
            Tch = self.ui.inputTable.item(index, 2).text()
            SIch = self.ui.inputTable.item(index, 3).text()
            MNch = self.ui.inputTable.item(index, 4).text()
            Cch = self.ui.inputTable.item(index, 5).text()
            Pch = self.ui.inputTable.item(index, 6).text()
            Sch = self.ui.inputTable.item(index, 7).text()
            GNm = self.ui.inputTable.item(index, 8).text()
            SIm = self.ui.inputTable.item(index, 9).text()
            MNm = self.ui.inputTable.item(index, 10).text()
            Cm = self.ui.inputTable.item(index, 11).text()
            Pm = self.ui.inputTable.item(index, 12).text()
            Sm = self.ui.inputTable.item(index, 13).text()
            F1 = self.ui.inputTable.item(index, 14).text()
            F2 = self.ui.inputTable.item(index, 15).text()
            F3 = self.ui.inputTable.item(index, 16).text()
            F4 = self.ui.inputTable.item(index, 17).text()
            Gmsh = self.ui.inputTable.item(index, 18).text()
            Vd = self.ui.inputTable.item(index, 19).text()
            Td = self.ui.inputTable.item(index, 20).text()

            self.ui.chugunWeightLE.setText(Gch)
            self.ui.temperatureCugunLE.setText(Tch)
            self.ui.inChugunSiLE.setText(SIch)
            self.ui.inChugunMnLE.setText(MNch)
            self.ui.inChugunCLE.setText(Cch)
            self.ui.inChugunPLE.setText(Pch)
            self.ui.inChugunSLE.setText(Sch)
            self.ui.metalWeightLE.setText(GNm)
            self.ui.inMetalSiLE.setText(SIm)
            self.ui.inMetalMnLE.setText(MNm)
            self.ui.inMetalCLE.setText(Cm)
            self.ui.inMetalPLE.setText(Pm)
            self.ui.inMetalSLE.setText(Sm)
            self.ui.flus1LE.setText(F1)
            self.ui.flus2LE.setText(F2)
            self.ui.flus3LE.setText(F3)
            self.ui.flus4LE.setText(F4)
            self.ui.inMixerSlugLE.setText(Gmsh)
            self.ui.inVdutLE.setText(Vd)
            self.ui.inVremDutLE.setText(Td)
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка!")
            msg.setInformativeText("Ошибка!")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return


    def ChangeOutputsTable(self):
        try:
            index = self.ui.outputTable.currentRow().__int__()
            MeW = self.ui.outputTable.item(index, 1).text()
            MeT = self.ui.outputTable.item(index, 2).text()
            MeSi = self.ui.outputTable.item(index, 3).text()
            MeMn = self.ui.outputTable.item(index, 4).text()
            MeC = self.ui.outputTable.item(index, 5).text()
            MeP = self.ui.outputTable.item(index, 6).text()
            MeS = self.ui.outputTable.item(index, 7).text()
            MeManufacturingTime = self.ui.outputTable.item(index, 8).text()
            SW = self.ui.outputTable.item(index, 9).text()
            SCaO = self.ui.outputTable.item(index, 10).text()
            SSiO2 = self.ui.outputTable.item(index, 11).text()
            SMgO = self.ui.outputTable.item(index, 12).text()
            SFeO = self.ui.outputTable.item(index, 13).text()
            SAl2O3 = self.ui.outputTable.item(index, 14).text()
            SMnO = self.ui.outputTable.item(index, 15).text()
            SP2O5 = self.ui.outputTable.item(index, 16).text()
            SS = self.ui.outputTable.item(index, 17).text()

            self.ui.outMeWeightLE.setText(MeW)
            self.ui.outTempMeLE.setText(MeT)
            self.ui.outMeWPSiLE.setText(MeSi)
            self.ui.outMeWPMnLE.setText(MeMn)
            self.ui.outMeWPCLE.setText(MeC)
            self.ui.outMeWPPLE.setText(MeP)
            self.ui.outMeWPSLE.setText(MeS)
            self.ui.outManufactureMetallTime.setText(MeManufacturingTime)
            self.ui.outSlugWeightLE.setText(SW)
            self.ui.outSlugWPCaOLE.setText(SCaO)
            self.ui.outSlugWPSiO2LE.setText(SSiO2)
            self.ui.outSlugWPMgOLE.setText(SMgO)
            self.ui.outSlugWPFeOLE.setText(SFeO)
            self.ui.outSlugWPAl2O3LE.setText(SAl2O3)
            self.ui.outSlugWPMnOLE.setText(SMnO)
            self.ui.outSlugWPP2O5LE.setText(SP2O5)
            self.ui.outSlugWPSLE.setText(SS)
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка!")
            msg.setInformativeText("Ошибка!")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return


    def ChangeUsersTable(self):
        try:
            index = self.ui.usersTable.currentRow().__int__()
            change = int(self.ui.usersTable.item(index, 0).text())
            newUserName = self.ui.usersTable.item(index, 1).text()
            newPassword = self.ui.usersTable.item(index, 2).text()
            newRole = self.ui.usersTable.item(index, 3).text()

            self.ui.usersUserNameLE.setText(newUserName)
            self.ui.usersPasswordLE.setText(newPassword)
            self.ui.usersRoleLE.setText(newRole)
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка!")
            msg.setInformativeText("Ошибка!")
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

    def ConfirmChangeInputsTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите изменить данные?")
        msg.setWindowTitle("Измененин!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                query = ("UPDATE input_params SET weight_chugun=%s, temperature_chugun=%s, si_weight_percent=%s, mn_weight_percent=%s, c_weight_percent=%s, p_weight_percent=%s, "
                         "s_weiht_percent=%s, weight_lom=%s, si_lom_weight_percent=%s, mn_lom_weight_percent=%s, c_lom_weight_percent=%s, p_lom_weight_percent=%s,"
                         " s_lom_weight_percent=%s, flus_1=%s, flus_2=%s, flus_3=%s, flus_4=%s, mixer_slag=%s, v_d=%s, t_d=%s WHERE idinput_params=%s;")

                Gch = float(self.ui.chugunWeightLE.text())
                Tch = float(self.ui.temperatureCugunLE.text())
                SIch = float(self.ui.inChugunSiLE.text())
                MNch = float(self.ui.inChugunMnLE.text())
                Cch = float(self.ui.inChugunCLE.text())
                Pch = float(self.ui.inChugunPLE.text())
                Sch = float(self.ui.inChugunSLE.text())
                GNm = float(self.ui.metalWeightLE.text())
                SIm = float(self.ui.inMetalSiLE.text())
                MNm = float(self.ui.inMetalMnLE.text())
                Cm = float(self.ui.inMetalCLE.text())
                Pm = float(self.ui.inMetalPLE.text())
                Sm = float(self.ui.inMetalSLE.text())
                F1 = float(self.ui.flus1LE.text())
                F2 = float(self.ui.flus2LE.text())
                F3 = float(self.ui.flus3LE.text())
                F4 = float(self.ui.flus4LE.text())
                Gmsh = float(self.ui.inMixerSlugLE.text())
                Vd = float(self.ui.inVdutLE.text())
                Td = float(self.ui.inVremDutLE.text())
                index = self.ui.inputTable.currentRow().__int__()
                inId = int(self.ui.inputTable.item(index, 0).text())
                tst = list()
                tryPerc = list()
                try:
                    tst.append(
                        [Gch, Tch, SIch, MNch, Cch, Pch, Sch, GNm, SIm, MNm, Cm, Pm, Sm, F1, F2, F3, F4, Gmsh, Vd, Td, inId])
                    tt = tst[0]
                    for a in range(len(tt)):
                        if tt[a] < 0:
                            raise Exception
                    tryPerc.append([SIch, MNch, Cch, Pch, Sch, SIm, MNm, Cm, Pm, Sm])
                    tryPerc = tryPerc[0]
                    for b in range(len(tryPerc)):
                        if tryPerc[b] > 100:
                            raise Exception
                except Exception:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Данные не могут быть меньше 0, процент не может быть больше 100")
                    msg.setWindowTitle("Ошибка!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()
                    return
                cursor.execute(query, (Gch, Tch, SIch, MNch, Cch, Pch, Sch, GNm, SIm, MNm, Cm, Pm, Sm, F1, F2, F3, F4, Gmsh, Vd, Td, inId))

                self.ui.inputTable.item(index, 1).setText(str(Gch))
                self.ui.inputTable.item(index, 2).setText(str(Tch))
                self.ui.inputTable.item(index, 3).setText(str(SIch))
                self.ui.inputTable.item(index, 4).setText(str(MNch))
                self.ui.inputTable.item(index, 5).setText(str(Cch))
                self.ui.inputTable.item(index, 6).setText(str(Pch))
                self.ui.inputTable.item(index, 7).setText(str(Sch))
                self.ui.inputTable.item(index, 8).setText(str(GNm))
                self.ui.inputTable.item(index, 9).setText(str(SIm))
                self.ui.inputTable.item(index, 10).setText(str(MNm))
                self.ui.inputTable.item(index, 11).setText(str(Cm))
                self.ui.inputTable.item(index, 12).setText(str(Pm))
                self.ui.inputTable.item(index, 13).setText(str(Sm))
                self.ui.inputTable.item(index, 14).setText(str(F1))
                self.ui.inputTable.item(index, 15).setText(str(F2))
                self.ui.inputTable.item(index, 16).setText(str(F3))
                self.ui.inputTable.item(index, 17).setText(str(F4))
                self.ui.inputTable.item(index, 18).setText(str(Gmsh))
                self.ui.inputTable.item(index, 19).setText(str(Vd))
                self.ui.inputTable.item(index, 20).setText(str(Td))

                connection.commit()
                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные изменены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def ConfirmChangeOutputsTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите изменить данные?")
        msg.setWindowTitle("Измененин!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                query = ("UPDATE output_params SET metal_weight=%s, metal_temperature=%s, si_metal_weight_percent=%s, mn_metal_weight_percent=%s, c_metal_weight_percent=%s, "
                          "p_metal_weight_percent=%s, s_metal_weight_percent=%s, metal_output_time=%s, slag_weight=%s, cao_slag_weight_percent=%s, "
                          "sio2_slag_weight_percent=%s, mgo_slag_weight_percent=%s, feo_slag_weight_percent=%s, al2o3_slag_weight_percent=%s, "
                          "mno_slag_weight_percent=%s, p2o5_slag_weight_percent=%s, s_slag_weight_percent=%s WHERE idoutput_params=%s;")

                MeW = float(self.ui.outMeWeightLE.text())
                MeT = float(self.ui.outTempMeLE.text())
                MeSi = float(self.ui.outMeWPSiLE.text())
                MeMn = float(self.ui.outMeWPMnLE.text())
                MeC = float(self.ui.outMeWPCLE.text())
                MeP = float(self.ui.outMeWPPLE.text())
                MeS = float(self.ui.outMeWPSLE.text())
                MeManufacturingTime = float(self.ui.outManufactureMetallTime.text())
                SW = float(self.ui.outSlugWeightLE.text())
                SCaO = float(self.ui.outSlugWPCaOLE.text())
                SSiO2 = float(self.ui.outSlugWPSiO2LE.text())
                SMgO = float(self.ui.outSlugWPMgOLE.text())
                SFeO = float(self.ui.outSlugWPFeOLE.text())
                SAl2O3 = float(self.ui.outSlugWPAl2O3LE.text())
                SMnO = float(self.ui.outSlugWPMnOLE.text())
                SP2O5 = float(self.ui.outSlugWPP2O5LE.text())
                SS = float(self.ui.outSlugWPSLE.text())
                index = self.ui.outputTable.currentRow().__int__()
                outId = int(self.ui.outputTable.item(index, 0).text())
                tst = list()
                tryPerc = list()
                try:
                    tst.append(
                        [MeW, MeT, MeSi, MeMn, MeC, MeP, MeS, MeManufacturingTime, SW, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS, outId])
                    tt = tst[0]
                    for a in range(len(tt)):
                        if tt[a] < 0:
                            raise Exception
                    tryPerc.append([MeSi, MeMn, MeC, MeP, MeS, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS])
                    tryPerc = tryPerc[0]
                    for b in range(len(tryPerc)):
                        if tryPerc[b] > 100:
                            raise Exception
                except Exception:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Данные не могут быть меньше 0, процент не может быть больше 100")
                    msg.setWindowTitle("Ошибка!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()
                    return
                cursor.execute(query, (MeW, MeT, MeSi, MeMn, MeC, MeP, MeS, MeManufacturingTime, SW, SCaO, SSiO2, SMgO, SFeO, SAl2O3, SMnO, SP2O5, SS, outId))

                self.ui.outputTable.item(index, 1).setText(str(MeW))
                self.ui.outputTable.item(index, 2).setText(str(MeT))
                self.ui.outputTable.item(index, 3).setText(str(MeSi))
                self.ui.outputTable.item(index, 4).setText(str(MeMn))
                self.ui.outputTable.item(index, 5).setText(str(MeC))
                self.ui.outputTable.item(index, 6).setText(str(MeP))
                self.ui.outputTable.item(index, 7).setText(str(MeS))
                self.ui.outputTable.item(index, 8).setText(str(MeManufacturingTime))
                self.ui.outputTable.item(index, 9).setText(str(SW))
                self.ui.outputTable.item(index, 10).setText(str(SCaO))
                self.ui.outputTable.item(index, 11).setText(str(SSiO2))
                self.ui.outputTable.item(index, 12).setText(str(SMgO))
                self.ui.outputTable.item(index, 13).setText(str(SFeO))
                self.ui.outputTable.item(index, 14).setText(str(SAl2O3))
                self.ui.outputTable.item(index, 15).setText(str(SMnO))
                self.ui.outputTable.item(index, 16).setText(str(SP2O5))
                self.ui.outputTable.item(index, 17).setText(str(SS))

                connection.commit()
                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные изменены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def ConfirmChangeUsersTable(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите изменить данные?")
        msg.setWindowTitle("Измененин!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            try:
                connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
                cursor = connection.cursor()
                query = ("UPDATE users SET username=%s, password=%s, role=%s WHERE idusers=%s;")

                username = self.ui.usersUserNameLE.text()
                password = self.ui.usersPasswordLE.text()
                userRole = self.ui.usersRoleLE.text()
                index = self.ui.usersTable.currentRow().__int__()
                userId = int(self.ui.usersTable.item(index, 0).text())
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                cursor.execute(query, (username, password, userRole, userId))

                self.ui.usersTable.item(index, 1).setText(str(username))
                self.ui.usersTable.item(index, 2).setText(str(password))
                self.ui.usersTable.item(index, 3).setText(str(userRole))

                connection.commit()
                cursor.close()
                connection.close()
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка!")
                msg.setInformativeText("Ошибка!")
                msg.setWindowTitle("Ошибка!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Данные изменены")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def Logout(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите выйти?")
        msg.setWindowTitle("Выйти!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()

        if result == QMessageBox.Yes:
            self.returnToParent.show()
            self.hide()



    def OpenFileIn(self):
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            dataset = load_csv(file_path)
            if len(dataset[0]) != 20:
                raise Exception
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Что-то пошло не так")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return

        for i in range(len(dataset[0])):
            str_column_to_float(dataset, i)
        test_target = np.array(dataset)
        test_target.reshape(1, 20)
        print(test_target)
        self.ui.chugunWeightLE.setText(str(test_target[0][0]))
        self.ui.temperatureCugunLE.setText(str(test_target[0][1]))
        self.ui.inChugunSiLE.setText(str(test_target[0][2]))
        self.ui.inChugunMnLE.setText(str(test_target[0][3]))
        self.ui.inChugunCLE.setText(str(test_target[0][4]))
        self.ui.inChugunPLE.setText(str(test_target[0][5]))
        self.ui.inChugunSLE.setText(str(test_target[0][6]))
        self.ui.metalWeightLE.setText(str(test_target[0][7]))
        self.ui.inMetalSiLE.setText(str(test_target[0][8]))
        self.ui.inMetalMnLE.setText(str(test_target[0][9]))
        self.ui.inMetalCLE.setText(str(test_target[0][10]))
        self.ui.inMetalPLE.setText(str(test_target[0][11]))
        self.ui.inMetalSLE.setText(str(test_target[0][12]))
        self.ui.flus1LE.setText(str(test_target[0][13]))
        self.ui.flus2LE.setText(str(test_target[0][14]))
        self.ui.flus3LE.setText(str(test_target[0][15]))
        self.ui.flus4LE.setText(str(test_target[0][16]))
        self.ui.inMixerSlugLE.setText(str(test_target[0][17]))
        self.ui.inVdutLE.setText(str(test_target[0][18]))
        self.ui.inVremDutLE.setText(str(test_target[0][19]))



        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Данные загружены")
        msg.setWindowTitle("Успех!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


    def OpenFileOut(self):
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            dataset = load_csv(file_path)
            if len(dataset[0]) != 17:
                raise Exception
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Что-то пошло не так")
            msg.setWindowTitle("Успех!")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            return


        for i in range(len(dataset[0])):
            str_column_to_float(dataset, i)
        test_target = np.array(dataset)
        test_target.reshape(1, 16)
        print(test_target)
        self.ui.outMeWeightLE.setText(str(test_target[0][0]))
        self.ui.outTempMeLE.setText(str(test_target[0][1]))
        self.ui.outMeWPSiLE.setText(str(test_target[0][2]))
        self.ui.outMeWPMnLE.setText(str(test_target[0][3]))
        self.ui.outMeWPCLE.setText(str(test_target[0][4]))
        self.ui.outMeWPPLE.setText(str(test_target[0][5]))
        self.ui.outMeWPSLE.setText(str(test_target[0][6]))
        self.ui.outManufactureMetallTime.setText(str(test_target[0][7]))
        self.ui.outSlugWeightLE.setText(str(test_target[0][8]))
        self.ui.outSlugWPCaOLE.setText(str(test_target[0][9]))
        self.ui.outSlugWPSiO2LE.setText(str(test_target[0][10]))
        self.ui.outSlugWPMgOLE.setText(str(test_target[0][11]))
        self.ui.outSlugWPFeOLE.setText(str(test_target[0][12]))
        self.ui.outSlugWPAl2O3LE.setText(str(test_target[0][13]))
        self.ui.outSlugWPMnOLE.setText(str(test_target[0][14]))
        self.ui.outSlugWPP2O5LE.setText(str(test_target[0][15]))
        self.ui.outSlugWPSLE.setText(str(test_target[0][16]))


        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Данные загружены")
        msg.setWindowTitle("Успех!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()