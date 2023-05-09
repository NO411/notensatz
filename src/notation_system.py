from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItemGroup
from PyQt5.QtGui import QPen, QTransform, QFont, QColor
from PyQt5.QtCore import QPointF, Qt, QLineF

from typing import List, Union

from settings import Settings
from fonts import real_font_size, get_symbol, get_one_em
from qt_saving_layer import N_QGraphicsItemGroup, N_QGraphicsLineItem, Fixed_QGraphicsTextItem, N_QGraphicsTextItem
from misc import bound
from copy import deepcopy

# important: the vertical center of every music (text) item is the bottom line of the 5 lines of a stave
# also important: always use sceneBoundingRect which will update when transforming the item
class Musicitem(N_QGraphicsTextItem):
	"""Always scale and transform with QTransform, which can be pickled."""
	# em space (typically width of "M", here height of one bar line)
	# -> stave lines spacing = em / 4
	EM = get_one_em(Settings.Symbols.FONTSIZE)

	def __init__(self, symbol: Union[str, List[str]] = "", color: QColor = Qt.black):
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

	def get_line_y(line: int):
		return Musicitem.EM - line * (Musicitem.EM / 4)

class TimeSignature(Musicitem):
	signatures_map = {
		"2/4-Takt": [2, 4],
        "2/2-Takt": [2, 2],
        "3/2-Takt": [3, 2],
        "3/4-Takt": [3, 4],
        "3/8-Takt": [3, 8],
        "4/4-Takt": [4, 4],
        "5/4-Takt": [5, 4],
        "5/8-Takt": [5, 8],
        "6/4-Takt": [6, 4],
        "6/8-Takt": [6, 8],
        "7/8-Takt": [7, 8],
        "9/8-Takt": [9, 8],
        "12/8-Takt": [12, 8],
	}

	BAR_LINE_DISTANCE = Musicitem.EM / 5
	
	def __init__(self, name: str):
		self.fundamental_beats = TimeSignature.signatures_map[name][0]
		self.note_value = TimeSignature.signatures_map[name][1]
		super().__init__(self.gen_unicode_combi())
	
	def change_name(self, name: str):
		self.fundamental_beats = TimeSignature.signatures_map[name][0]
		self.note_value = TimeSignature.signatures_map[name][1]
		self.change_text(self.gen_unicode_combi())

	def gen_unicode_combi(self) -> List[str]:
		combi_list = []
		if (self.fundamental_beats > 9):
			combi_list.extend(["timeSigCombNumerator", "timeSig" + str(self.fundamental_beats // 10), "timeSigCombNumerator", "timeSig" + str(self.fundamental_beats % 10)])
		else:
			combi_list.extend(["timeSigCombNumerator", "timeSig" + str(self.fundamental_beats)])
		      
		if (self.note_value > 9):
			combi_list.extend(["timeSigCombDenominator", "timeSig" + str(self.note_value // 10), "timeSigCombDenominator", "timeSig" + str(self.note_value % 10)])
		else:
			combi_list.extend(["timeSigCombDenominator", "timeSig" + str(self.note_value)])
		return combi_list
	
	def join_unicode_combi(combi: List[str]):
		return '_'.join(combi)

class Note:
	def __init__(self, pitch: int, duration: float = None):
		# pitch from 1 - 88 (subcontra-a to c5)
		# pitch 0 is a rest
		self.pitch = pitch

		# values: e.g. 0.25 for a quarter note
		# -1 for whole rest
		self.duration = duration
		self.dotted = False

		# sync this to the table in app.py
		# -1 = nothing
		# 0 = ♮
		# 1 = #
		# 2 = b
		# 3 = ##
		# 4 = bb
		
		self.accidental = -1
		# ....
		#self.articulation_sign = 0

# notes that will appear above each other
class NoteGroup:
	def __init__(self):
		self.first_voice: List[Note] = []

class KeySignature:
	signatures_map = {
		# name defined in the combo box : [number of accidentals, type (see Note class)]
		"C-Dur / a-Moll" : [0, 1],
		"G-Dur / e-Moll" : [1, 1],
		"D-Dur / h-Moll" : [2, 1],
		"A-Dur / fis-Moll" : [3, 1],
		"E-Dur / cis-Moll" : [4, 1],
		"H-Dur / gis-Moll" : [5, 1],
		"Fis-Dur / dis-Moll" : [6, 1],
		"Cis-Dur / ais-Moll" : [7, 1],
		"F-Dur / d-Moll" : [1, 2],
		"B-Dur / g-Moll" : [2, 2],
		"Es-Dur / c-Moll" : [3, 2],
		"As-Dur / f-Moll" : [4, 2],
		"Des-Dur / b-Moll" : [5, 2],
		"Ges-Dur / es-moll" : [6, 2],
		"Ces-Dur / as-Moll" : [7, 2],
	}

	accidentals_positions = [
		# #
		[4, 2.5, 4.5, 3, 1.5, 3.5, 2],
		# b
		[2, 3.5, 1.5, 3, 1, 2.5, 0.5],
	]

	def __init__(self, key_signature: str):
		self.number = self.signatures_map[key_signature][0]
		self.type = self.signatures_map[key_signature][1]

class Bar(N_QGraphicsItemGroup):
	MIN_BAR_DIST = Musicitem.EM * 1

	def __init__(self, time_signature: TimeSignature):
		super().__init__(QGraphicsItemGroup())

		self.time_signature = time_signature
		self.time_signature_visible = False

		self.note_groups = []
		self.left_bar_line: Musicitem = None

	def show_time_signature(self, new_time_sig_name: str = None):
		if (new_time_sig_name != None):
			self.time_signature.change_name(new_time_sig_name)
		if (not self.time_signature_visible):
			self.time_signature_visible = True
			self.qt().addToGroup(self.time_signature.qt())
		self.time_signature.setPos(TimeSignature.BAR_LINE_DISTANCE, Musicitem.EM)

	def add_left_bar_line(self, bar_line: Musicitem, stave_y: float):
		self.left_bar_line = deepcopy(bar_line)
		self.left_bar_line.qt().setDefaultTextColor(Qt.black)
		self.qt().addToGroup(self.left_bar_line.qt())
		self.left_bar_line.qt().setPos(-self.left_bar_line.qt().sceneBoundingRect().width() / 2, self.left_bar_line.qt().scenePos().y() - stave_y)

	def reassemble(self):
		if (self.time_signature_visible):
			self.qt().addToGroup(self.time_signature.qt())
		if (self.left_bar_line != None):
			self.qt().addToGroup(self.left_bar_line.qt())

class Stave(N_QGraphicsItemGroup):
	"""This is a (N_)QGraphicsItemGroup to move all its members at once.\n
	All positions are relative to the parent from here on!\n
	0 = bottom line\n
	0.5 = first space from the bottom \n
	1 = 2nd line from the bottom\n
	...\n
	e.g. -1 would be c (with g clef)\n
	"""

	line_pen = QPen(Qt.black, 3)

	clefs = {
		"Violinschlüssel": {
			"line": 1,
			"smufl_key": "gClef",
			"accidental_shift": 0,
		},
		"Bassschlüssel": {
			"line": 3,
			"smufl_key": "fClef",
			"accidental_shift": -1,
		},
		"Altschlüssel": {
			"line": 2,
			"smufl_key": "cClef",
			"accidental_shift": -0.5,
		},
		"Tenorschlüssel": {
			"line": 3,
			"smufl_key": "cClef",
			"accidental_shift": 0.5,
		},
	}

	def __init__(self, clef_key: str, width: float, key_signature: KeySignature):
		super().__init__(QGraphicsItemGroup())

		# setup members
		self.clef_key: str = clef_key
		self.width = width
		self.key_signature: KeySignature = key_signature
		self.lines: List[N_QGraphicsLineItem] = []
		self.bars: List[Bar] = []

		# draw all lines
		for i in range(5):
			# first i is 0
			# first line is the bottom line with index 0 in self.lines...
			y = Musicitem.EM - i * 0.25 * Musicitem.EM
			line = N_QGraphicsLineItem(QGraphicsLineItem(0, y, self.width, y))
			line.qt().setPen(Stave.line_pen)
			self.lines.append(line)
			self.qt().addToGroup(line.qt())

		# add clef
		self.clef = Musicitem(Stave.clefs[self.clef_key]["smufl_key"])
		self.qt().addToGroup(self.clef.qt())
		self.clef.setPos(0.05 * Musicitem.EM, Musicitem.EM - Musicitem.EM * 0.25 * Stave.clefs[self.clef_key]["line"])

		self.key_signature_accidentals: List[Musicitem] = []
		# add key signature
		for i in range(self.key_signature.number):
			# b
			smufl_name = "accidentalSharp"
			if (self.key_signature.type == 2):
				# #
				smufl_name = "accidentalFlat"
			accidental = Musicitem(smufl_name)
			self.qt().addToGroup(accidental.qt())
			x = self.clef.qt().pos().x() + self.clef.qt().sceneBoundingRect().width() + i * (accidental.qt().sceneBoundingRect().width() - 0.1 * Musicitem.EM) + 0.1 * Musicitem.EM
			y = Musicitem.EM - Musicitem.EM * 0.25 * (KeySignature.accidentals_positions[self.key_signature.type - 1][i] + Stave.clefs[clef_key]["accidental_shift"])
			accidental.setPos(x, y)
			self.key_signature_accidentals.append(accidental)

	def create_first_bar(self, first_system: bool, start_x: float, time_signature: TimeSignature):
		self.bars.append(Bar(time_signature))
		self.qt().addToGroup(self.bars[0].qt())
		self.bars[0].qt().setPos(start_x, 0)

		if (first_system):
			self.bars[0].show_time_signature()

	def add_bar(self, bar_line: Musicitem, first_stave: bool):
		x = bar_line.qt().scenePos().x() + bar_line.qt().sceneBoundingRect().width() / 2
		system_x = x - self.qt().scenePos().x()

		i = len(self.bars)

		for i_, bar in enumerate(self.bars):
			if (bar.qt().scenePos().x() > x):
				i = i_
				break

		new_bar = Bar(deepcopy(self.bars[i - 1].time_signature))
		if (first_stave):
			new_bar.add_left_bar_line(bar_line, self.qt().scenePos().y())

		self.bars.insert(i, new_bar)
		self.qt().addToGroup(new_bar.qt())
		new_bar.qt().setPos(system_x, 0)

	def reassemble(self):
		for line in self.lines:
			self.qt().addToGroup(line.qt())

		self.qt().addToGroup(self.clef.qt())

		for accidental in self.key_signature_accidentals:
			self.qt().addToGroup(accidental.qt())
		self.qt().setPos(self._pos)

		for bar in self.bars:
			bar.reassemble()
			self.qt().addToGroup(bar.qt())
			bar.qt().setPos(bar._pos)

	def get_center(self) -> QPointF:
		return QPointF(self.qt().scenePos().x() + self.width / 2, self.qt().scenePos().y() + Musicitem.EM / 2)

	def get_closest_line(self, mouse_pos: QPointF) -> int:
		step = Musicitem.EM / 4
		n = (self.qt().scenePos().y() + Musicitem.EM - mouse_pos.y()) / step
		# with multiplying by two, rounding and the dividing again, we get 0.5 steps 
		n *= 2
		return bound(round(n) / 2, -10, 10)

class System(N_QGraphicsItemGroup):
	"""This is a (N_)QGraphicsItemGroup to move it from one page (QGraphicsScene) to another.\n
	All positions are relative to the parent from here on!\n
	To add an item, first add it and then set a relative position!\n
	Never ever use sceneBoundingRect.y/x()!!"""

	min_stave_spacing = Musicitem.EM * 1.2
	system_spacing = Musicitem.EM * 1.7
	def __init__(self, page_index: int, voices: int, pos: QPointF, clefs_tabel: List[str], key_signature: KeySignature, with_piano: bool, time_signature: TimeSignature, first_system: bool = False):
		super().__init__(QGraphicsItemGroup())

		# setup all members
		self.page_index = page_index
		self.qt().setPos(pos)

		self.width = Settings.Layout.WIDTH - self.qt().x() - Settings.Layout.MARGIN
		self.voices: int = voices
		self.key_signature = key_signature
		self.with_piano: bool = with_piano

		# create staves
		self.staves: List[Stave] = [
			# create all staves using list comprehension
			Stave(clefs_tabel[n], self.width, self.key_signature) for n in range(voices)
		]

		self.first_system = first_system

		for n, stave in enumerate(self.staves):
			self.qt().addToGroup(stave.qt())
			stave.qt().setPos(0, n * (Musicitem.EM + System.min_stave_spacing))
			stave.create_first_bar(self.first_system, self.get_start_x(), deepcopy(time_signature))

		# setup the left bar line
		self.left_bar_line = Musicitem("barlineSingle")
		self.left_bar_line.qt().setTransform(QTransform().scale(1, (self.get_bottom_y() - self.qt().y()) / Musicitem.EM))
		self.qt().addToGroup(self.left_bar_line.qt())
		self.left_bar_line.setPos(-self.left_bar_line.qt().sceneBoundingRect().width() / 2, self.get_bottom_y() - self.qt().y())

		# draw final barline (just to test it)
		self.right_bar_line = Musicitem("barlineFinal")
		self.right_bar_line.qt().setTransform(QTransform().scale(1, (self.get_bottom_y() - self.qt().y()) / Musicitem.EM))
		self.qt().addToGroup(self.right_bar_line.qt())
		self.set_end_bar_line()

		if (self.with_piano and self.voices > 1):
			self.addbrace()

	def addbrace(self):
		self.brace = Musicitem("brace")
		self.qt().addToGroup(self.brace.qt())

		# default brace: 1 EM
		scale = (self.staves[-1].qt().y() - self.staves[-2].qt().y() + Musicitem.EM) / Musicitem.EM
		self.brace.qt().setTransform(QTransform().scale(scale, scale))
		self.brace.setPos(-self.brace.qt().sceneBoundingRect().width(), self.staves[-1].qt().y() + Musicitem.EM)

	def get_start_x(self):
		staves_start_x = []
		for stave in self.staves:
			if (self.key_signature.number > 0):
				staves_start_x.append(stave.key_signature_accidentals[-1].qt().sceneBoundingRect().width() + stave.key_signature_accidentals[-1].qt().pos().x())
			else:
				staves_start_x.append(stave.clef.qt().sceneBoundingRect().width() + stave.clef.qt().pos().x())
		return max(staves_start_x)
	
	def set_normal_end_bar_line(self):
		self.right_bar_line.qt().setPlainText(get_symbol("barlineSingle"))
		self.right_bar_line.setPos(self.width - self.right_bar_line.qt().sceneBoundingRect().width() / 2, self.get_bottom_y() - self.qt().y())
	
	def set_end_bar_line(self):
		self.right_bar_line.qt().setPlainText(get_symbol("barlineFinal"))
		self.right_bar_line.setPos(self.width - self.right_bar_line.qt().sceneBoundingRect().width() / 1.3, self.get_bottom_y() - self.qt().y())

	def get_bottom_y(self) -> float:
		return self.qt().y() + self.staves[-1].qt().y() + Musicitem.EM

	def reassemble(self):
		for n, stave in enumerate(self.staves):
			stave.reassemble()
			self.qt().addToGroup(stave.qt())
			stave.qt().setPos(stave._pos)

		if (self.with_piano):
			self.qt().addToGroup(self.brace.qt())

		self.qt().addToGroup(self.right_bar_line.qt())
		self.qt().addToGroup(self.left_bar_line.qt())
	
	def get_height(self):
		return self.get_bottom_y() - self.qt().y()

	def get_center(self) -> QPointF:
		return QPointF(self.qt().x() + self.width / 2, self.qt().y() + self.get_height() / 2)
	
	def get_closest_stave(self, mouse_pos: QPointF) -> Stave:
		stave_distances = []
		staves: List[Stave] = []
		for stave in self.staves:
			stave_distances.append(QLineF(stave.get_center(), mouse_pos).length())
			staves.append(stave)

		return staves[stave_distances.index(min(stave_distances))]
	
	def get_closest_bar_n(self, mouse_pos: QPointF) -> int:
		bar_distances = []
		indexes: List[int] = []
		# bars have all the same pos for one system
		for n, bar in enumerate(self.staves[0].bars):
			bar_distances.append(QLineF(QPointF(bar.qt().scenePos().x(), 0), mouse_pos).length())
			indexes.append(n)

		return indexes[bar_distances.index(min(bar_distances))]