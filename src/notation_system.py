from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItemGroup, QGraphicsRectItem
from PyQt5.QtGui import QPen, QTransform, QFont, QColor
from PyQt5.QtCore import QPointF, Qt, QLineF, QRectF

from typing import List, Union

from settings import Settings
from fonts import real_font_size, get_symbol, get_one_em, get_specification
from qt_saving_layer import N_QGraphicsItemGroup, N_QGraphicsLineItem, Fixed_QGraphicsTextItem, N_QGraphicsTextItem
from misc import bound, bound_in_intervals
from copy import deepcopy

# important: the vertical center of every music (text) item is the bottom line of the 5 lines of a stave
# also important: always use sceneBoundingRect which will update when transforming the item
class Musicitem(N_QGraphicsTextItem):
	"""Always scale and transform with QTransform, which can be pickled.\n
	Transform first, then position.
	"""
	# em space (typically width of "M", here height of one bar line)
	# -> stave lines spacing = em / 4
	EM = get_one_em(Settings.Symbols.FONTSIZE)
	MIN_OBJ_DIST = EM / 6

	def __init__(self, symbol: Union[str, List[str]] = "", color: QColor = Qt.black):
		super().__init__(Fixed_QGraphicsTextItem(""))

		self.change_text(symbol)
		self.qt().setFont(QFont("Bravura", real_font_size(Settings.Symbols.FONTSIZE)))
		self.qt().setDefaultTextColor(color)

		self.deleting = False

	def change_text(self, symbol: Union[str, List[str]] = ""):
		self.key = symbol
		text = ""
		if (symbol != ""):
			text = get_symbol(symbol)
		self.qt().setPlainText(text)

	def get_line_y(line: int) -> float:
		return Musicitem.EM - line * (Musicitem.EM / 4)

	def spec_to_px(spec: float) -> float:
		return Musicitem.EM / 4 * spec

	def get_character_width(key):
		box = get_specification("glyphBBoxes", key)
		return Musicitem.spec_to_px(box["bBoxNE"][0] - box["bBoxSW"][0])

	def get_qt_blank_space(self):
		key_ = self.key
		real_width = 0
		qt_width = self.qt().sceneBoundingRect().width()

		if (type(self.key) != str):
			# time signatures

			possible_widths = []

			if (len(self.key) > 4):
				# special case: time signature 12/8 (and others maybe added later)
				if (self.key[2] == "timeSigCombNumerator"):
					possible_widths.append(Musicitem.get_character_width(self.key[1]) + Musicitem.get_character_width(self.key[3]))
					if (len(self.key) > 6 and self.key[6] == "timeSigCombDenominator"):
						possible_widths.append(Musicitem.get_character_width(self.key[5]) + Musicitem.get_character_width(self.key[7]))
				elif (self.key[4] == "timeSigCombDenominator"):
					possible_widths.append(Musicitem.get_character_width(self.key[3]) + Musicitem.get_character_width(self.key[5]))
			else:
				possible_widths.append(Musicitem.get_character_width(self.key[1]))
				possible_widths.append(Musicitem.get_character_width(self.key[3]))

			real_width = max(possible_widths)
		else:
			real_width = Musicitem.get_character_width(key_)

		real_width *= self.qt().transform().m11()
		return (qt_width - real_width) / 2

	def set_real_x(self, ax: float):
		self.qt().setX(ax - self.get_qt_blank_space())

	def set_real_y(self, ay: float):
		"""get bottom stave line matching"""
		self.qt().setY(ay - self.qt().sceneBoundingRect().height() / 2)

	def set_real_pos(self, ax: float, ay: float):
		"""left side of the symbol (x), relative to its bottom line position"""
		self.set_real_x(ax)
		self.set_real_y(ay)

	def get_real_width(self):
		return self.qt().sceneBoundingRect().width() - 2 * self.get_qt_blank_space()

	def get_real_height(self):
		if (type(self.key) != str):
			# time signatures
			return Musicitem.EM
		box = get_specification("glyphBBoxes", self.key)
		return Musicitem.spec_to_px(abs(box["bBoxSW"][1] - box["bBoxNE"][1])) * self.qt().transform().m22()

	def get_real_x(self):
		"""relative to its itemgroup"""
		return self.qt().scenePos().x() + self.get_qt_blank_space()

	def get_real_relative_x(self):
		"""relative to its itemgroup"""
		return self.qt().x() + self.get_qt_blank_space()
	
	def get_real_y(self):
		return self.qt().scenePos().y() + self.qt().sceneBoundingRect().height() / 2

	def get_real_relative_y(self):
		return self.qt().y() + self.qt().sceneBoundingRect().height() / 2
	
	def get_bounding_rect(self) -> QRectF:
		if (type(self.key) != str):
			# time signatures
			return QRectF(
				self.get_real_x(),
				self.get_real_y() - Musicitem.EM,
				self.get_real_width(),
				Musicitem.EM
			)
		else:
			return QRectF(
				self.get_real_x(),
				self.get_real_y() - Musicitem.spec_to_px(get_specification("glyphBBoxes", self.key)["bBoxNE"][1]) * self.qt().transform().m22(),
				self.get_real_width(),
				self.get_real_height()
			)
		
	def change_color(self, color: QColor):
		self.qt().setDefaultTextColor(color)

	def select_deleting(self):
		self.deleting = True
		self.change_color(QColor(Settings.Gui.DELETE_COLOR))

	def unselect_deleting(self):
		self.deleting = False
		self.change_color(Qt.black)

