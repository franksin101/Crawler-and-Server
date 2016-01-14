from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtNetwork
import gc
import sys

from mainWindow import mainWindow

if __name__ == "__main__" :
	print("the program is execute!")
	app = QtGui.QApplication(sys.argv)
	ui = mainWindow()
	thread1 = QtCore.QThead()
	thread2 = QtCore.QThead()
	sys.exit(app.exec_())
	
	
def run1() :
	print("1")

def run2() :
	print("2")