from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from fonts import get_symbol, real_font_size
from page import Page
from fonts import get_one_em
from typing import List, Union

from qt_saving_layer import N_QGraphicsTextItem

# important: the vertical center of every music (text) item is the bottom line of the 5 lines of a stave
# also important: always use sceneBoundingRect which cares about transformations .....
class Musicitem(N_QGraphicsTextItem):
	"""Always scale and transform with QTransform, which can be pickled."""
	FONTSIZE = 24
	# em space (typically width of "M", here height of one bar line)
	# -> stave lines spacing = em / 4
	EM = get_one_em(FONTSIZE, Page.HEIGHT)
	def __init__(self, symbol: Union[str, List[str]]):
		super().__init__(QGraphicsTextItem(get_symbol(symbol)))

		self.qt().setFont(QFont("Bravura", real_font_size(Musicitem.FONTSIZE, Page.HEIGHT)))
		self.qt().setDefaultTextColor(Qt.black)

	def setPos(self, ax: float, ay: float):
		"""overwrite function to achieve bottom stave line matching"""
		super().qt().setPos(ax, ay - self.qt().sceneBoundingRect().height() / 2)
