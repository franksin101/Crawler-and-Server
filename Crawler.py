from PySide import QtGui, QtCore
import Web

class Crawler :
	def __init__(self) :
		self.WebView = Web.WebView()
	def initUI(self) :
		self.MainHBoxLayout = QtGui.QHBoxLayout()
		