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
        self._init(item)
    
    def _init(self, item):
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

    def __getstate__(self):
        self.rect = self.qt().sceneRect()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsScene(self.rect))

class N_QGraphicsTextItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsTextItem):
        super().__init__(item)

    def qt(self) -> QGraphicsTextItem:
        return self._qt()

    def __getstate__(self):
        self.text = self.qt().toPlainText()
        self.pos = self.qt().pos()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsTextItem(self.text))
        self.qt().setPos(self.pos)

class N_QGraphicsItemGroup(N_GraphicsObject):
    def __init__(self, item: QGraphicsItemGroup):
        super().__init__(item)

    def qt(self) -> QGraphicsItemGroup:
        return self._qt()

    def __getstate__(self):
        self.pos = self.qt().pos()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsItemGroup())
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
        self._init(QGraphicsLineItem(self.line))

class N_QGraphicsRectItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsRectItem):
        super().__init__(item)

    def qt(self) -> QGraphicsRectItem:
        return self._qt()

    def __getstate__(self):
        self.rect = self.qt().rect()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsRectItem(self.rect))
