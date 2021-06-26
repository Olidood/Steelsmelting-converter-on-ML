# example of making predictions for a regression problem
import tkinter
from tkinter import messagebox

from PyQt5.QtWidgets import QMessageBox
from keras.models import Sequential
from keras.layers import Dense, LSTM

from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from csv import reader
import pylab
from keras import layers
from keras import models
import numpy as np
import matplotlib.pyplot as plt
from array import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import pymysql.cursors
from userlst import Ui_MainWindow
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import *
import fileinput
from sklearn import preprocessing




#оздаем 2 запроса на подключение к базе данных и 2 курсора курсор(считывателя информации) для входных и выходных параметров соответственно.
#Ну и запросы на выдачу всех полей, кроме ID
connection = pymysql.connect(user='BRPQBOaYj9', password='XD9adzf5Ow', host='remotemysql.com', database='BRPQBOaYj9')
inCursor = connection.cursor()
getAllInQuery = ("SELECT weight_chugun, temperature_chugun, si_weight_percent, mn_weight_percent, c_weight_percent, p_weight_percent, "
				 "s_weiht_percent, weight_lom, si_lom_weight_percent, mn_lom_weight_percent, c_lom_weight_percent, p_lom_weight_percent,"
				 " s_lom_weight_percent, flus_1, flus_2, flus_3, flus_4, mixer_slag, v_d, t_d FROM input_params")
inCursor.execute(getAllInQuery)

outCursor = connection.cursor()
getAllOutQuery = ("SELECT metal_weight, metal_temperature, si_metal_weight_percent, mn_metal_weight_percent, c_metal_weight_percent, "
				  "p_metal_weight_percent, s_metal_weight_percent, metal_output_time, slag_weight, cao_slag_weight_percent, "
				  "sio2_slag_weight_percent, mgo_slag_weight_percent, feo_slag_weight_percent, al2o3_slag_weight_percent, "
				  "mno_slag_weight_percent, p2o5_slag_weight_percent, s_slag_weight_percent FROM output_params")
outCursor.execute(getAllOutQuery)

#Создаем пустые листы и заполняем их полученными данными из базы (extend)
inDataset = list()
normsin= list()
inDataset.extend(inCursor.fetchall())
train_data = np.array(inDataset)
train_data =train_data.transpose()
for i in range(len(train_data)):
	normsin.append(list())
	train_data[i], normsin[i] = preprocessing.normalize([train_data[i]], norm='l2', return_norm=True)
normsin = np.array(normsin)
train_data =train_data.transpose()
train_data.reshape(len(train_data), 20)
print(train_data)
print("to")
print(normsin)
outDataset = list()
normsout = list()
outDataset.extend(outCursor.fetchall())
train_target = np.array(outDataset)
train_target =train_target.transpose()
for i in range(len(train_target)):
	normsout.append(list())
	train_target[i], normsout[i] = preprocessing.normalize([train_target[i]], norm='l2', return_norm=True)
normsout = np.array(normsout)
train_target =train_target.transpose()
train_target.reshape(len(train_target), 17)
print(train_target)
print(normsout)
#Не забываем закрыть
inCursor.close()
outCursor.close()
connection.close()


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



#входные данные
"""filename = 'vxodnie.csv'
dataset = load_csv(filename)
print(dataset)


for i in range(len(dataset[0])):
	str_column_to_float(dataset, i)
print (dataset)
train_data = np.array(dataset)
train_data.reshape(928,17)
#train_data = np.expand_dims(train_data, axis=0)
print(train_data)

# выходные данные
filename='Gsh1.csv'
dataset = load_csv(filename)
#print(dataset)

for i in range(len(dataset[0])):
	str_column_to_float(dataset, i)
#print (dataset)
train_target = np.array(dataset)
train_target.reshape(928,2)

#print(train_target)
"""

"""# выходные данные тест
filename='Gshtest.csv'
dataset = load_csv(filename)
#print(dataset)

for i in range(len(dataset[0])):
	str_column_to_float(dataset, i)
#print (dataset)
test_target = np.array(dataset)
test_target.reshape(15,1)
#print(test_target)

#тест входные
filename = 'testvxod.csv'
dataset = load_csv(filename)
#print(dataset)


for i in range(len(dataset[0])):
	str_column_to_float(dataset, i)
#print (dataset)
test_data = np.array(dataset)
test_data.reshape(15,17)
#print(test_data)
"""
def build_model():
	model = models.Sequential()
	model.add(layers.Dense(128, activation='relu', input_shape=(train_data.shape[1],)))
	model.add(layers.Dense(128, activation='relu'))
	model.add(layers.Dense(17)) 
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
	score = model.evaluate(train_data, train_target, verbose=0)
	print (score)
	return model
