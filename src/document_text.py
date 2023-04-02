from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsTextItem

import app

class DocumentTextitem(QGraphicsTextItem):
    def __init__(self, text: str, fontSize: float, y: float, alignment: str, bold: bool):
        """
        `alignment`: "right", "center"
        """
        super().__init__()

        # text
        self.setPlainText(text)
        font = QFont("Times New Roman", fontSize)
        font.setBold(bold)
        self.setFont(font)
        self.setDefaultTextColor(Qt.black)

        # interaction
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.document().setMaximumBlockCount(1)

        # alignment and positioning
        self.alignment = alignment
        self._y = y
        self.align()
        self.document().contentsChanged.connect(self.align)

    def crop_text(self):
        # set maximum width
        while (self.boundingRect().width() > (app.width - 2 * app.margin)):
            self.document().blockSignals(True)
            cursor = self.textCursor()
            old_cursor_pos = cursor.position()
            # remove character which was added by the user at the cursor position
            self.setPlainText(self.toPlainText()[:old_cursor_pos - 1] + self.toPlainText()[old_cursor_pos:])
            new_pos = old_cursor_pos - 1
            if (new_pos >= 0):
                cursor.setPosition(old_cursor_pos - 1)
            self.setTextCursor(cursor)
            self.document().blockSignals(False)

    def align(self):
        if (self.alignment == "right"):
            self.crop_text()
            self.setPos(app.width - app.margin - self.boundingRect().width(), self._y)
        elif (self.alignment == "center"):
            self.crop_text()
            self.setPos(app.width / 2 - self.boundingRect().width() / 2, self._y)

    def remove_highlight(self):
        # work around to remove highlighted text
        cursor = self.textCursor()
        cursor.setPosition(len(self.toPlainText()))
        self.setTextCursor(cursor)

    # !!
    # this is really important to avoid a program crash when rightklicking an QGraphicstextItem!
    def contextMenuEvent(self, event):
        event.ignore()