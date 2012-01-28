"""
Python module containing the entry point for the BrainForge IDE
(C) 2012 Sandeep Datta
"""

import sys
from PyQt4.QtGui import *
from BrainForge import *

def main(args):
	app = QApplication(args)

	mw = BrainForge()
	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main(sys.argv)