def get_entire_extent(items: List[Musicitem]) -> float:
	start_points = []
	end_points = []

	for item in items:
		start_points.append(item.get_real_relative_x())
		end_points.append(item.get_real_relative_x() + item.get_real_width())

	return max(end_points) - min(start_points)

class MusicitemGroup(N_QGraphicsItemGroup):
	def __init__(self, items: List[Musicitem]):
		super().__init__(QGraphicsItemGroup())
	
		self.items: List[Musicitem] = items
		self.qt().setPos(self.items[0].qt().pos())

		for item in self.items:
			item.qt().setDefaultTextColor(Qt.black)
			self.qt().addToGroup(item.qt())

		self.deleting = False
	
	def reassemble(self):
		for item in self.items:
			self.qt().addToGroup(item.qt())

		self.qt().setPos(self._pos)

	def get_real_width(self):
		return get_entire_extent(self.items)
	
	def get_real_relative_x(self):
		rel_x = min(self.items, key=lambda item: item.get_real_relative_x()).get_real_relative_x()
		return self.qt().pos().x() + rel_x
	
	def get_bounding_rect(self) -> QRectF:
		bounding_rects = [item.get_bounding_rect() for item in self.items]

		left = min([rect.x() for rect in bounding_rects])
		top = min([rect.y() for rect in bounding_rects])
		right = max([rect.x() + rect.width() for rect in bounding_rects])
		bottom = max([rect.y() + rect.height() for rect in bounding_rects])

		return QRectF(left, top, right - left, bottom - top)
	
	def change_color(self, color: QColor):
		for item in self.items:
			item.qt().setDefaultTextColor(color)
	
	def select_deleting(self):
		self.deleting = True
		self.change_color(QColor(Settings.Gui.DELETE_COLOR))

	def unselect_deleting(self):
		self.deleting = False
		self.change_color(Qt.black)

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

class Rest(MusicitemGroup):
	SYMBOLS = [
		"restWhole",
		"restHalf",
		"restQuarter",
		"rest8th",
		"rest16th",
		"rest32nd",
		"rest64th",
	]

	def __init__(self, rest: Musicitem):
		super().__init__([rest])

class Clef(Musicitem):
	SYMBOLS = [
		{
			"lines": [1],
			"smufl_key": "gClefChange",
		},
		{
			"lines": [3],
			"smufl_key": "fClefChange",
		},
		{
			"lines": [2, 3],
			"smufl_key": "cClefChange",
		},
	]

	def __init__(self, clef: Musicitem, n: int):
		super().__init__()
		self.change_text(Clef.SYMBOLS[n]["smufl_key"])
		self.qt().setDefaultTextColor(Qt.black)
		self.qt().setPos(clef.qt().pos())

