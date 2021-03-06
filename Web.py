from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtNetwork


class WebPage(QtWebKit.QWebPage) :
	def __init__(self) :
		super(WebPage, self).__init__()
		self.settings().setDefaultTextEncoding("Big5")
	def userAgentForUrl(self, url) :
		return "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko" # IE 11
		
class WebView(QtWebKit.QWebView) :
	def __init__(self):
		super(WebView, self).__init__()
		self.setPage(WebPage())
		self.linkClicked.connect(self.handleLinkClicked)
		self.loadFinished.connect(self.loadPageReady)
	
	@QtCore.Slot(bool)
	def loadPageReady(self, isFinished) :
		if isFinished :
			print("finished")
			pass
	
	@QtCore.Slot(QtCore.QUrl)
	def handleLinkClicked(self, url) :
		self.load(url)