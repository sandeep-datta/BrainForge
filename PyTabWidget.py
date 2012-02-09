from PyQt4.QtGui import *
from Decorators import *
from Helpers import *


class PyTab(QWidget):

	def __init__(this, qTabWidget, widget, text, icon=None):
		this._tabWidget = qTabWidget
		this._widget = widget
		widget.setParent(this)
		
		if icon:
			this._index = this._tabWidget.addTab(this, text, icon)
		else:
			this._index = this._tabWidget.addTab(this, text)
		

	@property
	def Index(this):
		return this._index
	
	@property
	def Widget(this):
		return this._tabWidget.widget(this.Index)
	
	@property
	def Text(this):
		return this._tabWidget.tabText(this.Index)

	@Text.setter
	def Text(this, text):
		this._tabWidget.setTabText(this.Index, text)

	def tabInserted(this, index):
		this._index = this._tabWidget.indexOf(this)

	def tabRemoved(this, index):
		this._index = this._tabWidget.indexOf(this)

class PyTabWIdget(QWidget):

	def __init__(this):
		_tabWidget = QTabWidget(this)

	@property
	def TabWidget(this):
		return this._tabWidget

	@property
	def Tabs(this):
		for i in range(this._tabWidget.count())
			yeild _getTab(i)
	
	@property
	def currentTab(this):
		return this._tabWidget.currentWidget()

	def _getTab(this, index):
		widget = this._tabWidget.widget(index)
		return widget

	def tabInserted(this, index):
		_propogate(funcName(), index)
	
	def tabRemoved(this, index):
		_propogate(funcName(), index)
		
	def _propogate(funcname, *args):
		for t in this.Tabs:
			getattr(t, funcname, None)(*args)	

	def addTab(this, widget, text, icon=None):
		return PyTab(this._tabWidget, widget, text, icon) #PyTab will add itself to the tab widget

	def removeTab(this, tab):
		this._tabWidget.removeTab(tab.Index)		