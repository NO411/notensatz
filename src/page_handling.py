from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QMessageBox, QCheckBox
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

import app
from ui_misc import update_page_change_buttons_colors

def create_empty_page():
    new_page = QGraphicsScene(0, 0, app.width, app.height)
    # white background
    rect = QGraphicsRectItem(0, 0, app.width, app.height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)
    return new_page

def update_page_info_and_button_text():
    app.ui.current_page_label.setText("Seite " + str(app.current_page + 1) + " von " + str(len(app.pages)))
    update_page_change_buttons_colors()

def new_page():
    new_page = create_empty_page()
    if (len(app.pages) == app.current_page + 1):
        app.pages.append(new_page)
    else:
        app.pages.insert(app.current_page + 1, new_page)
    app.current_page += 1
    app.ui.view.setScene(app.pages[app.current_page])
    update_page_info_and_button_text()

def delete_page():
    if (app.show_warning_box):
        warning_box = QMessageBox(QMessageBox.Warning, "Seite Löschen", f"Wollen Sie die Seite {app.current_page + 1} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
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


    app.pages.pop(app.current_page)
    app.current_page -= 1
    if (app.current_page < 0):
        app.current_page = 0
    if (len(app.pages) == 0):
        app.pages.append(create_empty_page())

    app.ui.view.setScene(app.pages[app.current_page])
    update_page_info_and_button_text()

def next_page():
    if (app.current_page + 1 < len(app.pages)):
        app.current_page += 1
        app.ui.view.setScene(app.pages[app.current_page])
        update_page_info_and_button_text()

def previous_page():
    if (app.current_page > 0):
        app.current_page -= 1
        app.ui.view.setScene(app.pages[app.current_page])
        update_page_info_and_button_text()