from PyQt5.QtCore import QPointF

from notation_system import Bar, System, KeySignature
from typing import List
from page import Page, DocumentTextitem
from qt_saving_layer import ItemContainer

text_items = ItemContainer()

class DocumentUi:
	def __init__(self):
		# table of all pages (those include the scenes)
		self.pages: List[Page] = []

		self.heading = None
		self.sub_heading = None
		self.composer = None
		self.tempo = None

	def setup(self, staves: int, first_bar: Bar, with_piano: bool, clefs: List[str], key_signature: KeySignature):
		# info: first page was already added by page_handling 
		self.with_piano = with_piano
		self.staves = staves
		self.clefs = clefs
		self.key_signature = key_signature

		top_spacing = self.get_tempo().y() + self.get_tempo().sceneBoundingRect().height() + Page.MARGIN / 4
		self.systems = [System(0, self.staves, QPointF(2 * Page.MARGIN, top_spacing), self.clefs, self.key_signature, self.with_piano, first_bar, True)]
		self.pages[0].scene.addItem(self.systems[-1])

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

	def get_heading(self) -> DocumentTextitem:
		global text_items
		return text_items[self.heading]

	def set_heading(self, heading: DocumentTextitem):
		global text_items
		self.heading = text_items.append(heading)
		
	def get_sub_heading(self) -> DocumentTextitem:
		global text_items
		return text_items[self.sub_heading]

	def set_sub_heading(self, sub_heading: DocumentTextitem):
		global text_items
		self.sub_heading = text_items.append(sub_heading)

	def get_composer(self) -> DocumentTextitem:
		global text_items
		return text_items[self.composer]

	def set_composer(self, composer: DocumentTextitem):
		global text_items
		self.composer = text_items.append(composer)
	
	def get_tempo(self) -> DocumentTextitem:
		global text_items
		return text_items[self.tempo]

	def set_tempo(self, tempo: DocumentTextitem):
		global text_items
		self.tempo = text_items.append(tempo)

	def prepare_for_pickle():
		# save texts from DocumentTextitems as variables
		# also call the prepare function on the pages
		pass
	
	def restore_from_pickle():
		# create DocumentTextitems from the texts in the unpickled object
		pass
