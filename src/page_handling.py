from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QMessageBox, QCheckBox, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt

import app
from document_text import DocumentTextitem
from ui_misc import update_page_change_buttons_colors

def create_empty_page(new_first_page):
    new_page = QGraphicsScene(0, 0, app.width, app.height)
    # white background
    rect = QGraphicsRectItem(0, 0, app.width, app.height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)

    if (new_first_page):
        # the font sizes were roughly measured using an example
        heading = DocumentTextitem("Partitur", app.width * 0.6 / 21, app.margin, "center", True)
        subheading = DocumentTextitem("Unterüberschrift", app.width * 0.4 / 21, heading.y() + heading.boundingRect().height(), "center", False)
        composer = DocumentTextitem("Komponist / Arrangeur", app.width * 0.3 / 21, subheading.y() + subheading.boundingRect().height(), "right", True)

        new_page.addItem(heading)
        app.document_ui.heading = heading

        new_page.addItem(subheading)
        app.document_ui.subheading = subheading

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