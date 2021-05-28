import sys
from kernel import *
from Scan2login import *
from mainsub import *
from threading import Thread
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow,QWidget

def scan2login():
	global MainWindow
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	ui = Ui_Form()  #  ui_from是类名
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

def mainsub(name):
	global SubWindow
	app = QApplication(sys.argv)
	SubWindow = QMainWindow()
	ui = Ui_Form_sub()  #  ui_from是类名 mainsub.py
	ui.setupUi(SubWindow,name)
	SubWindow.show()
	sys.exit(app.exec_())

#尝试运行Kernel.py里面的 init函数
state,info=init()
if state == 'fail':    #若失败,则是未登录,尝试调用扫码登陆窗体.
	pack = mkqr()    #mkqr是kernel的函数
	Thread(target=scan2login).start()	#开启一个线程(显示的窗体)
	getAcookie(pack)	#程序堵塞在这,传入pack后每隔一秒验证一次
	MainWindow.close()	#上方代码执行完毕,关闭主窗体

	#重新登录
	state, info = init()
	if state == 'fail':
		err='扫码完成后发生了报错,即重新使用cookie登陆时报错!'
		debug(err)
		exit(-1)

try:
	mainsub(info[0])	#主窗体启动
except Exception as e:
	print(e)





