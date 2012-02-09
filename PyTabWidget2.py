from PyQt4.QtGui import *
from Decorators import *
from Helpers import *
import inspect

#@memoized
def get_qwidget_class():
	return QWidget




#@memoized
def get_pytabwidget_class():
	class PyTabWidget(QWidget):

		@property
		def Widget(this):
			return this._tabWidget


		def __init__(this):
			QWidget.__init__(this)
			this._tabWidget = QTabWidget(this)
			#this._tabWidget.setParent(this)
		
		def callSetter(this, setterName, value):
			return getattr(this._tabWidget, setterName)(value)

		def callGetter(this, getterName):
			return getattr(this._tabWidget, getterName)()
	
	for x in dir(QTabWidget):
		if x.startswith("set") and not x.startswith("setTab"):
			setterName = x
			setter = getattr(QTabWidget, setterName)
			
			if hasattr(setter, "__call__"):
				verb = x[len("set"):]
				print(verb)
				#setterArgs = inspect.getargspec(setter)[0]
				#validSetter = len(setterArgs) == 2   #1 - this ptr 2 - actual argument
				getterName = verb[0].lower() + verb[1:]
				getter = None
				try:
					getter = getattr(PyTabWidget, getterName)
				except AttributeError:
					pass
				#getterArgs = inspect.getargspec(getter)[0]
				#validGetter = len(getterArgs) == 1 #1 - this pointer

				if setter and getter:
					setattr(PyTabWidget, "_" + setterName, lambda this, value: this.callSetter(setterName, value))
					setattr(PyTabWidget, "_" + getterName, lambda this: this.callGetter(getterName))
					setattr(PyTabWidget, verb, property(getattr(PyTabWidget, "_" + setterName), getattr(PyTabWidget, "_" + getterName)))
				elif setter:
					setattr(PyTabWidget, "_" + setterName, lambda this, value: this.callSetter(setterName, value))
					setattr(PyTabWidget, verb, property(getattr(PyTabWidget, "_" + setterName)))
				elif getter:
					setattr(PyTabWidget, "_" + getterName, lambda this: this.callGetter(getterName))
					setattr(PyTabWidget, verb, property(None, getattr(PyTabWidget, "_" + getterName)))

	return PyTabWidget


#@memoized
def get_pytab_class():
	class PyTab(get_qwidget_class()):
		pass

if __name__ == "__main__":
	PyTabWidget = get_pytabwidget_class()

	# PyTabWidget = type(PyTabWidget.__name__, 
	# 					(QWidget,), 
	# 					dict(PyTabWidget.__dict__))
	import sys
	app = QApplication(sys.argv)

	mw = PyTabWidget()
	mw.Widget.addTab(QWidget(), "Tab1")
	mw.show()
	
	sys.exit(app.exec_())