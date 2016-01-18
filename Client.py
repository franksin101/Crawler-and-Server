from PySide import QtCore
from PySide import QtGui
from PySide import QtNetwork

import sys

class ClientConnectionObject(QtCore.QObject) :
	urlChangedSignal = QtCore.Signal(QtCore.QUrl)
	def __init__(self) :
		super(ClientConnectionObject, self).__init__()
		self.textDocument = QtGui.QTextDocument()
		self.url = QtCore.QUrl("127.0.0.1")
		self.tcpSocket = QtNetwork.QTcpSocket()
		pass
	def setUrl(self, url = "127.0.0.1") :
		self.url = QtCore.QUrl(url)
		self.urlChangedSignal.emit(self.url)
	def document(self) :
		return self.textDocument
		
class ClientWidget(QtGui.QWidget) :
	def __init__(self) :
		super(ClientWidget, self).__init__()
		self.initialUI()
		pass
	def initialUI(self) :
		self.mainHLayout = QtGui.QHBoxLayout()
		self.bottomHLayout = QtGui.QHBoxLayout()
		self.rightVLayout = QtGui.QVBoxLayout()
		self.listWidget = QtGui.QListWidget()
		self.textBrowser = QtGui.QTextBrowser()
		self.bottomLineEdit = QtGui.QLineEdit()
		self.bottomPushButton = QtGui.QPushButton("Submit")
		
		self.bottomHLayout.addWidget(self.bottomLineEdit)
		self.bottomHLayout.addWidget(self.bottomPushButton)
		
		self.rightVLayout.addWidget(self.listWidget)
		self.rightVLayout.addLayout(self.bottomHLayout)
		
		self.mainHLayout.addWidget(self.textBrowser)
		self.mainHLayout.addLayout(self.rightVLayout)
		
		self.setLayout(self.mainHLayout)
		
		self.show()
		pass
	
	def keyPressEvent(self, event) :
		print(event.text())
		if event.key() == "\n" :
			self.bottomPushButton.click()
		

class Client(QtCore.QObject) :
	def __init__(self) :
		self.widget = ClientWidget()
		
if __name__ == "__main__" :
	app = QtGui.QApplication(sys.argv)
	
	client = Client()
	
	sys.exit(app.exec_())