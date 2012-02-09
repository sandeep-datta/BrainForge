"""
The main BrainForge application module
(C) 2012 Sandeep Datta
"""

import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from os import path

from PythonEditor import PythonEditor
from PyTabWidget import *


class BrainForge(QMainWindow):

	@property
	def Title(this):
		return "%s v%s" % (QCoreApplication.applicationName(), QCoreApplication.applicationVersion())

	@property
	def Settings(this):
		return this._settings

	def __init__(this):
		super().__init__()

		QCoreApplication.setOrganizationName("Sandeep Datta");
		QCoreApplication.setOrganizationDomain("sandeepdatta.com");
		QCoreApplication.setApplicationName("Brainforge")
		QCoreApplication.setApplicationVersion("0.02")

		this._settings = QSettings() #note org/app name will be taken from QCoreApplication
		this.initUi()

		this.openFiles = {}
		this.newFiles = {}
		this.nextNewFileIndex = 1

	def initUi(this):

		btn = QPushButton("Click me!", this)
		btn.resize(btn.sizeHint())
		btn.clicked.connect(lambda : print ("clicked"))

		this.statusBar()#.showMessage("Ready.")

		this.setupMenu()
		#this._tabWidget = QTabWidget()

		this._tabWidget = PyTabWidget()
		this._tabWidget.TabWidget.setTabsClosable(True)
		this.setCentralWidget(this._tabWidget)

		this.setWindowTitle(this.Title)
		
		this.setWindowIcon(QIcon('main.png'))
		this.moveToCenter()
		geom = this.Settings.value("MainWindow.geometry")
		if geom:
			this.restoreGeometry(geom)
			this.show()
		else:
			this.showMaximized()

	def closeEvent(this, event):
		this.Settings.setValue("MainWindow.geometry", this.saveGeometry())
		# if this.actionConfirmed("Are you sure you want to quit?"):
		# 	event.accept()
		# else:
		# 	event.ignore()

	def actionConfirmed(this, prompt):
		reply = QMessageBox.question(this, QCoreApplication.applicationName()
										, prompt
										, QMessageBox.Yes | QMessageBox.No
										, QMessageBox.No)
		return reply == QMessageBox.Yes

	def moveToCenter(this):
		rect = this.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		rect.moveCenter(cp)
		this.move(rect.topLeft())

	def setupMenu(this):
		exitAction 		= this.newAction("E&xit", "application-exit", "Alt+F4", "Exit application", this.close)
		newFileAction 	= this.newAction("&New", "document-new", "Ctrl+N", "New file", this.onNewFile)
		openFileAction 	= this.newAction("&Open", "document-open", "Ctrl+O", "Open file", this.onOpenFile)
		closeFileAction = this.newAction("&Close", "window-close", "Ctrl+W", "Close file", this.onCloseFile)
		saveFileAction = this.newAction("&Save", "document-save", "Ctrl+S", "Save file", this.onSaveFile)
		#preferences-desktop-font

		mbar = this.menuBar()
		fileMenu = mbar.addMenu("&File")
		fileMenu.addAction(newFileAction)
		fileMenu.addAction(openFileAction)
		fileMenu.addAction(closeFileAction)
		fileMenu.addAction(saveFileAction)
		fileMenu.addAction(exitAction)

		tbar = this.addToolBar("main")
		tbar.addAction(newFileAction)
		tbar.addAction(openFileAction)
		tbar.addAction(closeFileAction)
		tbar.addAction(saveFileAction)
		tbar.addAction(exitAction)

	def newAction(this, text, stdIconName, shortcut, statusTip, handler):
		icon = QIcon.fromTheme(stdIconName, QIcon(":/%s.png" % (stdIconName)))
		action = QAction(icon, text, this)
		action.setShortcut(shortcut)
		action.setStatusTip(statusTip)
		action.triggered.connect(handler)
		return action
	
	def saveContents(this, tab):
		editor = tab.Widget
		if editor and editor.isModified():
			if not editor._isNewFile:
				with open(editor._fileName, "w") as f:
					f.write(editor.text()) 
			else:
				fname = QFileDialog.getOpenFileName(this, "Save file")
				if fname:
					with open(fname, "w") as f:
						f.write(editor.text())
					this.openFiles[fname] = editor
					del this.newFiles[editor._fileName]
					editor._fileName = fname
					editor._isNewFile = False
					# index = this._tabWidget
					# this._tabWidget.setTabText(index, path.basename(fname))


	def onOpenFile(this):
		fname = QFileDialog.getOpenFileName(this, "Open file")
		print("Opening file:" + fname)

		if fname in this.openFiles and this.openFiles[fname].isModified():
			if not this.actionConfirmed("Do you want to reopen '%s'? All changes will be lost." % fname):
				return

		if fname:
			with open(fname) as f:
				if not fname in this.openFiles:
					this.addTab(fname, False)
				else:
					editor = this.openFiles[fname]
					editor.setText(f.read())
	def addTab(this, fname, isNewFile):
		editor = PythonEditor()
		if not isNewFile:
			with open(fname) as f:
				editor.setText(f.read())
		editor.setModified(False)
		editor._fileName = fname #tack the file name onto the editor for future use
		editor._isNewFile = isNewFile

		if isNewFile:
			this.newFiles[fname] = editor
		else:
			this.openFiles[fname] = editor

		this._tabWidget.addTab(editor, path.basename(fname))
	
	def onCloseFile(this):
		tab = this._tabWidget.currentTab
		this.saveContents(tab)
		this._tabWidget.removeTab(tab)
		del this.openFiles[tab._fileName]


	def onSaveFile(this):
		tab = this._tabWidget.currentTab
		this.saveContents(tab)

	def onNewFile(this):
		fname = "New file" + str(this.nextNewFileIndex)
		this.nextNewFileIndex += 1
		this.addTab(fname, True)