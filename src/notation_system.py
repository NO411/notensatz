from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsItemGroup, QGraphicsItem
from PyQt5.QtGui import QPen, QTransform
from PyQt5.QtCore import QPointF, Qt
from typing import List, Optional, Union
from page import Page
from music_item import Musicitem
from fonts import get_symbol

class TimeSignature:
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
	
	def __init__(self, fundamental_beats_or_map: Union[int, dict], note_value: int = None):
		if (type(fundamental_beats_or_map) == int):
			self.fundamental_beats = fundamental_beats_or_map
			self.note_value = note_value
		else:
			self.fundamental_beats = fundamental_beats_or_map["fundamental_beats"]
			self.note_value = fundamental_beats_or_map["note_value"]

	def to_dict(self):
		return {
			"fundamental_beats": self.fundamental_beats,
			"note_value": self.note_value,
		}
	
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
	def __init__(self, pitch_or_note_map: Union[int, dict], duration: float = None):
		if (type(pitch_or_note_map) == int):
			# pitch from 1 - 88 (subcontra-a to c5)
			# pitch 0 is a rest
			self.pitch = pitch_or_note_map

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
		else:
			self.pitch = pitch_or_note_map["pitch"]
			self.duration = pitch_or_note_map["duration"]
			self.dotted = pitch_or_note_map["dotted"]
			self.accidental = pitch_or_note_map["accidental"]

	def to_dict(self):
		return {
			"pitch": self.pitch,
			"duration": self.duration,
			"dotted": self.dotted,
			"accidental": self.accidental,
		}

# notes that will appear above each other
class NoteGroup:
	def __init__(self, note_group_map: Optional[dict] = None):
		if (type(note_group_map) != dict):
			self.first_voice: List[Note] = []
			self.second_voice: List[Note] = []
		else:
			for note in note_group_map["first_voice"]:
				self.first_voice.append(Note(note))

			for note in note_group_map["second_voice"]:
				self.second_voice.append(Note(note))
	def to_dict(self):
		group_map = {
			"first_voice": [],
			"second_voice": [],
		}

		for note in self.first_voice:
			group_map["first_voice"].append(note.to_dict())
		for note in self.second_voice:
			group_map["second_voice"].append(note.to_dict())

		return group_map

