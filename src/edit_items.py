from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsRectItem, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QBrush, QFont, QPen
from PyQt5.QtCore import Qt

from fonts import real_font_size
from qt_saving_layer import Fixed_QGraphicsTextItem, N_QGraphicsScene, N_QGraphicsRectItem, N_QGraphicsTextItem
from notation_system import Musicitem, System, Stave
from settings import Settings

from typing import List

class EditScene(QGraphicsScene):
	def __init__(self, x: float, y: float, width: float, height: float):
		super().__init__(x, y, width, height)
		self.current_system: System = None
		self.current_stave: Stave = None
		self.current_line: int = None
		self.current_bar_n: int = None
		self.edit_objects: List[Musicitem] = []

		self.setup = False

	# defined by document.py and assembled by main.py
	def custom_move(self, event: QGraphicsSceneMouseEvent): ...
	def custom_pressed(self, event: QGraphicsSceneMouseEvent): ...
	def custom_setup_edit(self, app):...
	# will access self.app (App instance) added by page_handling

	def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
		self.custom_move(event)
		super().mouseMoveEvent(event)
	def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
		self.custom_pressed(event)
		super().mousePressEvent(event)

	def setup_edit(self, app):
		if (not self.setup):
			self.edit_objects: List[Musicitem] = []
			self.custom_setup_edit(app)
			
			self.setup = True

class Page(N_QGraphicsScene):
	def __init__(self, page_number: int):
		super().__init__(EditScene(0, 0, Settings.Layout.WIDTH, Settings.Layout.HEIGHT))
		# real page number, not an index
		self.page_number = page_number
		self.qt().page_number = self.page_number

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
		# important: self.rect not self._rect
		self.qt().addItem(self.rect.qt())
		if (self.page_number > 1):
			self.qt().addItem(self.page_number_text.qt())

		# object was saved as QGraphicsScene, because all the editing stuff is not needed
		self.qt().__class__ = EditScene

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
