from PyQt5.QtCore import QPointF

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

		self.with_piano: bool = None

	def setup(self, staves: int, first_bar: Bar, with_piano: bool, clefs: List[str], key_signature: KeySignature):
		# info: first page was already added by page_handling 
		self.with_piano = with_piano
		self.staves = staves
		self.clefs = clefs
		self.key_signature = key_signature

		top_spacing = self.tempo.y() + self.tempo.sceneBoundingRect().height() + Page.MARGIN / 5
		self.systems = [System(self.pages[0].scene, self.staves, self.clefs, self.key_signature, self.with_piano, first_bar, QPointF(2 * Page.MARGIN, top_spacing), True)]