from PySide import QtGui, QtCore
from Web import WebPage, WebView
from TabWidget import TabWidget

import sys
import gc

class Crawler(QtGui.QWidget):
	def __init__(self):
		super(Crawler, self).__init__()
	def setupUI(self) :
		self.mainHBoxLayout = QtGui.QHBoxLayout()
		self.mainVBoxLayout = QtGui.QVBoxLayout()
		self.executeCrawler = QtGui.QPushButton()
		self.myWebView = WebView()
		self.myTabWidget = TabWidget()
		pass
	
if __name__ == "__main__" :
	print("Hello World")