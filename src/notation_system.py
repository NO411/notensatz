from typing import List

class TimeSignature:
	def __init__(self, fundamental_beats, note_value):
		self.fundamental_beats = fundamental_beats
		self.note_value = note_value

class Note:
	def __init__(self, pitch: int, duration: float):
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
		self.second_voice: List[Note] = []


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
	def __init__(self, key_signature_string):
		self.number = self.signatures_map[key_signature_string][0]
		self.type = self.signatures_map[key_signature_string][1]

class Bar:
	def __init__(self, time_signature: TimeSignature, key_signature: KeySignature):
		self.time_signature = time_signature
		self.key_signature = key_signature
		self.note_groups = []

	def setup(self):
		self.note_groups = [NoteGroup()]
		self.note_groups[0].first_voice.append(Note(-1, -1))