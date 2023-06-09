from PyQt5.QtCore import QPointF, QLineF

from notation_system import TimeSignature, System, KeySignature
from typing import List
from edit_items import Page, DocumentTextitem
from settings import Settings

from copy import deepcopy


class DocumentUi:
    """
    members which should be saved in file: obj.member\n
    members like editing objects, which should not be saved in file: obj.qt().member
    """

    def __init__(self):
        # table of all pages (those include the scenes)
        self.pages: List[Page] = []

        self.heading: DocumentTextitem = None
        self.sub_heading: DocumentTextitem = None
        self.composer: DocumentTextitem = None
        self.tempo: DocumentTextitem = None

    def setup(self, staves: int, time_signature_name: str, with_piano: bool, clefs: List[str],
              key_signature: KeySignature):
        # info: first page was already added by page_handling
        self.with_piano = with_piano
        self.staves = staves
        self.clefs = clefs
        self.key_signature = key_signature

        time_signature = TimeSignature(time_signature_name)
        n = 0
        for key, _ in TimeSignature.signatures_map.items():
            if (time_signature_name == key):
                time_signature.symbol = n
                break
            n += 1

        top_spacing = self.tempo.qt().y() + self.tempo.qt().sceneBoundingRect().height() + Settings.Layout.MARGIN / 4
        self.systems = [
            System(0, self.staves, QPointF(2 * Settings.Layout.MARGIN, top_spacing), self.clefs, self.key_signature,
                   self.with_piano, time_signature, True)]
        self.pages[0].qt().addItem(self.systems[-1].qt())

    def add_new_system(self) -> bool:
        page_index = len(self.pages) - 1
        last_time_sig = deepcopy(self.systems[-1].staves[0].bars[-1].time_signature)
        self.systems[-1].set_normal_end_bar_line()
        self.systems.append(System(page_index, self.staves, QPointF(Settings.Layout.MARGIN, self.systems[
            -1].get_bottom_y() + System.system_spacing), self.clefs, self.key_signature, self.with_piano, last_time_sig,
                                   False))
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
            system.qt().setPos(system._pos)

    def get_closest_system(self, mouse_pos: QPointF, current_page: int) -> System:
        system_distances = []
        systems: List[System] = []
        for system in self.systems:
            if (system.page_index == current_page):
                system_distances.append(QLineF(QPointF(0, system.get_center().y()), mouse_pos).length())
                systems.append(system)

        return systems[system_distances.index(min(system_distances))]
