from PySide import QtCore
from PySide import QtGui
from PySide import QtNetwork

import sys

class ClientThread(QtCore.QThread) :
	finishedSignal = QtCore.Signal(str)

	def __init__(self) :
		super(ClientThread, self).__init__()
		self.id = self.currentThreadId()
		self.finished.connect(self.deleteLater())
		self.finished.connect(self.finishedWithThreadID)
		self.finished.connect(self.finishedWithThreadIDHandler)
		pass
	def run(self) :
		self.exit(self.exec_())
		
	@QtCore.Slot()
	def finishedWithThreadID(self) :
		self.finishedSignal.emit(str(self.id))
		
	@QtCore.Slot(str)	
	def finishedWithThreadIDHandler(self, threadID) :
		print("Thread ID " + threadID + " is finished.")
		pass

class ThreadAdministrator(QtCore.QObject):
	def __init__(self) :
		super(ThreadAdministrator, self).__init__()
		self.threadTable = dict()
		pass
	
	def newThread(self) :
		ANewThread = ClientThread()
		self.threadTable[str(ANewThread.currentThreadId())] = ANewThread
		ANewThread.finishedSignal.connect(self.deleteThread)
		return ANewThread
		
	@QtCore.Slot(str)
	def deleteThread(self, id) :
		if id in [key for key in self.threadTable.keys()] :
			del self.threadTable[id]
			
	# check and wait all connection finished, then destory itself
	@QtCore.Slot()
	def waitForAllThread(self) :
		isAllFinished = True
		while True :
			for thread in self.threadTable :
				if thread.isRunning() :
					isAllFinished = False
					break
				elif thread.isFinished() :
					isAllFinished = True

			if isAllFinished :
				break
			else :
				isAllFinished = True
		self.quit()
		

class ClientConnectionObject(QtCore.QObject) :
	urlChangedSignal = QtCore.Signal(QtCore.QUrl) # emit change targeted Url Signal
	
	def __init__(self, url = "127.0.0.1") :
		super(ClientConnectionObject, self).__init__()
		self.textDocument = QtGui.QTextDocument()
		self.url = QtCore.QUrl(url)
		self.tcpSocket = QtNetwork.QTcpSocket()
		pass

	def setUrl(self, url = "127.0.0.1") :
		self.url = QtCore.QUrl(url)
		self.urlChangedSignal.emit(self.url)
		
	def document(self) :
		return self.textDocument
		
class ConnectionListWidgetItem(QtGui.QListWidgetItem) :
	def __init__(self, object = None) :
		super(ConnectionListWidgetItem, self).__init__()
		self.connectionObject = object
		pass
	def setConnectionObject(self, object) :
		self.connectionObject = object
	def getConnectionObject(self) :
		return self.connectionObject
		
		
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
		
		self.bottomPushButton.clicked.connect(self.clickToStartNewConnection)
		self.listWidget.currentItemChanged.connect(self.listCurrentItemChanged)
		self.listWidget.itemClicked.connect(self.listItemClicked)
		
		self.show()
		pass
		
	@QtCore.Slot()
	def clickToStartNewConnection(self) :
		if QtCore.QUrl(self.bottomLineEdit.text()).isValid() :
			clientConnectionObject = ClientConnectionObject(self.bottomLineEdit.text())
			conectionListWidgetItem = ConnectionListWidgetItem(clientConnectionObject)
			conectionListWidgetItem.setText(self.bottomLineEdit.text())
			self.listWidget.addItem(conectionListWidgetItem)
			self.listWidget.setCurrentItem(conectionListWidgetItem)
			self.bottomLineEdit.setText("")
			
			# conectionListWidgetItem.getConnectionObject().
	
	@QtCore.Slot(ConnectionListWidgetItem, ConnectionListWidgetItem)
	def listCurrentItemChanged(self, now, before) :
		print("it is already change to " + now.text() + " !!!")
		# now.
		self.textBrowser.setDocument(now.getConnectionObject().document())
		
	@QtCore.Slot(ConnectionListWidgetItem)
	def listItemClicked(self, clickedItem) :
		print("this is " + clickedItem.text() + " clicked")
		self.textBrowser.setDocument(clickedItem.getConnectionObject().document())
		
	
	def keyPressEvent(self, event) :
		print(event.key())
		if event.key() == QtCore.Qt.Key_Enter or event.key() == (QtCore.Qt.Key_Enter - 1) :
			self.bottomPushButton.click()
		

class Client(QtCore.QObject) :
	def __init__(self) :
		self.widget = ClientWidget()
		
if __name__ == "__main__" :
	app = QtGui.QApplication(sys.argv)
	
	client = Client()
	
	sys.exit(app.exec_())