from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from fonts import get_symbol, real_font_size
from page import Page
from fonts import get_one_em

# important: the vertical center of every music (text) item is the bottom line of the 5 lines of a stave
# also important: always use sceneBoundingRect which cares about transformations .....
class Musicitem(QGraphicsTextItem):
	FONTSIZE = 24
	# em space (typically width of "M", here height of one bar line)
	# -> stave lines spacing = em / 4
	EM = get_one_em(FONTSIZE, Page.HEIGHT)
	def __init__(self, symbol: str):
		super().__init__()
		
		# for time signatures: get_symbol("timeSigCombNumerator") + get_symbol("timeSig7") + get_symbol("timeSigCombDenominator") + get_symbol("timeSig8")
		self.setPlainText(get_symbol(symbol))
		self.setFont(QFont("Bravura", real_font_size(Musicitem.FONTSIZE, Page.HEIGHT)))
		self.setDefaultTextColor(Qt.black)

	def setPos(self, ax: float, ay: float):
		"""overwrite function to achieve bottom stave line matching"""
		super().setPos(ax, ay - self.sceneBoundingRect().height() / 2)