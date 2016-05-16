from PySide import QtNetwork
from PySide import QtCore
from PySide import QtGui
from Web import WebView
from TabWidget import TabWidget

import sys
import json

class Connection(QtCore.QObject) :
	closeConnection = QtCore.Signal()
	
	def __init__(self, TcpSocket = None) :
		if TcpSocket == None :
			raise ValueError
		self.stop = False
		self.webview = WebView()
		self.webview.load("http://127.0.0.1")
		self.TcpSocket = TcpSocket
		
	def widget(self) :
		return self.webview
	
	@QtCore.Slot()
	def forceStop(self) :
		self.stop = True
		self.closeConnection.emit(self.webview)
		self.TcpSocket.abort()
		self.TcpSocket.deleteLater()
		# self.webview.deleteLater()
		self.deleteLater()
		self.thread().forceStop()
	
	@QtCore.Slot()
	def service(self) :
		print(self.thread().currentThreadId())
		while not self.stop :
			command = self.TcpSocket.read(4096)
			
			if command["type"] == "loadUrl" :
				self.webview.load(cmd["url"])
				data = QtCore.QByteArray()
				data = "load finished" 
				self.TcpSocket.write(data)
				self.TcpSocket.flush()
				data.deleteLater()
			elif cmd["type"] == "close" :
				self.forceStop()
			else :
				print("unknow command")
		
class CrossThread(QtCore.QThread) :
	startedSignal = QtCore.Signal()
	finishedSignal = QtCore.Signal(str)
	
	def __init__(self) :
		super(CrossThread, self).__init__()
		self.id = self.currentThreadId()
		self.finished.connect(self.deleteLater)
		self.finished.connect(self.finishedWithThreadID)
		self.finished.connect(self.finishedWithThreadIDHandler)
		self.startedSignal.connect(self.startedHandler)
		pass
	def run(self) :
		self.startedSignal.emit()
		self.exit(self.exec_())
	
	# the start handler it 
	@QtCore.Slot()
	def startedHandler(self) :
		print(self.id + " is start !!")
		pass
	
	# when this thread finished it will emit a finished signal with id
	@QtCore.Slot()
	def finishedWithThreadID(self) :
		self.finishedSignal.emit(str(self.id))
	
	@QtCore.Slot(str)	
	def finishedWithThreadIDHandler(self, threadID) :
		print("Thread ID " + threadID + " is finished.")
		pass
	
	@QtCore.Slot()
	def forceStop(self) :
		self.quit()
		self.cleanup()
		

class MoniterObject :
	def __init__(self, Thread, Connection) :
		self.Thread = Thread
		self.Connection = Connection

class MoniterThread(QtCore.QThread) :
	startedSignal = QtCore.Signal()
	
	def __init__(self) :
		super(MoniterThread, self).__init__()
		self.threadTable = dict()
		self.finished.connect(self.deleteLater)
		pass
		
	def run(self) :
		self.exit(self.exec_())
		
	def allThreads(self) :
		return self.threadTable
	
	# add new object for monite
	@QtCore.Slot(MoniterObject)
	def addNewThread(self, moniterObject) :
		self.threadTable[str(moniterObject.Thread.currentThreadId())]  = moniterObject
	
	# delete special connection by thread id
	@QtCore.Slot(str)
	def deleteThread(self, threadID) :
		if threadID in [key for key in self.threadTable.keys()]:
			if self.threadTable[threadID].Thread.isRunning() :
				self.threadTable[threadID].Connection.forceStop()
			del self.threadTable[threadID]
	
	# force cancel all connection, then destory itself
	@QtCore.Slot()
	def deleteAll(self) :
		for thread_connection in self.threadTable :
			thread_connection.Connection.forceStop()
		self.quit()
	
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

class Server(QtNetwork.QTcpServer) :
	addNewThread = QtCore.Signal(MoniterObject)
	
	# basic initial 
	# private object :
	# 	widget : TabWidget for WebView
	#	monitor : A thread object for monite all connection and release finished connection
	# connections :
	#	when main widget close, it will shutdown server instantly
	#	a new connection handler
	#	monitor add new object event
	def __init__(self) :
		super(Server, self).__init__()
		self.widget = TabWidget()
		self.monitor = MoniterThread()
		self.widget.closeSignal.connect(self.stopServer)
		self.newConnection.connect(self.newConnectionHandler)
		self.addNewThread.connect(self.monitor.addNewThread)
		pass
	
	# start monitor, show widget, start service
	def run(self) :
		self.monitor.start()
		self.widget.show()
		self.listen(QtNetwork.QHostAddress("127.0.0.1"), 5000)
		
	@QtCore.Slot()
	def newConnectionHandler(self) :
		newTcpSocket = self.nextPendingConnection() # get new connection socket
		connection = Connection(newTcpSocket) # create a new connection delegate object
		crossThread = CrossThread() # create connection thread
		self.widget.addTab(str(crossThread.currentThreadId()), connection.widget()) # insert connection attach widget to server main widget
		connection.closeConnection.connect(self.widget.deleteTab) # connect connection close to remove widget of server main widget
		crossThread.finishedSignal.connect(self.monitor.deleteThread) # when a thread dead or finish its job, it will tell monitor to delete it.
		crossThread.startedSignal.connect(connection.service) # inform new connection thread start service.
		connection.moveToThread(crossThread) # let connection run in new thread 
		moniterObject = MoniterObject(crossThread, connection) # create a monitor object for monitor thread
		self.addNewThread.emit(moniterObject) # make monitor thread registe a new monitor object
		crossThread.start() # new connection thread start running
	
	# don't stop directly, it will wait all thread finished and stop safely
	@QtCore.Slot()
	def stopServer(self) :
		self.monitor.deleteAll()
		
		while not self.monitor.isFinished() :
			pass
			
		print("Is monitor thread is end ? : " + str(self.monitor.isFinished()))
		
		self.close()
		self.widget.deleteLater()
		self.deleteLater()
		
		
if __name__ == "__main__" :
	app = QtGui.QApplication(sys.argv)
	
	server = Server()
	server.run()
	
	sys.exit(app.exec_())