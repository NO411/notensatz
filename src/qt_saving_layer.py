from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem

class ItemContainer():
    def __init__(self):
        self.container = {}
        self.min_key = 0

    def append(self, item) -> int:
        """This function adds the item to the dictionary and returns the key."""
        # this way, no keys will double
        self.min_key += 1
        self.container[self.min_key] = item
        return self.min_key

    def __getitem__(self, key):
        return self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value

items = ItemContainer()

class N_GraphicsObject():
    def __init__(self, item):
        global items
        self.key = items.append(item)

    def _qt(self):
        global items
        return items[self.key]

class N_QGraphicsScene(N_GraphicsObject):
    def __init__(self, item: QGraphicsScene):
        super().__init__(item)

    def qt(self) -> QGraphicsScene:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.rect = self.qt().sceneRect()
        # ... all important members

    def restore_from_pickle(self):
        self.__init__(QGraphicsScene(self.rect))

class N_QGraphicsTextItem():
    def __init__(self, item: QGraphicsTextItem):
        super().__init__(item)

    def qt(self) -> QGraphicsTextItem:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.text = self.qt().toPlainText()

class N_QGraphicsItemGroup():
    def __init__(self, item: QGraphicsItemGroup):
        super().__init__(item)

    def qt(self) -> QGraphicsItemGroup:
        return self._qt()
    
    def prepare_for_pickle(self):
        pass

class N_QGraphicsLineItem():
    def __init__(self, item: QGraphicsLineItem):
        super().__init__(item)

    def qt(self) -> QGraphicsLineItem:
        return self._qt()
    
    def prepare_for_pickle(self):
        pass

class N_QGraphicsRectItem():
    def __init__(self, item: QGraphicsRectItem):
        super().__init__(item)

    def qt(self) -> QGraphicsRectItem:
        return self._qt()
    
    def prepare_for_pickle(self):
        pass
