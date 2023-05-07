from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsRectItem
from PyQt5.QtGui import QFont, QPen
from PyQt5.QtCore import Qt

class ItemContainer():
    def __init__(self):
        self._container = {}
        self._min_key = 0

    def append(self, item) -> int:
        """This function adds the item to the dictionary and returns the key."""
        # this way, no keys will double
        self._min_key += 1
        self._container[self._min_key] = item
        return self._min_key

    def __getitem__(self, key):
        return self._container[key]

    def __setitem__(self, key, value):
        self._container[key] = value

# stores all QGraphics objects which are not pickleable
items = ItemContainer()

class N_GraphicsObject():
    def __init__(self, item):
        self._init(item)
    
    def _init(self, item):
        global items
        self._key = items.append(item)

    def _qt(self):
        """Returns the real QGraphicsItem."""
        global items
        return items[self._key]

class N_QGraphicsScene(N_GraphicsObject):
    def __init__(self, item: QGraphicsScene):
        super().__init__(item)

    def qt(self) -> QGraphicsScene:
        return self._qt()

    def __getstate__(self):
        self._rect = self.qt().sceneRect()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsScene(self._rect))

class Fixed_QGraphicsTextItem(QGraphicsTextItem):
	# this is really important to avoid a program crash when rightklicking an QGraphicstextItem!
	def contextMenuEvent(self, event):
		event.ignore()

class N_QGraphicsTextItem(N_GraphicsObject):
    def __init__(self, item: Fixed_QGraphicsTextItem):
        super().__init__(item)

    def qt(self) -> Fixed_QGraphicsTextItem:
        return self._qt()

    def __getstate__(self):
        self._text = self.qt().toPlainText()
        self._pos = self.qt().pos()
        self._font = self.qt().font().toString()
        self._color = self.qt().defaultTextColor()
        self._max_block_count = self.qt().document().maximumBlockCount()
        self._interaction = bool(self.qt().textInteractionFlags() & Qt.TextEditorInteraction)
        self._transform = self.qt().transform()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(Fixed_QGraphicsTextItem(self._text))
        self.qt().setPos(self._pos)
        font = QFont()
        font.fromString(self._font)
        self.qt().setFont(font)
        self.qt().setDefaultTextColor(self._color)
        self.qt().document().setMaximumBlockCount(self._max_block_count)
        if (self._interaction):
            self.qt().setTextInteractionFlags(Qt.TextEditorInteraction)
        self.qt().setTransform(self._transform)

class N_QGraphicsItemGroup(N_GraphicsObject):
    def __init__(self, item: QGraphicsItemGroup):
        super().__init__(item)

    def qt(self) -> QGraphicsItemGroup:
        return self._qt()

    def __getstate__(self):
        self._pos = self.qt().pos()
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
        self._line = self.qt().line()
        self._color = self.qt().pen().color()
        self._width = self.qt().pen().width()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsLineItem(self._line))
        self.qt().setPen(QPen(self._color, self._width))

class N_QGraphicsRectItem(N_GraphicsObject):
    def __init__(self, item: QGraphicsRectItem):
        super().__init__(item)

    def qt(self) -> QGraphicsRectItem:
        return self._qt()

    def __getstate__(self):
        self._rect = self.qt().rect()
        self._brush_color = self.qt().brush().color()
        self._pen_color = self.qt().pen().color()
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d
        self._init(QGraphicsRectItem(self._rect))
        self.qt().setBrush(self._brush_color)
        self.qt().setPen(self._pen_color)

