from PyQt5.QtWidgets import QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from typing import List, Union

from notation_system import TimeSignature
from fonts import get_symbol, get_icon

class SymbolButton(QPushButton):
	# symbols that will be implemented
	# map of the symbols shown on the buttons in the symbols box
	SYMBOLS = {
		# notes
		"Noten": {
			"font": "Bravura",
			"buttons": [# [unicode key, tooltip text]
				# this key can also be a list
				["noteWhole", "ganze Note"],
				["noteHalfUp", "halbe Note"],
				["noteQuarterUp", "viertel Note"],
				["note8thUp", "achtel Note"],
				["note16thUp", "sechszehntel Note"],
				["note32ndUp", "zweiunddreißigstel Note"],
				["note64thUp", "vierundsechszigstel Note"],
				["metAugmentationDot", "Punktierung"],
			]
		},
		# articulation
		"Artikulation": {
			"font": "Bravura",
			"buttons": [
				["articAccentAbove", "Akzent"],
				["articStaccatoAbove", "Staccato"],
				["articTenutoAbove", "Tenuto"],
				["keyboardPedalPed", "Pedal"],
				["keyboardPedalUp", "Pedal loslassen"],
			],
		},
		# dynamics
		"Dynamik": {
			"font": "Bravura",
			"buttons": [
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
		},
		# rests
		"Pausen": {
			"font": "Bravura",
			"buttons": [
				["restWholeLegerLine", "ganze Pause"],
				["restHalfLegerLine", "halbe pause"],
				["restQuarter", "viertel Pause"],
				["rest8th", "achtel Pause"],
				["rest16th", "sechszehntel Pause"],
				["rest32nd", "zweiunddreißigstel Pause"],
				["rest64th", "vierundsechszigstel Pause"],
				["metAugmentationDot", "Punktierung"],
			],
		},
		# accidentals
		"Vorzeichen": {
			"font": "Bravura",
			"buttons": [
				["accidentalSharp", "Kreuz"],
				["accidentalFlat", "b"],
				["accidentalDoubleSharp", "Doppelkreuz"],
				["accidentalNatural", "Auflösung"],
				["accidentalDoubleFlat", "doppel b"],
			],
		},
		# time signatures
		"Taktarten": {
			"font": "Bravura",
			"buttons": [
				[TimeSignature(time_sig_table[0], time_sig_table[1]).gen_unicode_combi(), description]
				for description, time_sig_table in TimeSignature.signatures_map.items()
			],
		},
		"N-Tolen": {
			"font": "Bravura",
			"buttons": [],
		},
		# misc
		"Sonstige": {
			"font": "Bravura",
			"buttons": [
				["repeatDots", "Wiederholung"],
				["barlineSingle", "Taktstrich"],
				["gClefChange", "Violinchlüssel (Wechsel)"],
				["fClefChange", "Bassschlüssel (Wechsel)"],
				["cClefChange", "C-Schlüssel (Wechsel)"],
			],
		},
		"Werkzeuge": {
			"font": "Awesome",
			"buttons": [
				["trash-can", "Symbol löschen"],
				["arrows-up-down-left-right", "Symbol bewegen"]
			]
		}
	}
	def __init__(self, parent: QWidget, group_key: Union[str, List[str]], n_symbol: int):
		super().__init__(parent)

		self.group_key = group_key
		self.n_symbol = n_symbol

		symbol = SymbolButton.SYMBOLS[group_key]["buttons"][n_symbol]

		self.setFixedSize(35, 60)
		self.setFlat(True)
		self.setCheckable(True)
		self.setToolTip(symbol[1])
		self.setStyleSheet("QToolTip {color: black}")

		font = SymbolButton.SYMBOLS[group_key]["font"]
		label = QLabel(self)

		if (font == "Bravura"):
			label.setText(get_symbol(symbol[0]))
			label.setFont(QFont("Bravura", 20))
			label.setGeometry(0, -20, self.width(), 100)
		elif (font == "Awesome"):
			label.setText(get_icon(symbol[0]))
			label.setFont(QFont("Font Awesome 6 Free Solid", 20))
			label.setGeometry(0, 20, self.width(), 100)

		label.setAlignment(Qt.AlignHCenter)