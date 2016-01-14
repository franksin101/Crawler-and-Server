from Web import WebPage
from Web import WebView
from PySide import QtCore
from PySide import QtGui
from PySide import QtNetwork
from PySide import QtWebKit
import gc
import sys


class mainWindow(QtGui.QWidget) :
	def __init__(self, width = 600, height = 800):
		super(mainWindow, self).__init__()
		self.width = width
		self.height = height
		self.setGeometry(10, 10, self.width, self.height)
		self.initial()
	def initial(self) :
		self.MainHLayout = QtGui.QHBoxLayout()
		self.WebView = WebView()
		
		self.WebView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
		
		self.WebView.show()
		
		self.WebView.load(QtCore.QUrl("http://127.0.0.1/tpcdebt/test.php"))
		
		self.MainHLayout.addWidget(self.WebView)
		
		self.WebView.loadFinished.connect(self.loadPageOK)
		
		self.setLayout(self.MainHLayout)
		
		self.show()
	def loadPageOK(self, isFinished) :
		if isFinished :
			pass