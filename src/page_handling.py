from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QMessageBox, QCheckBox, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

import app
from ui_misc import update_page_change_buttons_colors

def align_title():
    title = app.document_ui.pages[app.document_ui.title[0]].items()[app.document_ui.title[1]]
    rec = title.boundingRect()

    # set maximum width
    while (title.boundingRect().width() > (app.width - app.width / 20)):
        title.document().blockSignals(True)
        title.setPlainText(title.toPlainText()[:-1])
        cursor = title.textCursor()
        cursor.setPosition(len(title.toPlainText()))
        title.setTextCursor(cursor)
        title.document().blockSignals(False)

    # bounding was updated...
    rec = title.boundingRect()
    title.setX(app.width / 2 - rec.width() / 2)

def create_empty_page(new_first_page):
    new_page = QGraphicsScene(0, 0, app.width, app.height)
    # white background
    rect = QGraphicsRectItem(0, 0, app.width, app.height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)

    if (new_first_page):
        title = QGraphicsTextItem("Title")
        title.setTextInteractionFlags(Qt.TextEditorInteraction)
        title.setFont(QFont("Times New Roman", app.width / 20))
        title.setDefaultTextColor(Qt.black)
        rec = title.boundingRect()
        title.setPos(app.width / 2 - rec.width() / 2, app.width / 20)
        title.document().contentsChanged.connect(align_title)
        title.document().setMaximumBlockCount(1)

        new_page.addItem(title)
        index = new_page.items().index(title)
        # [page, index]
        app.document_ui.title = [0, index]
    
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