class Note(MusicitemGroup):
	SYMBOLS = [
		"noteheadWhole",
		"noteheadHalf",
		"noteheadBlack",
	]

	# add Up / Down
	FLAGS = [
		"flag8th",
		"flag16th",
		"flag32nd",
		"flag64th",
	]

	def __init__(self, notehead: Musicitem, stem: Musicitem, flag: Musicitem, leger_lines: List[Musicitem]):
		items = []
		items.append(notehead)
		items.extend(leger_lines)

		if (stem.key != ""):
			items.append(stem)

		if (flag.key != ""):
			items.append(flag)

		super().__init__(items)

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
	def __init__(self, time_signature: TimeSignature):
		super().__init__(QGraphicsItemGroup())

		self.time_signature: TimeSignature = time_signature
		self.time_signature_visible = False

		self.objects: List[Union[Musicitem, MusicitemGroup]] = []
		self.left_bar_line: Musicitem = None

	def show_time_signature(self, new_time_sig_name: str = None):
		if (new_time_sig_name != None):
			self.time_signature.change_name(new_time_sig_name)
		if (not self.time_signature_visible):
			self.time_signature_visible = True
			self.qt().addToGroup(self.time_signature.qt())
		self.time_signature.set_real_pos(Musicitem.MIN_OBJ_DIST, Musicitem.EM)

	def hide_time_signature(self):
		self.time_signature_visible = False
		self.time_signature.change_color(Qt.black)
		# qt() object visually removed from scene by editing.py when calling this function

	def add_left_bar_line(self, bar_line: Musicitem, stave_y: float):
		self.left_bar_line = deepcopy(bar_line)
		self.left_bar_line.qt().setDefaultTextColor(Qt.black)
		self.qt().addToGroup(self.left_bar_line.qt())
		self.left_bar_line.set_real_x(-self.left_bar_line.get_real_width())
		self.left_bar_line.qt().setY(self.left_bar_line.qt().scenePos().y() - stave_y)

	def get_start(self) -> float:
		total_start_x = self.qt().scenePos().x() + Musicitem.MIN_OBJ_DIST
		if (self.time_signature_visible):
			total_start_x += self.time_signature.get_real_width() + Musicitem.MIN_OBJ_DIST
		return total_start_x
	
	def get_end(potential_items: List[Musicitem], next_bar_x: float) -> float:
		return next_bar_x - get_entire_extent(potential_items) - Musicitem.MIN_OBJ_DIST

	def find_places(self, potential_items: List[Musicitem], next_bar_x: float) -> List[List[float]]:
		"""returns intervals of real Musicitem x-coordinates (not qt object position) including spacing, relative to (0, 0)"""
		intervals = []
		items_width = get_entire_extent(potential_items)
		total_start_x = self.get_start()
		total_end_x = Bar.get_end(potential_items, next_bar_x)

		if (len(self.objects) >= 1):
			first_end_x = self.objects[0].get_real_relative_x() + self.qt().scenePos().x() - items_width - Musicitem.MIN_OBJ_DIST 
			if (first_end_x - total_start_x >= 0):
				intervals.append([total_start_x, first_end_x])

			for n, obj in enumerate(self.objects):
				start_x = obj.get_real_relative_x() + self.qt().scenePos().x() + obj.get_real_width()  + Musicitem.MIN_OBJ_DIST
				end_x = total_end_x

				if (n < len(self.objects) - 1):
					end_x = self.objects[n + 1].get_real_relative_x() + self.qt().scenePos().x() - items_width - Musicitem.MIN_OBJ_DIST

				if (end_x - start_x >= 0):
					intervals.append([start_x, end_x])
		else:
			if (total_end_x - total_start_x >= 0):
				intervals.append([total_start_x, total_end_x])

		return intervals
	
	def add_object(self, new_obj: Union[Musicitem, N_QGraphicsItemGroup]):
		self.qt().addToGroup(new_obj.qt())

		i = len(self.objects)

		for i_, obj in enumerate(self.objects):
			if (obj.get_real_relative_x() > new_obj.get_real_relative_x()):
				i = i_
				break

		self.objects.insert(i, new_obj)

	def add_rest(self, rest: Musicitem):
		new_rest = Rest(deepcopy(rest))
		self.add_object(new_rest)

	def add_clef(self, clef: Musicitem, n: int):
		new_clef = Clef(deepcopy(clef), n)
		self.add_object(new_clef)

	def add_note(self, notehead: Musicitem, stem: Musicitem, flag: Musicitem, leger_lines: List[Musicitem]):
		new_note = Note(deepcopy(notehead), deepcopy(stem), deepcopy(flag), [deepcopy(leger_line) for leger_line in leger_lines])
		self.add_object(new_note)

	def reassemble(self):
		if (self.time_signature_visible):
			self.qt().addToGroup(self.time_signature.qt())
		if (self.left_bar_line != None):
			self.qt().addToGroup(self.left_bar_line.qt())

		for obj in self.objects:
			self.qt().addToGroup(obj.qt())
			# insert other types later
			if (type(obj).__bases__[0] == MusicitemGroup):
				obj.reassemble()

