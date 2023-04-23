from PyQt5.QtCore import QPointF

from notation_system import TimeSignature, System, KeySignature
from typing import List
from page import Page, DocumentTextitem

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

		top_spacing = self.tempo.qt().y() + self.tempo.qt().sceneBoundingRect().height() + Page.MARGIN / 4
		self.systems = [System(0, self.staves, QPointF(2 * Page.MARGIN, top_spacing), self.clefs, self.key_signature, self.with_piano, time_signature, True)]
		self.pages[0].scene.qt().addItem(self.systems[-1].qt())

	def add_new_system(self) -> bool:
		page_index = len(self.pages) - 1
		last_time_sig = self.systems[-1].staves[0].bars[-1].time_signature
		self.systems[-1].set_normal_end_bar_line()
		self.systems.append(System(page_index, self.staves, QPointF(Page.MARGIN, self.systems[-1].get_bottom_y() + System.system_spacing), self.clefs, self.key_signature, self.with_piano, last_time_sig, False))
		if (self.systems[-1].get_bottom_y() > Page.HEIGHT - Page.MARGIN):
			self.systems[-1].qt().setPos(Page.MARGIN, Page.MARGIN)
			return True
		
	def delete_last_system(self):
		self.pages[-1].scene.qt().removeItem(self.systems[-1].qt())
		self.systems.pop(len(self.systems) - 1)
		self.systems[-1].set_end_bar_line()

	def reassemble(self):
		for page in self.pages:
			page.reassemble()

		self.pages[0].scene.qt().addItem(self.heading.qt())
		self.pages[0].scene.qt().addItem(self.sub_heading.qt())
		self.pages[0].scene.qt().addItem(self.composer.qt())
		self.pages[0].scene.qt().addItem(self.tempo.qt())

		for system in self.systems:
			system.reassemble()
			self.pages[system.page_index].scene.qt().addItem(system.qt())
			system.qt().setPos(system.pos)
