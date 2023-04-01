from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QMessageBox, QCheckBox, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

import app
from ui_misc import update_page_change_buttons_colors

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
        self.setTextInteractionFlags(Qt.TextEditorInteraction | Qt.NoTextInteraction)
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

def create_empty_page(new_first_page):
    new_page = QGraphicsScene(0, 0, app.width, app.height)
    # white background
    rect = QGraphicsRectItem(0, 0, app.width, app.height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)

    if (new_first_page):
        # the font sizes were roughly measured using an example
        title = DocumentTextitem("Titel", app.width * 0.6 / 21, app.margin, "center", True)
        composer = DocumentTextitem("Komponist", app.width * 0.3 / 21, title.y() + title.boundingRect().height(), "right", True)

        new_page.addItem(title)
        app.document_ui.title = title

        new_page.addItem(composer)
        app.document_ui.composer = composer
    
    return new_page

def update_page_info_and_button_text():
    app.ui.current_page_label.setText("Seite " + str(app.current_page + 1) + " von " + str(len(app.document_ui.pages)))
    update_page_change_buttons_colors()

def new_page():
    new_page = create_empty_page(False)
    if (len(app.document_ui.pages) == app.current_page + 1):
        app.document_ui.pages.append(new_page)
    else:
        app.document_ui.pages.insert(app.current_page + 1, new_page)
    app.current_page += 1
    app.ui.view.setScene(app.document_ui.pages[app.current_page])
    update_page_info_and_button_text()

def delete_page():
    if (app.show_warning_box):
        warning_box = QMessageBox(QMessageBox.Information, "Seite Löschen", f"Wollen Sie die Seite {app.current_page + 1} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        warning_box.setDefaultButton(QMessageBox.Yes)
        warning_box.button(QMessageBox.Yes).setText("Ja")
        warning_box.button(QMessageBox.No).setText("Nein")
        check_box = QCheckBox("Nicht mehr nachfragen", warning_box)
        warning_box.setCheckBox(check_box)

        result = warning_box.exec_()

        if (result == QMessageBox.No):
            return

        if (check_box.isChecked()):
            app.show_warning_box = False

    app.document_ui.pages.pop(app.current_page)
    app.current_page -= 1
    if (app.current_page < 0):
        app.current_page = 0
    if (len(app.document_ui.pages) == 0):
        app.document_ui.pages.append(create_empty_page(True))

    app.ui.view.setScene(app.document_ui.pages[app.current_page])
    update_page_info_and_button_text()

def next_page():
    if (app.current_page + 1 < len(app.document_ui.pages)):
        app.current_page += 1
        app.ui.view.setScene(app.document_ui.pages[app.current_page])
        update_page_info_and_button_text()

def previous_page():
    if (app.current_page > 0):
        app.current_page -= 1
        app.ui.view.setScene(app.document_ui.pages[app.current_page])
        update_page_info_and_button_text()