from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtNetwork
import gc
import sys

from mainWindow import mainWindow

class Thread1(QtCore.QThread) :
	def __init__(self) :
		super(Thead1, self).__init__()
	def run(self) :
		while True :
			print(1)
			
class Thread2(QtCore.QThread) :
	def __init__(self) :
		super(Thead2, self).__init__()
	def run(self) :
		while True :
			print(2)

if __name__ == "__main__" :
	print("the program is execute!")
	app = QtGui.QApplication(sys.argv)
	ui = mainWindow()
	
	t1 = Thread1()
	t2 = Thread2()
	
	t1.start()
	t2.start()
	
	sys.exit(app.exec_())