class KeySignature:
	signatures_map = {
		# name defined in the vombo box : [number of accidentals, type (see Note class)]
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

	def __init__(self, key_signature: Union[str, dict]):
		if (type(key_signature) == str):
			self.number = self.signatures_map[key_signature][0]
			self.type = self.signatures_map[key_signature][1]
		else:
			self.number = key_signature["number"]
			self.type = key_signature["type"]

	def to_dict(self):
		return {
			"number": self.number,
			"type": self.type,
		}

class Bar:
	def __init__(self, time_signature_or_dict_data: Union[TimeSignature, dict]):
		if (type(time_signature_or_dict_data) == TimeSignature):
			self.time_signature = time_signature_or_dict_data
			self.note_groups = []
		else:
			self.time_signature = TimeSignature(time_signature_or_dict_data["time_signature"])
			self.note_groups = []
			for note_group in time_signature_or_dict_data["note_groups"]:
				self.note_groups.append(NoteGroup(note_group))
		self.objects: List[Musicitem] = []
	def to_dict(self):
		dict_data = {
			"time_signature": self.time_signature.to_dict(),
			"note_groups": [note_group.to_dict() for note_group in self.note_groups],
		}
		return dict_data

	#def set_up(self, start_pos: QPointF, staves: List[Stave]):
	
class Stave(QGraphicsItemGroup):
	"""This is a QGraphicsItemGroup to move all its members at once.\n
	All positions are relative to the parent from here on!"""

	line_pen = QPen(Qt.black, 3)

	# 0 = bottom line
	# 0.5 = first space from the bottom 
	# 1 = 2nd line from the bottom
	# ...
	# e.g. -1 would be c (with g clef)

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

	def __init__(self, system_group: QGraphicsItemGroup, clef_key: str, width: float, key_signature: KeySignature, first_bar: Bar):
		super().__init__()

		# setup members
		self.system_group: QGraphicsItemGroup = system_group
		self.clef_key: str = clef_key
		self.width = width
		self.key_signature: KeySignature = key_signature
		self.lines: List[QGraphicsLineItem] = []
		self.bars: List[Bar] = [first_bar]

		# draw all lines
		for i in range(5):
			# first i is 0
			# first line is the bottom line with index 0 in self.lines...
			y = Musicitem.EM - i * 0.25 * Musicitem.EM
			line = QGraphicsLineItem(0, y, self.width, y)
			line.setPen(Stave.line_pen)
			self.lines.append(line)
			self.addToGroup(line)

		# add clef
		self.clef = Musicitem(Stave.clefs[self.clef_key]["smufl_key"])
		self.addToGroup(self.clef)
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
			self.addToGroup(accidental)
			x = self.clef.pos().x() + self.clef.sceneBoundingRect().width() + i * (accidental.sceneBoundingRect().width() - 0.1 * Musicitem.EM) + 0.1 * Musicitem.EM
			y = Musicitem.EM - Musicitem.EM * 0.25 * (KeySignature.accidentals_positions[self.key_signature.type - 1][i] + Stave.clefs[clef_key]["accidental_shift"])
			accidental.setPos(x, y)
			self.key_signature_accidentals.append(accidental)

	def add_first_time_signature(self, start_x: float):
		time_signature = Musicitem(self.bars[0].time_signature.gen_unicode_combi())
		self.addToGroup(time_signature)
		time_signature.setPos(start_x + 0.25 * Musicitem.EM, Musicitem.EM)
		self.bars[0].objects.append(time_signature)

	def to_dict(self):
		dict_data = {
			"bars": [bar.to_dict() for bar in self.bars]
		}
		return dict_data

class System(QGraphicsItemGroup):
	"""This is a QGraphicsItemGroup to move it from one page (QGraphicsScene) to another.\n
	All positions are relative to the parent from here on!\n
	To add an item, first add it and then set a relative position!"""

	min_stave_spacing = Musicitem.EM
	system_spacing = Musicitem.EM * 1.5
	def __init__(self, page_index: int, voices: int, pos: QPointF, clefs_tabel: List[str], key_signature: KeySignature, with_piano: bool, first_bar: Bar, first_system: bool = False):
		super().__init__()

		# setup all members
		self.page_index = page_index
		self.setPos(pos)

		self.width = Page.WIDTH - self.x() - Page.MARGIN
		self.voices: int = voices
		self.key_signature = key_signature
		self.with_piano: bool = with_piano

		# create staves
		self.staves: List[Stave] = [
			# create all staves using list comprehension
			Stave(self, clefs_tabel[n], self.width, self.key_signature, first_bar) for n in range(voices)
		]
		for n, stave in enumerate(self.staves):
			self.addToGroup(stave)
			stave.setPos(0, n * (Musicitem.EM + System.min_stave_spacing))

		self.first_system = first_system

		# setup the left bar line
		self.left_bar_line = Musicitem("barlineSingle")
		self.left_bar_line.setTransform(QTransform().scale(1, (self.voices * Musicitem.EM + (self.voices - 1) * System.min_stave_spacing) / Musicitem.EM))
		self.addToGroup(self.left_bar_line)
		self.left_bar_line.setPos(-self.left_bar_line.sceneBoundingRect().width() / 2, (2 * self.voices - 1) * Musicitem.EM)

		# draw final barline (just to test it)
		self.right_bar_line = Musicitem("barlineFinal")
		self.right_bar_line.setTransform(QTransform().scale(1, (self.voices * Musicitem.EM + (self.voices - 1) * System.min_stave_spacing) / Musicitem.EM))
		self.addToGroup(self.right_bar_line)
		self.set_end_bar_line()

		if (self.with_piano and self.voices > 1):
			self.addbrace()

		if (self.first_system):
			for stave in self.staves:
				stave.add_first_time_signature(self.get_start_x())

	def addbrace(self):
		self.brace = Musicitem("brace")
		self.addToGroup(self.brace)

		# default brace: 1 EM
		scale = (self.staves[-1].y() - self.staves[-2].y() + Musicitem.EM) / Musicitem.EM
		self.brace.setScale(scale)
		self.brace.setPos(-self.brace.sceneBoundingRect().width(), self.staves[-1].y() + Musicitem.EM)

	def get_start_x(self):
		staves_start_x = []
		for stave in self.staves:
			if (self.key_signature.number > 0):
				staves_start_x.append(stave.key_signature_accidentals[-1].sceneBoundingRect().width() + stave.key_signature_accidentals[-1].pos().x())
			else:
				staves_start_x.append(stave.clef.sceneBoundingRect().width() + stave.clef.pos().x())
		return max(staves_start_x)

	def to_dict(self):
		dict_data = {
			"staves": [stave.to_dict() for stave in self.staves],
		}
		return dict_data

	def set_normal_end_bar_line(self):
		self.right_bar_line.setPlainText(get_symbol("barlineSingle"))
		self.right_bar_line.setPos(self.width - self.right_bar_line.sceneBoundingRect().width() / 2, (2 * self.voices - 1) * Musicitem.EM)
	
	def set_end_bar_line(self):
		self.right_bar_line.setPlainText(get_symbol("barlineFinal"))
		self.right_bar_line.setPos(self.width - self.right_bar_line.sceneBoundingRect().width() / 1.3, (2 * self.voices - 1) * Musicitem.EM)

	def get_bottom_y(self)-> float:
		return self.y() + self.staves[-1].y() + Musicitem.EM
	