from PySide import QtGui, QtCore
from Web import WebPage, WebView
from TabWidget import TabWidget

import sys
import gc

class Crawler(QtGui.QWidget):
	signalClickedToLoadUrl = QtCore.Signal(QtCore.QUrl)
	
	def __init__(self, width = 800, height = 600):
		super(Crawler, self).__init__()
		self.setGeometry(10, 10, width, height)
		self.setupUI()
		
	def setupUI(self) :
		self.mainHBoxLayout = QtGui.QHBoxLayout()
		self.mainRVBoxLayout = QtGui.QVBoxLayout()
		self.mainLVBoxLayout = QtGui.QVBoxLayout()
		self.executeCrawler = QtGui.QPushButton("Get Content!!!")
		self.urlBarLineEdit = QtGui.QLineEdit()
		self.myWebView = WebView()
		self.myTabWidget = TabWidget()
		
		self.myWebView.show()
		self.myTabWidget.addTab(self.myWebView, "my Web View")
		
		self.mainLVBoxLayout.addWidget(self.urlBarLineEdit)
		self.mainLVBoxLayout.addWidget(self.myTabWidget)
		self.mainRVBoxLayout.addWidget(self.executeCrawler)
		
		self.mainHBoxLayout.addLayout(self.mainLVBoxLayout)
		self.mainHBoxLayout.addLayout(self.mainRVBoxLayout)
		self.setLayout(self.mainHBoxLayout)
		
		self.executeCrawler.clicked.connect(self.slotClickedToLoadUrl)
		self.signalClickedToLoadUrl.connect(self.slotLoadUrl)
		self.myWebView.loadFinished.connect(self.slotWebViewLoadFinished)
		
		self.show()
	
	@QtCore.Slot()
	def slotClickedToLoadUrl(self) :
		print(self.urlBarLineEdit.text())
		self.signalClickedToLoadUrl.emit(QtCore.QUrl(self.urlBarLineEdit.text()))
	
	@QtCore.Slot(QtCore.QUrl)
	def slotLoadUrl(self, qUrl) :
		self.myWebView.load(qUrl)
	
	@QtCore.Slot(bool)
	def slotWebViewLoadFinished(self, isFinished) :
		if isFinished :
			self.urlBarLineEdit.setText(self.myWebView.url().toString())
			pageFrames = self.myWebView.page().mainFrame().childFrames()
			
			print("base Url := " + self.myWebView.page().mainFrame().baseUrl().toString())
			
			"""for frame in pageFrames :
				print(frame.frameName())
				print(frame.toHtml())"""
			pass
	
if __name__ == "__main__" :
	# print("the program is execute!")
	app = QtGui.QApplication(sys.argv)
	ui = Crawler()
	sys.exit(app.exec_())