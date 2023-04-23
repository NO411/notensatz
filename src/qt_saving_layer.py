from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem
from PyQt5.QtGui import QFont, QPen
from PyQt5.QtCore import Qt

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
        self.font = self.qt().font().toString()
        self.color = self.qt().defaultTextColor()
        self.max_block_count = self.qt().document().maximumBlockCount()
        self.interaction = bool(self.qt().textInteractionFlags() & Qt.TextEditorInteraction)
        self.transform = self.qt().transform()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsTextItem(self.text))
        self.qt().setPos(self.pos)
        font = QFont()
        font.fromString(self.font)
        self.qt().setFont(font)
        self.qt().setDefaultTextColor(self.color)
        self.qt().document().setMaximumBlockCount(self.max_block_count)
        if (self.interaction):
            self.qt().setTextInteractionFlags(Qt.TextEditorInteraction)
        self.qt().setTransform(self.transform)

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

class N_QGraphicsLineItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsLineItem):
        super().__init__(item)

    def qt(self) -> QGraphicsLineItem:
        return self._qt()
    
    def __getstate__(self):
        self.line = self.qt().line()
        self.color = self.qt().pen().color()
        self.width = self.qt().pen().width()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsLineItem(self.line))
        self.qt().setPen(QPen(self.color, self.width))

class N_QGraphicsRectItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsRectItem):
        super().__init__(item)

    def qt(self) -> QGraphicsRectItem:
        return self._qt()

    def __getstate__(self):
        self.rect = self.qt().rect()
        self.brush_color = self.qt().brush().color()
        self.pen_color = self.qt().pen().color()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsRectItem(self.rect))
        self.qt().setBrush(self.brush_color)
        self.qt().setPen(self.pen_color)

