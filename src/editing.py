from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QFont, QPen, QColor
from PyQt5.QtCore import Qt

from fonts import real_font_size, get_symbol, get_one_em
from qt_saving_layer import Fixed_QGraphicsTextItem, N_QGraphicsScene, N_QGraphicsRectItem, N_QGraphicsTextItem
from typing import List, Union
from settings import Settings

# important: the vertical center of every music (text) item is the bottom line of the 5 lines of a stave
# also important: always use sceneBoundingRect which will update when transforming the item
class Musicitem(N_QGraphicsTextItem):
	"""Always scale and transform with QTransform, which can be pickled."""
	# em space (typically width of "M", here height of one bar line)
	# -> stave lines spacing = em / 4
	EM = get_one_em(Settings.Symbols.FONTSIZE)

	def __init__(self, symbol: Union[str, List[str]] = "", color: QColor  = Qt.black):
		super().__init__(Fixed_QGraphicsTextItem(""))

		self.change_text(symbol)
		self.qt().setFont(QFont("Bravura", real_font_size(Settings.Symbols.FONTSIZE)))
		self.qt().setDefaultTextColor(color)

	def setPos(self, ax: float, ay: float):
		"""overwrite function to achieve bottom stave line matching"""
		super().qt().setPos(ax, ay - self.qt().sceneBoundingRect().height() / 2)

	def change_text(self, symbol: Union[str, List[str]] = ""):
		text = ""
		if (symbol != ""):
			text = get_symbol(symbol)
		self.qt().setPlainText(text)

class EditQGraphicsScene(QGraphicsScene):
	def __init__(self, x: float, y: float, width: float, height: float):
		super().__init__(x, y, width, height)
		self.edit_object = Musicitem()

	def mouseMoveEvent(self, event):
		pos = event.scenePos()

class Page(N_QGraphicsScene):
	def __init__(self, page_number: int):
		super().__init__(EditQGraphicsScene(0, 0, Settings.Layout.WIDTH, Settings.Layout.HEIGHT))

		# real page number, not an index
		self.page_number = page_number

		# setup white background
		self.rect = N_QGraphicsRectItem(QGraphicsRectItem(0, 0, Settings.Layout.WIDTH, Settings.Layout.HEIGHT))
		self.rect.qt().setBrush(QBrush(Qt.white))
		self.rect.qt().setPen(QPen(Qt.white))
		self.qt().addItem(self.rect.qt())

		# add page number text
		if (page_number > 1):
			align = "right"
			if (page_number % 2 == 0):
				align = "left"
			self.page_number_text = DocumentTextitem(False, str(page_number), real_font_size(10), Settings.Layout.MARGIN / 2, align, Settings.Layout.MARGIN, False)
			self.qt().addItem(self.page_number_text.qt())

	def update_page_text(self):
		self.page_number_text.alignment = "right"
		if (self.page_number % 2 == 0):
			self.page_number_text.alignment = "left"

		self.page_number_text.qt().setPlainText(str(self.page_number))
		self.page_number_text.align()

	def reassemble(self):
		self.qt().addItem(self.rect.qt())
		if (self.page_number > 1):
			self.qt().addItem(self.page_number_text.qt())

class DocumentTextitem(N_QGraphicsTextItem):
	def __init__(self, allow_interaction: bool, text: str, fontSize: float, y: float, alignment: str, align_spacing: float, bold: bool):
		"""
		`alignment`: "right", "left, ""center"
		"""
		super().__init__(Fixed_QGraphicsTextItem(text))

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
		self.connect_contentchange()

	def connect_contentchange(self):
		self.qt().document().contentsChanged.connect(self.align)

	def crop_text(self):
		# set maximum width
		while (self.qt().boundingRect().width() > (Settings.Layout.WIDTH - 2 * self.align_spacing)):
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
			x_align = Settings.Layout.WIDTH - self.align_spacing - self.qt().boundingRect().width()
		elif (self.alignment == "left"):
			x_align = self.align_spacing
		elif (self.alignment == "center"):
			x_align = Settings.Layout.WIDTH / 2 - self.qt().boundingRect().width() / 2
			
		self.qt().setPos(x_align, self._y)
	def remove_highlight(self):
		# work around to remove highlighted text
		cursor = self.qt().textCursor()
		cursor.setPosition(len(self.qt().toPlainText()))
		self.qt().setTextCursor(cursor)

	# automatically reconnect the align function
	def __setstate__(self, d):
		super().__setstate__(d)
		self.__dict__.update(d)
		self.connect_contentchange()
