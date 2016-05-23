from PySide import QtGui, QtCore
from Web import WebPage, WebView
from TabWidget import TabWidget

import sys
import gc

def findAllElementsChild(e) :
	if e.nextSibling.tagName() == "" :
		pass
	else :
		print(e.tagName())
		findAllElementsChild(e.nextSibling)

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
		self.urlBarLineEdit = QtGui.QLineEdit("http://www2.tpa.edu.tw/tpaedu/Home/login.asp")
		self.myWebView = WebView()
		self.myTabWidget = TabWidget()
		
		#self.myWebView.settings().setDefaultTextEncoding("big5")
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
			
			if self.myWebView.page().mainFrame().baseUrl().toString() == "http://www2.tpa.edu.tw/tpaedu/default.asp" :
				print("it is tpa local net")
				for frame in pageFrames :
					print(frame.frameName())
					#print(frame.toHtml())
					elements = frame.findAllElements("td")
					print(elements.count())
					for index in range(elements.count()) :
						"""print("elements" + str(index))
						print(elements.at(index + 1).tagName())
						print(elements.at(index + 1).firstChild().tagName())
						print(elements.at(index + 1).firstChild().nextSibling().tagName())
						print(elements.at(index + 1).firstChild().nextSibling().nextSibling().tagName())
						print(elements.at(index + 1).firstChild().nextSibling().nextSibling().nextSibling().tagName())
						print(str(type(elements.at(index + 1).firstChild().nextSibling().nextSibling().nextSibling().nextSibling())))"""
						findAllElementsChild(elements.at(index + 1).firstChild())
						
					if frame.frameName() == "logo" :
						pass
					elif frame.frameName() == "menu" :
						# get menu for javascript robot action
						pass
					elif frame.frameName() == "main" :
						# get main content to crawler data
						pass
					elif self.myWebView.page().mainFrame().baseUrl().toString() == "http://www2.tpa.edu.tw/tpaedu/Home/login.asp" :
						pass
				pass
	
if __name__ == "__main__" :
	# print("the program is execute!")
	app = QtGui.QApplication(sys.argv)
	ui = Crawler()
	sys.exit(app.exec_())