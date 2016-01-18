from PySide import QtGui
from PySide import QtCore
from Web import WebView

import sys
import gc

class TabWidget(QtGui.QTabWidget) :
	closeSignal = QtCore.Signal()
	
	def __init__(self) :
		super(TabWidget, self).__init__()
		self.closeSignal.connect(self.closeSignalHandler)
		pass

	def closeEvent(self, event) :
		self.closeSignal.emit()
	
	@QtCore.Slot()
	def closeSignalHandler(self) :
		pass
	
	@QtCore.Slot(QtGui.QWidget)
	def deleteTab(self, widget) :
		self.widget(self.indexOf(widget)).deleteLater()
		self.removeTab(index)