model = build_model()
model.summary()

"""
#Валидация модели
k = 4 # количество блоков
num_val_samples = len(train_data)//k #количество строк в валидационной выборке
num_epochs = 100 #количество эпох
all_scores =[] #массив для соххранения итоговых оценок
# цикл по количеству блоков
for i in range(k):
	print('processing fold #', i)
	#выделение валидационной выборки
	val_data = train_data[i * num_val_samples: (i +1) * num_val_samples]
	val_targets = train_target[i * num_val_samples: (i +1)* num_val_samples]

	#берем оставшиеся данные для обучения
	partial_train_data = np.concatenate([train_data[:i*num_val_samples], train_data[(i+1)*num_val_samples:]], axis=0)
	partial_train_targets=np.concatenate([train_target[:i*num_val_samples], train_target[(i+1)*num_val_samples:]], axis=0)

	#строим модель
	model = build_model()

	history = model.fit(partial_train_data, partial_train_targets, validation_data=(val_data,val_targets), epochs=num_epochs, batch_size=1, verbose=0)
	mae_history = history.history['mae']
	all_mae_histories = list()
	all_mae_histories.append(mae_history)

	average_mae_history =[np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

	plt.plot(range(1, len(average_mae_history)+1), average_mae_history)
	plt.xlabel('Epoches')
	plt.ylabel('Validation_MAE')
	plt.show()"""


