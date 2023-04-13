from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem
from PyQt5.QtGui import QPen, QTransform
from PyQt5.QtCore import QPointF, Qt
from typing import List, Optional, Union
from page import Page
from music_item import Musicitem

class TimeSignature:
	def __init__(self, fundamental_beats_or_map: Union[int, dict], note_value: int = None):
		if (type(fundamental_beats_or_map) == int):
			self.fundamental_beats = fundamental_beats_or_map
			self.note_value = note_value
		else:
			self.fundamental_beats = fundamental_beats_or_map["fundamental_beats"]
			self.note_value = fundamental_beats_or_map["note_value"]

	def to_map(self):
		return {
			"fundamental_beats": self.fundamental_beats,
			"note_value": self.note_value,
		}

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

	def to_map(self):
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
	def to_map(self):
		group_map = {
			"first_voice": [],
			"second_voice": [],
		}

		for note in self.first_voice:
			group_map["first_voice"].append(note.to_map())
		for note in self.second_voice:
			group_map["second_voice"].append(note.to_map())

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

	def to_map(self):
		return {
			"number": self.number,
			"type": self.type,
		}

class Bar:
	def __init__(self, time_signature_or_bar_map: Union[TimeSignature, dict]):
		if (type(time_signature_or_bar_map) == TimeSignature):
			self.time_signature = time_signature_or_bar_map
			self.note_groups = []
		else:
			self.time_signature = TimeSignature(time_signature_or_bar_map["time_signature"])
			self.note_groups = []
			for note_group in time_signature_or_bar_map["note_groups"]:
				self.note_groups.append(NoteGroup(note_group))
		self.objects: List[Musicitem] = []
	def to_map(self):
		bar_map = {
			"time_signature": self.time_signature.to_map(),
			"note_groups": [],
		}

		for note_group in self.note_groups:
			bar_map["note_groups"].append(note_group.to_map())

		return bar_map

	#def set_up(self, start_pos: QPointF, staves: List[Stave]):
	
class Stave:
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

	def __init__(self, drawing_scene: QGraphicsScene, clef_key: str, left_pos: QPointF, width: float, key_signature: KeySignature, first_bar: Bar):
		# setup members
		self.drawing_scene: QGraphicsScene = drawing_scene
		self.clef_key: str = clef_key
		self.left_pos: QPointF = left_pos
		self.width = width
		self.key_signature: KeySignature = key_signature
		self.lines: List[QGraphicsLineItem] = []
		self.bars: List[Bar] = [first_bar]

		# draw all lines
		for i in range(5):
			# first i is 0
			# first line is the bottom line with index 0 in self.lines...
			y = self.left_pos.y() + Musicitem.EM - i * 0.25 * Musicitem.EM
			line = QGraphicsLineItem(self.left_pos.x(), y, self.left_pos.x() + self.width, y)
			line.setPen(Stave.line_pen)
			self.lines.append(line)
			self.drawing_scene.addItem(line)

		# add clef
		self.clef = Musicitem(Stave.clefs[self.clef_key]["smufl_key"])
		self.clef.setPos(self.left_pos.x() + 0.05 * Musicitem.EM, self.left_pos.y() + Musicitem.EM - Musicitem.EM * 0.25 * Stave.clefs[self.clef_key]["line"])
		self.drawing_scene.addItem(self.clef)

		self.key_signature_accidentals: List[Musicitem] = []
		# add key signature
		for i in range(self.key_signature.number):
			# b
			smufl_name = "accidentalSharp"
			if (self.key_signature.type == 2):
				# #
				smufl_name = "accidentalFlat"
			accidental = Musicitem(smufl_name)
			x = self.clef.pos().x() + self.clef.sceneBoundingRect().width() + i * (accidental.sceneBoundingRect().width() - 0.1 * Musicitem.EM) + 0.1 * Musicitem.EM
			y = self.left_pos.y() + Musicitem.EM - Musicitem.EM * 0.25 * (KeySignature.accidentals_positions[self.key_signature.type - 1][i] + Stave.clefs[clef_key]["accidental_shift"])
			accidental.setPos(x, y)
			self.key_signature_accidentals.append(accidental)
			self.drawing_scene.addItem(accidental)

	def add_first_time_signature(self, start_x: float):
		time_signature = Musicitem(["timeSigCombNumerator", "timeSig" + str(self.bars[0].time_signature.fundamental_beats), "timeSigCombDenominator", "timeSig" + str(self.bars[0].time_signature.note_value)])
		time_signature.setPos(start_x + 0.25 * Musicitem.EM, self.left_pos.y() + Musicitem.EM)
		self.bars[0].objects.append(time_signature)
		self.drawing_scene.addItem(time_signature)

