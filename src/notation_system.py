from typing import List, Union

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
	def __init__(self, note_group_map: Union[dict, None] = None):
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
	def __init__(self, time_signature_or_bar_map: Union[TimeSignature, dict], key_signature: KeySignature = None):
		if (type(time_signature_or_bar_map) == TimeSignature):
			self.time_signature = time_signature_or_bar_map
			self.key_signature = key_signature
			self.note_groups = []
		else:
			self.time_signature = TimeSignature(time_signature_or_bar_map["key_signature"])
			self.key_signature = KeySignature(time_signature_or_bar_map["key_signature"])
			self.note_groups = []
			for note_group in time_signature_or_bar_map["note_groups"]:
				self.note_groups.append(NoteGroup(note_group))

	def setup(self):
		self.note_groups = [NoteGroup()]
		self.note_groups[0].first_voice.append(Note(-1, -1))

	def to_map(self):
		bar_map = {
			"key_signature": self.key_signature.to_map(),
			"time_signature": self.time_signature.to_map(),
			"note_groups": [],
		}

		for note_group in self.note_groups:
			bar_map["note_groups"].append(note_group.to_map())
		
		return bar_map