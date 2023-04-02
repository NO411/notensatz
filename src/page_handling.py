from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QMessageBox, QCheckBox, QMenu
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt,QPropertyAnimation

import app
from document_text import DocumentTextitem
from ui_misc import update_page_change_buttons_colors

def create_empty_page(new_first_page=False, heading_text="", sub_heading_text="", composer_text=""):
    new_page = QGraphicsScene(0, 0, app.width, app.height)
    # white background
    rect = QGraphicsRectItem(0, 0, app.width, app.height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)

    if (new_first_page):
        if (heading_text == ""):
            heading_text = "Titel"
        if (sub_heading_text == ""):
            sub_heading_text = "Unterüberschrift"
        if (composer_text == ""):
            composer_text = "Komponist / Arrangeur"

        # the font sizes were roughly measured using an example
        heading = DocumentTextitem(heading_text, app.width * 0.6 / 21, app.margin, "center", True)
        sub_heading = DocumentTextitem(sub_heading_text, app.width * 0.4 / 21, heading.y() + heading.boundingRect().height(), "center", False)
        composer = DocumentTextitem(composer_text, app.width * 0.3 / 21, sub_heading.y() + sub_heading.boundingRect().height(), "right", True)

        new_page.addItem(heading)
        new_page.addItem(sub_heading)
        new_page.addItem(composer)

        app.document_ui.heading = heading
        app.document_ui.sub_heading = sub_heading
        app.document_ui.composer = composer

        app.ui.action_edit_heading.triggered.connect(heading.setFocus)
        app.ui.action_edit_subheading.triggered.connect(sub_heading.setFocus)
        app.ui.action_edit_composer.triggered.connect(composer.setFocus)
    
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

def create_new_document():
    # disconnect old signals / slots:
    app.ui.action_edit_heading.triggered.disconnect(app.document_ui.heading.setFocus)
    app.ui.action_edit_subheading.triggered.disconnect(app.document_ui.sub_heading.setFocus)
    app.ui.action_edit_composer.triggered.disconnect(app.document_ui.composer.setFocus)

    # remove blur effect and enable centralwidget if still in welcome screen
    if (app.in_welcome_screen):
        app.in_welcome_screen = False
        app.ui.centralwidget.setEnabled(True)
        app.ui.centralwidget.setGraphicsEffect(None)
        app.ui.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        app.ui.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        app.ui.welcome_label.setParent(None)
        app.window.resizeEvent = None
        app.ui.welcome_button_new.setParent(None)
        app.ui.welcome_button_open.setParent(None)
        edit_menu = app.ui.menubar.findChild(QMenu, "menu_edit")
        edit_menu.setEnabled(True)
        app.ui.action_save.setEnabled(True)
        app.ui.action_save_as.setEnabled(True)
        app.ui.action_export.setEnabled(True)

    app.document_ui.pages = [create_empty_page(True, app.new_doc_dialog_ui.heading_line_edit.text(), app.new_doc_dialog_ui.sub_heading_line_edit.text(), app.new_doc_dialog_ui.composer_line_edit.text())]
    app.ui.view.setScene(app.document_ui.pages[0])
    app.new_doc_dialog.close()