from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

from notation_system import Bar
from typing import List
from fonts import get_symbol

# converts font sizes to pixels in the app
def point_to_px(pt: float):
	# A4 width = 21cm
	# 1 inch = 2,54 cm
	# A4 px width = 2480
	# 1 pt = 1 / 72 inch

	return int((pt * Page.WIDTH / 72) / (21 / 2.54))

class Page:
	# A4 layout
	WIDTH = 2480
	HEIGHT = 3508
	# default margin: ca. 1.54 cm
	# default paper width: 21 cm
	# margin / width = [default margin] / [default paper width]
	# -> margin = width * [default margin] / [default paper width]
	MARGIN = WIDTH * 1.54 / 21

	def __init__(self, page_number: int):
		self.scene = QGraphicsScene(0, 0, Page.WIDTH, Page.HEIGHT)

		# real page number, not an index
		self.page_number = page_number

		# setup white background
		rect = QGraphicsRectItem(0, 0, Page.WIDTH, Page.HEIGHT)
		rect.setBrush(QBrush(Qt.white))
		self.scene.addItem(rect)

		# add page number text
		if (page_number > 1):
			align = "right"
			if (page_number % 2 == 0):
				align = "left"
			self.page_number_text = DocumentTextitem(False, str(page_number), point_to_px(8), Page.MARGIN, align, False)
			self.scene.addItem(self.page_number_text)

	def update_page_text(self):
		self.page_number_text.alignment = "right"
		if (self.page_number % 2 == 0):
			self.page_number_text.alignment = "left"

		self.page_number_text.setPlainText(str(self.page_number))
		self.page_number_text.align()

	def increase_page_number(self):
		self.page_number += 1
		self.update_page_text()
	
	def decrease_page_number(self):
		self.page_number -= 1
		self.update_page_text()

class DocumentUi:
	def __init__(self):
		# table of all pages (those include the scenes)
		self.pages: List[Page] = []

		# references of the objects stored in the scene to be able to access them
		# because it is not always possible to determine the index of the item in the pages[x].items() list
		self.heading = None
		self.sub_heading = None
		self.composer = None

		self.staves = None
		# table of Bar objects
		self.bars: List[Bar] = []

	def setup(self, staves: int, first_bar: Bar):
		# info: first page was already added by page_handling 

		self.staves = staves
		self.bars = [first_bar]
		self.bars[0].setup()

class Musicitem(QGraphicsTextItem):
	def __init__(self, symbol: str):
		super().__init__()
		
		self.setPlainText(get_symbol(symbol))
		self.setFont(QFont("Bravura", point_to_px(17.5)))
		self.setDefaultTextColor(Qt.black)

class DocumentTextitem(QGraphicsTextItem):
	def __init__(self, allow_interaction: bool, text: str, fontSize: float, y: float, alignment: str, bold: bool):
		"""
		`alignment`: "right", "left, ""center"
		"""
		super().__init__()

		# text
		self.setPlainText(text)
		font = QFont("Times New Roman", fontSize)
		font.setBold(bold)
		self.setFont(font)
		self.setDefaultTextColor(Qt.black)

		if (allow_interaction):
			# interaction
			self.setTextInteractionFlags(Qt.TextEditorInteraction)
			self.document().setMaximumBlockCount(1)

		# alignment and positioning
		self.alignment = alignment
		self._y = y
		self.align()
		self.document().contentsChanged.connect(self.align)

	def crop_text(self):
		# set maximum width
		while (self.boundingRect().width() > (Page.WIDTH - 2 * Page.MARGIN)):
			self.document().blockSignals(True)
			cursor = self.textCursor()
			old_cursor_pos = cursor.position()
			# remove character which was added by the user at the cursor position
			self.setPlainText(self.toPlainText()[:old_cursor_pos - 1] + self.toPlainText()[old_cursor_pos:])
			new_pos = old_cursor_pos - 1
			if (new_pos >= 0):
				cursor.setPosition(old_cursor_pos - 1)
			self.setTextCursor(cursor)
			self.document().blockSignals(False)

	def align(self):
		self.crop_text()
		x_align = 0
		if (self.alignment == "right"):
			x_align = Page.WIDTH - Page.MARGIN - self.boundingRect().width()
		elif (self.alignment == "left"):
			x_align = Page.MARGIN
		elif (self.alignment == "center"):
			x_align = Page.WIDTH / 2 - self.boundingRect().width() / 2
			
		self.setPos(x_align, self._y)
	def remove_highlight(self):
		# work around to remove highlighted text
		cursor = self.textCursor()
		cursor.setPosition(len(self.toPlainText()))
		self.setTextCursor(cursor)

	# !!
	# this is really important to avoid a program crash when rightklicking an QGraphicstextItem!
	def contextMenuEvent(self, event):
		event.ignore()