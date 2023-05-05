from PyQt5.QtWidgets import QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from typing import List, Union

from notation_system import TimeSignature
from fonts import get_symbol

class SymbolButton(QPushButton):
	# symbols that will be implemented
	# map of the symbols shown on the buttons in the symbols box
	SYMBOLS = {
		# notes
		"Noten": [# [unicode key, tooltip text]
			# this key can also be a list
			["noteWhole", "ganze Note"],
			["noteHalfUp", "halbe Note"],
			["noteQuarterUp", "viertel Note"],
			["note8thUp", "achtel Note"],
			["note16thUp", "sechszehntel Note"],
			["note32ndUp", "zweiunddreißigstel Note"],
			["note64thUp", "vierundsechszigstel Note"],
			["metAugmentationDot", "Punktierung"],
		],
		# articulation
		"Artikulation": [
			["articAccentAbove", "Akzent"],
			["articStaccatoAbove", "Staccato"],
			["articTenutoAbove", "Tenuto"],
			["keyboardPedalPed", "Pedal"],
			["keyboardPedalUp", "Pedal loslassen"],
		],
		# dynamics
		"Dynamik": [
			["dynamicMP", "mezzopiano"],
			["dynamicPiano", "piano"],
			["dynamicPP", "pianissimo"],
			["dynamicPPP", "pianopianissimo"],
			["dynamicPF", "pianoforte"],
			["dynamicFortePiano", "fortepiano"],
			["dynamicMF", "mezzoforte"],
			["dynamicForte", "forte"],
			["dynamicFF", "fortissimo"],
			["dynamicFFF", "fortefortissimo"],
			["dynamicCrescendoHairpin", "crescendo"],
			["dynamicDiminuendoHairpin", "decrescendo"],
		],
		# rests
		"Pausen": [
			["restWholeLegerLine", "ganze Pause"],
			["restHalfLegerLine", "halbe pause"],
			["restQuarter", "viertel Pause"],
			["rest8th", "achtel Pause"],
			["rest16th", "sechszehntel Pause"],
			["rest32nd", "zweiunddreißigstel Pause"],
			["rest64th", "vierundsechszigstel Pause"],
			["metAugmentationDot", "Punktierung"],
		],
		# accidentals
		"Vorzeichen": [
			["accidentalSharp", "Kreuz"],
			["accidentalFlat", "b"],
			["accidentalDoubleSharp", "Doppelkreuz"],
			["accidentalNatural", "Auflösung"],
			["accidentalDoubleFlat", "doppel b"],
		],
		# time signatures
		"Taktarten": [
			[TimeSignature(time_sig_table[0], time_sig_table[1]).gen_unicode_combi(), description]
			for description, time_sig_table in TimeSignature.signatures_map.items()
		],
		"N-Tolen": [],
		# misc
		"Sonstige": [
			["repeatDots", "Wiederholung"],
			["barlineSingle", "Taktstrich"],
			["gClefChange", "Violinchlüssel (Wechsel)"],
			["fClefChange", "Bassschlüssel (Wechsel)"],
			["cClefChange", "C-Schlüssel (Wechsel)"],
		],
	}
	def __init__(self, parent: QWidget, group_key: Union[str, List[str]], n_symbol: int):
		super().__init__(parent)

		self.group_key = group_key
		self.n_symbol = n_symbol

		symbol = SymbolButton.SYMBOLS[group_key][n_symbol]

		description = ""
		if (type(group_key) == str):
			description = group_key
		else:
			description = TimeSignature.join_unicode_combi(group_key)

		self.setObjectName(description + "Button")
		self.setFixedSize(35, 60)
		self.setFlat(True)
		self.setCheckable(True)
		self.setToolTip(symbol[1])
		self.setStyleSheet("QToolTip {color: black}")
		label = QLabel(get_symbol(symbol[0]), self)
		font = QFont("Bravura", 20)
		label.setFont(font)
		label.setAlignment(Qt.AlignHCenter)
		label.setGeometry(0, -20, self.width(), 100)