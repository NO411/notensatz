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
        """Returns the real QGraphicsItem."""
        global items
        return items[self.key]

class N_QGraphicsScene(N_GraphicsObject):
    def __init__(self, item: QGraphicsScene):
        super().__init__(item)

    def qt(self) -> QGraphicsScene:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.rect = self.qt().sceneRect()

    def restore_from_pickle(self):
        self.__init__(QGraphicsScene(self.rect))

    def __getstate__(self):
        self.line = self.qt().line()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self.__init__(QGraphicsLineItem(self.line))

class N_QGraphicsTextItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsTextItem):
        super().__init__(item)

    def qt(self) -> QGraphicsTextItem:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.text = self.qt().toPlainText()
        self.pos = self.qt().pos()

    def restore_from_pickle(self):
        self.__init__(QGraphicsTextItem(self.text))
        self.qt().setPos(self.pos)

class N_QGraphicsItemGroup(N_GraphicsObject):
    def __init__(self, item: QGraphicsItemGroup):
        super().__init__(item)

    def qt(self) -> QGraphicsItemGroup:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.pos = self.qt().pos()

    def restore_from_pickle(self):
        self.__init__(QGraphicsItemGroup())
        self.qt().setPos(self.pos)

class N_QGraphicsLineItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsLineItem):
        super().__init__(item)

    def qt(self) -> QGraphicsLineItem:
        return self._qt()
    
    def __getstate__(self):
        self.line = self.qt().line()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self.__init__(QGraphicsLineItem(self.line))

class N_QGraphicsRectItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsRectItem):
        super().__init__(item)

    def qt(self) -> QGraphicsRectItem:
        return self._qt()
    
    def prepare_for_pickle(self):
        self.rect = self.qt().rect()

    def restore_from_pickle(self):
        self.__init__(QGraphicsRectItem(self.rect))