class System:
	min_stave_spacing = Musicitem.EM
	def __init__(self, drawing_scene: QGraphicsScene, voices: int, clefs_tabel: List[str], key_signature: KeySignature, with_piano: bool, first_bar: Bar, position: QPointF, first_system: bool = False):
		# setup all members
		self.drawing_scene: QGraphicsScene = drawing_scene
		self.pos: QPointF = position
		self.width = Page.WIDTH - self.pos.x() - Page.MARGIN
		self.voices: int = voices
		self.key_signature = key_signature
		self.with_piano: bool = with_piano
		self.staves: List[Stave] = [
			# create all staves using list comprehension
			Stave(drawing_scene, clefs_tabel[n], QPointF(self.pos.x(), self.pos.y() + n * (Musicitem.EM + System.min_stave_spacing)), self.width, self.key_signature, first_bar) for n in range(voices)
		]
		self.first_system = first_system

		# setup the left bar line
		self.left_bar_line = Musicitem("barlineSingle")
		self.left_bar_line.setTransform(QTransform().scale(1, (self.voices * Musicitem.EM + (self.voices - 1) * System.min_stave_spacing) / Musicitem.EM))
		self.left_bar_line.setPos(self.pos.x() - self.left_bar_line.sceneBoundingRect().width() / 2, self.pos.y() + (2 * self.voices - 1) * Musicitem.EM)
		self.drawing_scene.addItem(self.left_bar_line)

		# draw final barline (just to test it)
		self.right_bar_line = Musicitem("barlineFinal")
		self.right_bar_line.setTransform(QTransform().scale(1, (self.voices * Musicitem.EM + (self.voices - 1) * System.min_stave_spacing) / Musicitem.EM))
		self.right_bar_line.setPos(self.pos.x() + self.width - self.right_bar_line.sceneBoundingRect().width() / 1.3, self.pos.y() + (2 * self.voices - 1) * Musicitem.EM)
		self.drawing_scene.addItem(self.right_bar_line)

		if (self.with_piano and self.voices > 1):
			self.addbrace()

		if (self.first_system):
			for stave in self.staves:
				stave.add_first_time_signature(self.get_start_x())

	def addbrace(self):
		self.brace = Musicitem("brace")

		# default brace: 1 EM
		scale = (self.staves[-1].left_pos.y() - self.staves[-2].left_pos.y() + Musicitem.EM) / Musicitem.EM
		self.brace.setScale(scale)
		self.brace.setPos(self.pos.x() - self.brace.sceneBoundingRect().width(),self.staves[-1].left_pos.y() + Musicitem.EM)
		self.drawing_scene.addItem(self.brace)

	def get_start_x(self):
		staves_start_x = []
		for stave in self.staves:
			if (self.key_signature.number > 0):
				staves_start_x.append(stave.key_signature_accidentals[-1].sceneBoundingRect().width() + stave.key_signature_accidentals[-1].pos().x())
			else:
				staves_start_x.append(stave.clef.sceneBoundingRect().width() + stave.clef.pos().x())
		return max(staves_start_x)