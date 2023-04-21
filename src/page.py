from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

from fonts import real_font_size
from qt_saving_layer import N_QGraphicsTextItem, N_QGraphicsScene, N_QGraphicsRectItem

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
		self.scene = N_QGraphicsScene(QGraphicsScene(0, 0, Page.WIDTH, Page.HEIGHT))

		# real page number, not an index
		self.page_number = page_number

		# setup white background
		self.rect = N_QGraphicsRectItem(QGraphicsRectItem(0, 0, Page.WIDTH, Page.HEIGHT))
		self.rect.qt().setBrush(QBrush(Qt.white))
		self.scene.qt().addItem(self.rect.qt())

		# add page number text
		if (page_number > 1):
			align = "right"
			if (page_number % 2 == 0):
				align = "left"
			self.page_number_text = DocumentTextitem(False, str(page_number), real_font_size(10, Page.HEIGHT), Page.MARGIN / 2, align, Page.MARGIN, False)
			self.scene.qt().addItem(self.page_number_text.qt())

	def update_page_text(self):
		self.page_number_text.alignment = "right"
		if (self.page_number % 2 == 0):
			self.page_number_text.alignment = "left"

		self.page_number_text.qt().setPlainText(str(self.page_number))
		self.page_number_text.align()

	
class DocumentTextitem(N_QGraphicsTextItem):
	def __init__(self, allow_interaction: bool, text: str, fontSize: float, y: float, alignment: str, align_spacing: float, bold: bool):
		"""
		`alignment`: "right", "left, ""center"
		"""
		super().__init__(QGraphicsTextItem(text))

		font = QFont("Times New Roman", fontSize)
		font.setBold(bold)
		self.qt().setFont(font)
		self.qt().setDefaultTextColor(Qt.black)

		if (allow_interaction):
			# interaction
			self.qt().setTextInteractionFlags(Qt.TextEditorInteraction)
			self.qt().document().setMaximumBlockCount(1)

		# alignment and positioning
		self.alignment = alignment
		self._y = y
		self.align_spacing = align_spacing
		self.align()
		self.qt().document().contentsChanged.connect(self.align)

	def crop_text(self):
		# set maximum width
		while (self.qt().boundingRect().width() > (Page.WIDTH - 2 * self.align_spacing)):
			self.qt().document().blockSignals(True)
			cursor = self.qt().textCursor()
			old_cursor_pos = cursor.position()
			# remove character which was added by the user at the cursor position
			self.qt().setPlainText(self.qt().toPlainText()[:old_cursor_pos - 1] + self.qt().toPlainText()[old_cursor_pos:])
			new_pos = old_cursor_pos - 1
			if (new_pos >= 0):
				cursor.setPosition(old_cursor_pos - 1)
			self.qt().setTextCursor(cursor)
			self.qt().document().blockSignals(False)

	def align(self):
		self.crop_text()
		x_align = 0
		if (self.alignment == "right"):
			x_align = Page.WIDTH - self.align_spacing - self.qt().boundingRect().width()
		elif (self.alignment == "left"):
			x_align = self.align_spacing
		elif (self.alignment == "center"):
			x_align = Page.WIDTH / 2 - self.qt().boundingRect().width() / 2
			
		self.qt().setPos(x_align, self._y)
	def remove_highlight(self):
		# work around to remove highlighted text
		cursor = self.qt().textCursor()
		cursor.setPosition(len(self.qt().toPlainText()))
		self.qt().setTextCursor(cursor)

	# !!
	# this is really important to avoid a program crash when rightklicking an QGraphicstextItem!
	def contextMenuEvent(self, event):
		event.ignore()