model=build_model()
model.fit(train_data, train_target, epochs= 100, batch_size=16, verbose=0)
'''
test_mse_score, test_mae_score = model.evaluate(test_data, test_target)
print(test_mae_score)
'''
class Network(QtWidgets.QMainWindow):
	def __init__(self, parent):
		super(Network, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.init_UI()
		self.returnToParent = parent
		self.tmppdd=[]

	def init_UI(self):
		self.setWindowTitle('Сталеплавильный конвертер')
		self.setWindowIcon(QIcon('icon.png'))
		self.ui.pushButtonPredict.clicked.connect(self.predictio)
		self.ui.pushButtonImport.clicked.connect(self.OpenFile)
		self.ui.pushButtonSave.clicked.connect(self.SaveFile)
		self.ui.pushButton_quitus.clicked.connect(self.Logout)
		#self.ui.pushButton_graf.clicked.connect(self.graf)
		self.ui.pushButtonBar.clicked.connect(self.bar)
		self.ui.pushButtonPie.clicked.connect(self.pie)

	def pie(self):
		try:
			values = []
			for l in range(8):
				values.append(self.tmppdd[9+l])
			print (values)
			labels = ['CaO', 'SiO2', 'MgO', 'FeO', 'Al2O3','MnO', 'P2O5', 'S']
			colors = ['blue', 'green', 'red', 'yellow', 'aqua', 'lawngreen', 'orange', 'purple']
			plt.title('Состав шлака')
			plt.pie(values, labels=labels, colors = colors, autopct='%1.0001f%%')
			plt.axis('equal')
			plt.show()
		except Exception:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Нет спрогнозированных данных")
			msg.setWindowTitle("Ошибка!")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return

	def bar(self):
		try:
			index = np.arange(5)
			for l in range(5):
				plt.bar(l, self.tmppdd[2 + l])
			plt.title('Содержание примесей в стали в %', fontsize=20)
			plt.xticks(index + 0.0001, ['Si', 'Mn', 'C', 'P', 'S'])
			#plt.set_xlabel('Вещество')
			#plt.set_ylabel('%')
			plt.show()
		except Exception:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Нет спрогнозированных данных")
			msg.setWindowTitle("Ошибка!")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return

	def predictio(self):
		try:
			Gch = float(self.ui.GchLE.text())
			Tch = float(self.ui.TchLE.text())
			SIch = float(self.ui.SichLE.text())
			MNch = float(self.ui.MnchLE.text())
			Cch = float(self.ui.CchLE.text())
			Pch = float(self.ui.PchLE.text())
			Sch = float(self.ui.SchLE.text())
			GNm = float(self.ui.Gm.text())
			SIm = float(self.ui.Sim.text())
			MNm = float(self.ui.Mnm.text())
			Cm = float(self.ui.Cm.text())
			Pm = float(self.ui.Pm.text())
			Sm = float(self.ui.Sm.text())
			F1 = float(self.ui.F1.text())
			F2 = float(self.ui.F2.text())
			F3 = float(self.ui.F3.text())
			F4 = float(self.ui.F4.text())
			Gmsh = float(self.ui.Gmsh.text())
			Vd = float(self.ui.Vd.text())
			Td = float(self.ui.Td.text())

		except ValueError:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Не валидные данные!")
			msg.setInformativeText("Возможно вы ввели запятую вместо точки.")
			msg.setWindowTitle("Ошибка!")
			msg.setDetailedText("Возможно вы пропустили поле или использвали запрещенные символы.")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return
		except AttributeError:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)

			msg.setText("Не валидные данные!")
			msg.setInformativeText("Возможно вы ввели запятую вместо точки.")
			msg.setWindowTitle("Ошибка!")
			msg.setDetailedText("Возможно вы пропустили поле или использвали запрещенные символы.")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return
		except Exception:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)

			msg.setText("Не валидные данные!")
			msg.setInformativeText("Возможно вы ввели запятую вместо точки.")
			msg.setWindowTitle("Ошибка!")
			msg.setDetailedText("Возможно вы пропустили поле или использвали запрещенные символы.")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return

		tst = list()
		tryPerc = list()
		#normstest = list()
		try:
			tst.append([Gch,Tch,SIch,MNch,Cch,Pch,Sch,GNm,SIm,MNm,Cm,Pm,Sm,F1,F2,F3,F4,Gmsh,Vd,Td])
			tt = tst[0]
			for a in range(len(tt)):
				if tt[a] < 0:
					raise Exception
			tryPerc.append([SIch,MNch,Cch,Pch,Sch,SIm,MNm,Cm,Pm,Sm])
			tryPerc = tryPerc[0]
			for b in range(len(tryPerc)):
				if tryPerc[b] > 100:
					raise Exception
		except Exception:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Данные не могут быть меньше 0, Проценты не могут быть больше 100")
			msg.setWindowTitle("Ошибка!")
			msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()
			return

		test_data = np.array(tst)

		test_data.reshape(1,20)
		print(test_data)
		normsin.reshape(1,20)
		print(normsin)
		for i in range(len(normsin)):
			test_data[0][i] = test_data[0][i]/normsin[i][0]
		print(test_data)

		out_Gmish = model.predict(test_data)
		print(out_Gmish)

		for j in range(len(normsout)):
			out_Gmish[0][j] = out_Gmish[0][j]*normsout[j][0]
		pdd = out_Gmish[0]
		for l in range(len(pdd)):
			pdd[l] = format(pdd[l], '.4f')
		self.ui.Gst.setText(str(pdd[0]))
		self.ui.Tst.setText(str(pdd[1]))
		self.ui.Sist.setText(str(pdd[2]))
		self.ui.Mnst.setText(str(pdd[3]))
		self.ui.Cst.setText(str(pdd[4]))
		self.ui.Pst.setText(str(pdd[5]))
		self.ui.Sst.setText(str(pdd[6]))
		self.ui.temst.setText(str(pdd[7]))
		self.ui.Msh.setText(str(pdd[8]))
		self.ui.CaOsh.setText(str(pdd[9]))
		self.ui.SiO2sh.setText(str(pdd[10]))
		self.ui.MgOsh.setText(str(pdd[11]))
		self.ui.FeOsh.setText(str(pdd[12]))
		self.ui.Al2O3sh.setText(str(pdd[13]))
		self.ui.MnOsh.setText(str(pdd[14]))
		self.ui.P2O5sh.setText(str(pdd[15]))
		self.ui.Ssh.setText(str(pdd[16]))

		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Прогноз прошел успешно!")
		msg.setWindowTitle("Успех!")
		msg.setStandardButtons(QMessageBox.Ok)
		retval = msg.exec_()
		self.tmppdd = pdd



	def OpenFile(self):
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
		self.ui.GchLE.setText(str(test_target[0][0]))
		self.ui.TchLE.setText(str(test_target[0][1]))
		self.ui.SichLE.setText(str(test_target[0][2]))
		self.ui.MnchLE.setText(str(test_target[0][3]))
		self.ui.CchLE.setText(str(test_target[0][4]))
		self.ui.PchLE.setText(str(test_target[0][5]))
		self.ui.SchLE.setText(str(test_target[0][6]))
		self.ui.Gm.setText(str(test_target[0][7]))
		self.ui.Sim.setText(str(test_target[0][8]))
		self.ui.Mnm.setText(str(test_target[0][9]))
		self.ui.Cm.setText(str(test_target[0][10]))
		self.ui.Pm.setText(str(test_target[0][11]))
		self.ui.Sm.setText(str(test_target[0][12]))
		self.ui.F1.setText(str(test_target[0][13]))
		self.ui.F2.setText(str(test_target[0][14]))
		self.ui.F3.setText(str(test_target[0][15]))
		self.ui.F4.setText(str(test_target[0][16]))
		self.ui.Gmsh.setText(str(test_target[0][17]))
		self.ui.Vd.setText(str(test_target[0][18]))
		self.ui.Td.setText(str(test_target[0][19]))
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Данные загружены")
		msg.setWindowTitle("Успех!")
		msg.setStandardButtons(QMessageBox.Ok)
		retval = msg.exec_()

	def SaveFile(self):
		Gst = float(self.ui.Gst.text())
		Tst = float(self.ui.Tst.text())
		Sist = float(self.ui.Sist.text())
		Mnst = float(self.ui.Mnst.text())
		Cst = float(self.ui.Cst.text())
		Pst = float(self.ui.Pst.text())
		Sst = float(self.ui.Sst.text())
		temst = float(self.ui.temst.text())
		Msh = float(self.ui.Msh.text())
		CaOsh = float(self.ui.CaOsh.text())
		SiO2sh = float(self.ui.SiO2sh.text())
		MgOsh = float(self.ui.MgOsh.text())
		FeOsh = float(self.ui.FeOsh.text())
		Al2O3sh = float(self.ui.Al2O3sh.text())
		MnOsh = float(self.ui.MnOsh.text())
		P2O5sh = float(self.ui.P2O5sh.text())
		Ssh = float(self.ui.Ssh.text())

		save = list()
		save.append([Gst, Tst, Sist, Mnst, Cst, Pst, Sst, temst, Msh, CaOsh, SiO2sh, MgOsh, FeOsh, Al2O3sh, MnOsh, P2O5sh, Ssh])
		try:
			"""#root.filename = tk.asksaveasfilename(("txt", "*.txt"))
				#if filename:
				#	self.filedialog.insert(END, f"Сохранить{filename}\n")
				#	with open(filename, "w") as f:
				#		f.write(save)
				#root = tk.Tk()
				#root.withdraw()
				#root.filename = filedialog.asksaveasfile(initialdir="/", title="Select file",  filetypes=((".txt", "*.txt"), ("all files","*.*")))
				#root.filename = open(initialdir="/", title="Select file",  filetypes=((".txt", "*.txt"), ("all files","*.*")))
				#with open(root.filename, "w") as file:
				#	file.write(save)
				data = [('txt', '.txt')]
				file = asksaveasfile(filetypes=data, defaultextension=data)
				with open(file, "w") as f:
					f.write(save)"""
			root = tk.Tk()
			root.withdraw()
			obz = ["Масса металла, т:", "Температура металла, С:", "Массовая доля Si М, %:", "Массовая доля Mn М,%:", "Массовая доля C М,%:", "Массовая доля P М, %:", "Массовая доля S М, %:", "Прод-ть выпуска М, мин:", "Масса шлака, т:", "Массовая доля CaO Ш, %:", "Массовая доля SiO2 Ш, %:", "Массовая доля MgO Ш, %:", "Массовая доля FeO Ш, %:", "Массовая доля Al2O3 Ш, %:", "Массовая доля MnO Ш, %:", "Массовая доля P2O5 Ш, %:", "Массовая доля S Ш, %:"]
			root.filename = filedialog.asksaveasfile(initialdir="/", title="Select file",  filetypes=((".txt", "*.txt"), ("all files","*.*")))
			path = root.filename.name + ".txt"
			if path.find(".txt"):
				f = open(path, "w")
			#else:
			#	f = open(path + ".txt", "w")
			saveStr = obz[0] + str(save[0][0])+","
			for i in range(16):
				if(i==15):
					saveStr += obz[i+1] + str(save[0][i+1])
				else:
					saveStr += obz[i+1] + str(save[0][i+1])+","
			f.write(saveStr)
			f.close()
		except Exception:
			return
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Данные сохранены")
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



"""app = QtWidgets.QApplication([])
application = Network()
application.show()
sys.exit(app.exec())"""

