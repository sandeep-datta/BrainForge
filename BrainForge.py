"""
The main BrainForge application module
(C) 2012 Sandeep Datta
"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class BrainForge(QMainWindow):

	@property
	def Title(self):
		return "%s v%s" % (self._appname, self._version)

	def __init__(self):
		super().__init__()
		self._appname = "Brainforge"
		self._version = "0.01"
		self._settings = QSettings("Sandeep Datta", self._appname)
		self.initUi()

	def initUi(self):

		btn = QPushButton("Click me!", self)
		btn.resize(btn.sizeHint())
		btn.clicked.connect(lambda : print ("clicked"))

		self.statusBar()#.showMessage("Ready.")

		self.setupMenu()

		self.setCentralWidget(QTextEdit())

		self.setWindowTitle(self.Title)
		
		self.setWindowIcon(QIcon('main.png'))
		self.moveToCenter()
		geom = self._settings.value("MainWindow.geometry")
		if geom:
			self.restoreGeometry(geom)
			self.show()
		else:
			self.showMaximized()

	def closeEvent(self, event):
		self._settings.setValue("MainWindow.geometry", self.saveGeometry())
		# if self.canCloseApp():
		# 	event.accept()
		# else:
		# 	event.ignore()

	def canCloseApp(self):
		reply = QMessageBox.question(self, self._appname
										, "Are you sure you want to quit?"
										, QMessageBox.Yes | QMessageBox.No
										, QMessageBox.No)
		return reply == QMessageBox.Yes

	def moveToCenter(self):
		rect = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		rect.moveCenter(cp)
		self.move(rect.topLeft())

	def setupMenu(self):
		exitAction = QAction(QIcon.fromTheme("application-exit", QIcon(":/exit.png")), "E&xit", self)
		exitAction.setShortcut("Ctrl+Q")
		exitAction.setStatusTip("Exit application")
		exitAction.triggered.connect(self.close)

		mbar = self.menuBar()
		fileMenu = mbar.addMenu("&File")
		fileMenu.addAction(exitAction)

		tbar = self.addToolBar("main")
		tbar.addAction(exitAction)