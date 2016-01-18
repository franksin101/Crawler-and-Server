from PySide import QtCore
from PySide import QtGui
import sys
import gc

class TestSlot(QtCore.QObject) :
	def __init__(self) :
		super(TestSlot, self).__init__()
		self.times = 0
		pass
		
	@QtCore.Slot(str)
	def slot(self, string) :
		print(string + str(self.times))
		self.times += 1
		if self.times >= 10 :
			self.deleteLater()
			self.thread().quit()
			
			

class TestSignal(QtCore.QObject) :
	signal = QtCore.Signal(str)
	def __init__(self) :
		super(TestSignal, self).__init__()
		pass
		
class CrossThread(QtCore.QThread) :
	def __init__(self) :
		super(CrossThread, self).__init__()
		pass
	def run(self) :
		self.exit(self.exec_())

if __name__ == "__main__" :
	print("the program is execute!")
	app = QtGui.QApplication(sys.argv)

	o1 = TestSignal()
	o2 = TestSlot()
	
	o1.signal.connect(o2.slot)
	
	t2 = CrossThread()
	
	o2.moveToThread(t2)
	
	w = QtGui.QWidget()
	
	w.show()
	
	t2.start()
	
	n = 0
	
	while n < 10 :
		o1.signal.emit("I am apple")
		n += 1
		
	print("END ~~~")
	
	#while True :
	#	print("Is t2 finished ? " + str(t2.isFinished()))
	
	while not t2.isFinished() :
		print("t2 not finished")
	
	if t2.isFinished() :
		print("finished")
		
	print(t2.wait())
	
	sys.exit(app.exec_())