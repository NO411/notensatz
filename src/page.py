from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

from fonts import real_font_size

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
		self.rect = QGraphicsRectItem(0, 0, Page.WIDTH, Page.HEIGHT)
		self.rect.setBrush(QBrush(Qt.white))
		self.scene.addItem(self.rect)

		# add page number text
		if (page_number > 1):
			align = "right"
			if (page_number % 2 == 0):
				align = "left"
			self.page_number_text = DocumentTextitem(False, str(page_number), real_font_size(10, Page.HEIGHT), Page.MARGIN / 2, align, Page.MARGIN, False)
			self.scene.addItem(self.page_number_text)

	def update_page_text(self):
		self.page_number_text.alignment = "right"
		if (self.page_number % 2 == 0):
			self.page_number_text.alignment = "left"

		self.page_number_text.setPlainText(str(self.page_number))
		self.page_number_text.align()

	
class DocumentTextitem(QGraphicsTextItem):
	def __init__(self, allow_interaction: bool, text: str, fontSize: float, y: float, alignment: str, align_spacing: float, bold: bool):
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
		self.align_spacing = align_spacing
		self.align()
		self.document().contentsChanged.connect(self.align)

	def crop_text(self):
		# set maximum width
		while (self.boundingRect().width() > (Page.WIDTH - 2 * self.align_spacing)):
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
			x_align = Page.WIDTH - self.align_spacing - self.boundingRect().width()
		elif (self.alignment == "left"):
			x_align = self.align_spacing
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