class Stave(N_QGraphicsItemGroup):
	"""This is a (N_)QGraphicsItemGroup to move all its members at once.\n
	All positions are relative to the parent from here on!\n
	0 = bottom line\n
	0.5 = first space from the bottom \n
	1 = 2nd line from the bottom\n
	...\n
	e.g. -1 would be c (with g clef)\n
	"""

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

		line_pen = QPen(Qt.black, Musicitem.spec_to_px(get_specification("engravingDefaults", "staffLineThickness")))
		
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
			y = Musicitem.get_line_y(i)
			# the line width creates an extra width
			line = N_QGraphicsLineItem(QGraphicsLineItem(line_pen.width() / 2, y, self.width - line_pen.width() / 2, y))
			line.qt().setPen(line_pen)
			self.lines.append(line)
			self.qt().addToGroup(line.qt())

		# add clef
		self.clef = Musicitem(Stave.clefs[self.clef_key]["smufl_key"])
		self.qt().addToGroup(self.clef.qt())
		self.clef.set_real_pos(Musicitem.MIN_OBJ_DIST, Musicitem.get_line_y(Stave.clefs[self.clef_key]["line"]))

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
			x = self.clef.get_real_relative_x() + self.clef.get_real_width() + Musicitem.MIN_OBJ_DIST
			if (i > 0):
				x = self.key_signature_accidentals[i - 1].get_real_relative_x() + self.key_signature_accidentals[i - 1].get_real_width()
			y = Musicitem.get_line_y(KeySignature.accidentals_positions[self.key_signature.type - 1][i] + Stave.clefs[clef_key]["accidental_shift"])
			accidental.set_real_pos(x, y)
			self.key_signature_accidentals.append(accidental)

	def create_first_bar(self, first_system: bool, start_x: float, time_signature: TimeSignature):
		self.bars.append(Bar(time_signature))
		self.qt().addToGroup(self.bars[0].qt())
		self.bars[0].qt().setPos(start_x, 0)

		if (first_system):
			self.bars[0].show_time_signature()

	def split_bar(self, bar_index: int):
		# bar_index + 1 is the new (atm empty) bar (index)
		remove_index = None
		
		for n, obj in enumerate(self.bars[bar_index].objects):
			if (obj.get_real_relative_x() + self.bars[bar_index].qt().scenePos().x() > self.bars[bar_index + 1].qt().scenePos().x()):
				if (remove_index is None):
					remove_index = n
				self.bars[bar_index].qt().removeFromGroup(obj.qt())
				self.bars[bar_index + 1].qt().addToGroup(obj.qt())
				self.bars[bar_index + 1].add_object(obj)

		if (remove_index != None):
			self.bars[bar_index].objects[:] = self.bars[bar_index].objects[:remove_index]
	
	def delete_bar_head(self, bar_index: int):
		for item in self.bars[bar_index].objects:
			self.bars[bar_index].qt().removeFromGroup(item.qt())
			self.bars[bar_index - 1].qt().addToGroup(item.qt())
			self.bars[bar_index - 1].add_object(item)

		self.bars.pop(bar_index)

	def add_bar(self, bar_lines: List[Musicitem], staves: int, stave_index: int, with_piano: bool):
		x = bar_lines[0].get_real_relative_x() + bar_lines[0].get_real_width()
		system_x = x - self.qt().scenePos().x()

		i = len(self.bars)

		for i_, bar in enumerate(self.bars):
			if (bar.qt().scenePos().x() > x):
				i = i_
				break

		# only add bar line once (check stave_index)
		new_bar = Bar(deepcopy(self.bars[i - 1].time_signature))
		if (with_piano and staves - 2 == stave_index):
			new_bar.add_left_bar_line(bar_lines[1], self.qt().scenePos().y())

		if ((not (with_piano and staves == 2)) and stave_index == 0):
			new_bar.add_left_bar_line(bar_lines[0], self.qt().scenePos().y())

		self.bars.insert(i, new_bar)
		self.qt().addToGroup(new_bar.qt())
		new_bar.qt().setPos(system_x, 0)

		self.split_bar(i - 1)

	def get_center(self) -> QPointF:
		return QPointF(self.qt().scenePos().x() + self.width / 2, self.qt().scenePos().y() + Musicitem.EM / 2)

	def get_closest_line(self, mouse_pos: QPointF, steps: int = 2) -> int:
		step = Musicitem.EM / 4
		n = (self.qt().scenePos().y() + Musicitem.EM - mouse_pos.y()) / step
		# with multiplying by two, rounding and the dividing again, we get 0.5 steps
		n *= steps
		return bound(round(n) / steps, -10, 10)

	def get_closest_bar_n(self, mouse_pos: QPointF) -> int:
		bar_line_intervals = []
		for n, bar in enumerate(self.bars):
			next_bar_x = 0
			bar_x = bar.qt().scenePos().x()

			if (n != len(self.bars) - 1):
				next_bar_x = self.bars[n + 1].qt().scenePos().x()
			else:
				next_bar_x = Settings.Layout.WIDTH - Settings.Layout.MARGIN

			bar_line_intervals.append([bar_x, next_bar_x])

		# return the index of the closest interval / interval border
		return bound_in_intervals(mouse_pos.x(), bar_line_intervals, True)

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

		self.free_objects: List[Union[Musicitem, MusicitemGroup]] = []

		self.first_system = first_system

		for n, stave in enumerate(self.staves):
			self.qt().addToGroup(stave.qt())
			stave.qt().setPos(0, n * (Musicitem.EM + System.min_stave_spacing))
			stave.create_first_bar(self.first_system, self.get_start_x(), deepcopy(time_signature))

		# setup the left bar line
		self.left_bar_line = Musicitem("barlineSingle")
		self.left_bar_line.qt().setTransform(QTransform().scale(1, (self.get_bottom_y() - self.qt().y()) / Musicitem.EM))
		self.qt().addToGroup(self.left_bar_line.qt())
		self.left_bar_line.set_real_pos(0, self.get_bottom_y() - self.qt().y())

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
		self.brace.set_real_pos(-self.brace.get_real_width() - Musicitem.EM / 16, self.staves[-1].qt().y() + Musicitem.EM)

	def get_start_x(self):
		staves_start_x = []
		for stave in self.staves:
			if (self.key_signature.number > 0):
				staves_start_x.append(stave.key_signature_accidentals[-1].qt().sceneBoundingRect().width() + stave.key_signature_accidentals[-1].qt().pos().x())
			else:
				staves_start_x.append(stave.clef.qt().sceneBoundingRect().width() + stave.clef.qt().pos().x())
		return max(staves_start_x)

	def set_normal_end_bar_line(self):
		self.right_bar_line.change_text("barlineSingle")
		self.right_bar_line.set_real_pos(self.width - self.right_bar_line.get_real_width(), self.get_bottom_y() - self.qt().y())

	def set_end_bar_line(self):
		self.right_bar_line.change_text("barlineFinal")
		self.right_bar_line.set_real_pos(self.width - self.right_bar_line.get_real_width(), self.get_bottom_y() - self.qt().y())

	def get_bottom_y(self) -> float:
		return self.staves[-1].qt().scenePos().y() + Musicitem.EM

	def get_height(self) -> float:
		return self.get_bottom_y() - self.qt().y()

	# only call when with_piano = True
	def get_bottom_other_voices_y(self) -> float:
		y = None
		if (len(self.staves) > 2):
			y = self.staves[-3].qt().scenePos().y() + Musicitem.EM
		else:
			y = self.get_bottom_y()
		return y

	# only call when with_piano = True
	def get_other_voices_height(self) -> float:
		height = None
		if (len(self.staves) > 2):
			height = self.get_bottom_other_voices_y() - self.qt().scenePos().y()
		return (height)

	def get_piano_height(self) -> float:
		height = None
		if (len(self.staves) > 1):
			height = self.staves[-1].qt().scenePos().y() + Musicitem.EM - self.staves[-2].qt().scenePos().y()
		return height

	def get_center(self) -> QPointF:
		return QPointF(self.qt().x() + self.width / 2, self.qt().y() + self.get_height() / 2)

	def get_closest_stave(self, mouse_pos: QPointF) -> Stave:
		stave_distances = []
		staves: List[Stave] = []
		for stave in self.staves:
			stave_distances.append(QLineF(stave.get_center(), mouse_pos).length())
			staves.append(stave)

		return staves[stave_distances.index(min(stave_distances))]

	def add_free_item(self, item: Musicitem):
		new_item = deepcopy(item)
		new_item.qt().setDefaultTextColor(Qt.black)
		self.qt().addToGroup(new_item.qt())
		self.free_objects.append(new_item)

	def reassemble(self):
		for n, stave in enumerate(self.staves):
			stave.reassemble()
			self.qt().addToGroup(stave.qt())
			stave.qt().setPos(stave._pos)

		if (self.with_piano):
			self.qt().addToGroup(self.brace.qt())

		self.qt().addToGroup(self.right_bar_line.qt())
		self.qt().addToGroup(self.left_bar_line.qt())

		for obj in self.free_objects:
			self.qt().addToGroup(obj.qt())