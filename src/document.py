from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

from notation_system import TimeSignature, System, KeySignature
from typing import List
from edit_items import Page, DocumentTextitem, Musicitem, EditScene
from settings import Settings

class DocumentUi:
	def __init__(self):
		# table of all pages (those include the scenes)
		self.pages: List[Page] = []

		self.heading: DocumentTextitem = None
		self.sub_heading: DocumentTextitem = None
		self.composer: DocumentTextitem = None
		self.tempo: DocumentTextitem = None

	def setup(self, staves: int, time_signature: TimeSignature, with_piano: bool, clefs: List[str], key_signature: KeySignature):
		# info: first page was already added by page_handling 
		self.with_piano = with_piano
		self.staves = staves
		self.clefs = clefs
		self.key_signature = key_signature

		top_spacing = self.tempo.qt().y() + self.tempo.qt().sceneBoundingRect().height() + Settings.Layout.MARGIN / 4
		self.systems = [System(0, self.staves, QPointF(2 * Settings.Layout.MARGIN, top_spacing), self.clefs, self.key_signature, self.with_piano, time_signature, True)]
		self.pages[0].qt().addItem(self.systems[-1].qt())

	def add_new_system(self) -> bool:
		page_index = len(self.pages) - 1
		last_time_sig = self.systems[-1].staves[0].bars[-1].time_signature
		self.systems[-1].set_normal_end_bar_line()
		self.systems.append(System(page_index, self.staves, QPointF(Settings.Layout.MARGIN, self.systems[-1].get_bottom_y() + System.system_spacing), self.clefs, self.key_signature, self.with_piano, last_time_sig, False))
		if (self.systems[-1].get_bottom_y() > Settings.Layout.HEIGHT - Settings.Layout.MARGIN):
			self.systems[-1].qt().setPos(Settings.Layout.MARGIN, Settings.Layout.MARGIN)
			return True
		
	def delete_last_system(self):
		self.pages[-1].qt().removeItem(self.systems[-1].qt())
		self.systems.pop(len(self.systems) - 1)
		self.systems[-1].set_end_bar_line()

	def reassemble(self):
		for page in self.pages:
			page.reassemble()

		self.pages[0].qt().addItem(self.heading.qt())
		self.pages[0].qt().addItem(self.sub_heading.qt())
		self.pages[0].qt().addItem(self.composer.qt())
		self.pages[0].qt().addItem(self.tempo.qt())

		for system in self.systems:
			system.reassemble()
			self.pages[system.page_index].qt().addItem(system.qt())
			system.qt().setPos(system.pos)

	def setup_edit(self):
		self.edit_object = Musicitem("", QColor("#528bff"))
		self.pages[0].qt().addItem(self.edit_object.qt())
