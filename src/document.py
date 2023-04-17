from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMessageBox, QCheckBox

from notation_system import Bar, System, KeySignature
from typing import List
from page import Page, DocumentTextitem

class DocumentUi:
	def __init__(self):
		# table of all pages (those include the scenes)
		self.pages: List[Page] = []

		# references of the objects stored in the scene to be able to access them
		# because it is not always possible to determine the index of the item in the pages[x].items() list
		self.heading: DocumentTextitem = None
		self.sub_heading: DocumentTextitem = None
		self.composer: DocumentTextitem = None
		self.tempo: DocumentTextitem = None

	def setup(self, staves: int, first_bar: Bar, with_piano: bool, clefs: List[str], key_signature: KeySignature):
		# info: first page was already added by page_handling 
		self.with_piano = with_piano
		self.staves = staves
		self.clefs = clefs
		self.key_signature = key_signature

		top_spacing = self.tempo.y() + self.tempo.sceneBoundingRect().height() + Page.MARGIN / 4
		self.systems = [System(0, self.staves, QPointF(2 * Page.MARGIN, top_spacing), self.clefs, self.key_signature, self.with_piano, first_bar, True)]
		self.pages[0].scene.addItem(self.systems[-1])

	def setup_by_dict(self, dict_data: dict):
		self.with_piano = dict_data["with_piano"]
		self.staves = dict_data["staves"]
		self.clefs = dict_data["clefs"]
		self.key_signature = dict_data["key_signature"]

		#for x, system_dict in enumerate(dict_data["systems"]):
		#	topy = system_dict["y"]
		#	self.systems.append(System(0, self.staves, QPointF(2 * Page.MARGIN, top_spacing), self.clefs, self.key_signature, self.with_piano, first_bar, True))

	def to_dict(self):
		dict_data = {
			"heading": self.heading.toPlainText(),
			"sub_heading": self.sub_heading.toPlainText(),
			"composer": self.composer.toPlainText(),
			"tempo": self.tempo.toPlainText(),
			"with_piano": self.with_piano,
			"staves": self.staves,
			"clefs": self.clefs,
			"key_signature": self.key_signature.to_dict(),
			"systems": [system.to_dict() for system in self.systems],
		}
		return dict_data

	def add_new_system(self) -> bool:
		page_index = len(self.pages) - 1
		last_time_sig = self.systems[-1].staves[0].bars[-1].time_signature
		self.systems[-1].set_normal_end_bar_line()
		self.systems.append(System(page_index, self.staves, QPointF(Page.MARGIN, self.systems[-1].get_bottom_y() + System.system_spacing), self.clefs, self.key_signature, self.with_piano, Bar(last_time_sig), False))
		if (self.systems[-1].get_bottom_y() > Page.HEIGHT - Page.MARGIN):
			self.systems[-1].setPos(Page.MARGIN, Page.MARGIN)
			return True
		
	def delete_last_system(self):
		self.pages[-1].scene.removeItem(self.systems[-1])
		self.systems.pop(len(self.systems) - 1)
		self.systems[-1].set_end_bar_line()