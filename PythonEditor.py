from PyQt4.QtGui import *
from PyQt4.Qsci import *
from Decorators import *

class PythonEditor(QsciScintilla):

	ARROW_MARKER_NUM = 8

	def __init__(this, parent = None):
		super().__init__(parent)

		this._font = this.getFont("Courier")
		
		this.setFont(this._font)
		
		#setup event handlers
		this.linesChanged.connect(this.onLinesChanged)
		
		
		this._fontMetrics = QFontMetrics(this._font)
		this.setMarginsFont(this._font)
		this.setMarginLineNumbers(0, True)
		this.setMarginsBackgroundColor(QColor("#cccccc"))

		#setup marker mechanism
		#Clickable margin 1 for showing markers
		this.setMarginSensitivity(1, True)
		this.marginClicked.connect(this.onMarginClicked)
		this.markerDefine(QsciScintilla.RightArrow, this.ARROW_MARKER_NUM)
		this.setMarkerBackgroundColor(QColor("#ee1111"), this.ARROW_MARKER_NUM)
		
		# Brace matching: enable for a brace immediately before or after
		# the current position
		#
		this.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		lexer = QsciLexerPython()
		lexer.setDefaultFont(this._font)
		this.setLexer(lexer)

		this.setAutoIndent(True)

		this.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
		this.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTH, 1)
		this.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
		

	def onLinesChanged(this):
		this.setMarginWidth(0, this._fontMetrics.width("0") * this.numDigits(this.lines())  + 6)

	def onMarginClicked(this, margin, line, keyboardState):
		# Toggle marker for the line the margin was clicked on
		if this.markersAtLine(line) != 0:
			this.markerDelete(line, this.ARROW_MARKER_NUM)
		else:
			this.markerAdd(line, this.ARROW_MARKER_NUM)
	
	def numDigits(this, num):
		return len(str(num))
	
	@memoized
	def getFont(this, family, sizeInPoints=10, fixed=False):
		font = QFont()
		font.setFamily(family)
		font.setPointSize(sizeInPoints)
		font.setFixedPitch(fixed)

		return font
