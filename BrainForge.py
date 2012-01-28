"""
The main BrainForge application module
(C) 2012 Sandeep Datta
"""

import sys
from PyQt4.QtGui import *

class BrainForge(QWidget):

	@property
	def Title(self):
		return "%s v%s" % (self._appname, self._version)

	def __init__(self):
		super().__init__()
		self._appname = "Brainforge"
		self._version = "0.01"
		self.initUi()

	def initUi(self):
		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle(self.Title)
		self.setWindowIcon(QIcon('web.png'))
		self.show()