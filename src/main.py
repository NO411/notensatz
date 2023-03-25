"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

# pyqt5 imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# window / dialog imports
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog

# other imports
# from <https://pypi.org/project/pyqtdarktheme/>
import qdarktheme


"""
LOAD FONT IMAGES VIA THE METADATA JSON FILE!!!!
"""

__author__ = "Noah Weiler"

def apply_zoom():
    new_zoom = ui.zoom_slider.value() / 100
    ui.view.resetTransform()
    ui.view.scale(new_zoom, new_zoom)
    ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")
    update_zoom_buttons_colors()

def zoom_in():
    ui.zoom_slider.setValue(ui.zoom_slider.value() + 1)
    apply_zoom()

def zoom_out():
    ui.zoom_slider.setValue(ui.zoom_slider.value() - 1)
    apply_zoom()

def create_empty_page():
    new_page = QGraphicsScene(0, 0, width, height)
    # white background
    rect = QGraphicsRectItem(0, 0, width, height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)
    return new_page

def update_page_info_and_button_text():
    ui.current_page_label.setText("Seite " + str(current_page + 1) + " von " + str(len(pages)))
    update_page_change_buttons_colors()

def new_page():
    global current_page
    new_page = create_empty_page()
    if (len(pages) == current_page + 1):
        pages.append(new_page)
    else:
        pages.insert(current_page + 1, new_page)
    current_page += 1
    ui.view.setScene(pages[current_page])
    update_page_info_and_button_text()

def delete_page():
    global current_page
    
    warning_box = QMessageBox(QMessageBox.Warning, "Seite Löschen", f"Wollen Sie die Seite {current_page + 1} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
    warning_box.setDefaultButton(QMessageBox.Yes)
    warning_box.button(QMessageBox.Yes).setText("Ja")
    warning_box.button(QMessageBox.No).setText("Nein")
    warning_box.setCheckBox(QCheckBox("Nicht mehr nachfragen", warning_box))

    result = warning_box.exec_()

    if (result == QMessageBox.No):
        return

    pages.pop(current_page)
    current_page -= 1
    if (current_page < 0):
        current_page = 0
    if (len(pages) == 0):
        pages.append(create_empty_page())

    ui.view.setScene(pages[current_page])
    update_page_info_and_button_text()
    
def next_page():
    global current_page
    if (current_page + 1 < len(pages)):
        current_page += 1
        ui.view.setScene(pages[current_page])
        update_page_info_and_button_text()

def previous_page():
    global current_page
    if (current_page > 0):
        current_page -= 1
        ui.view.setScene(pages[current_page])
        update_page_info_and_button_text()

def update_page_change_buttons_colors():
    if (current_page == 0):
        ui.previous_page_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.previous_page_button.setEnabled(False)
    else:
        ui.previous_page_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.previous_page_button.setEnabled(True)
    if (current_page + 1 == len(pages)):
        ui.next_page_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.next_page_button.setEnabled(False)
    else:
        ui.next_page_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.next_page_button.setEnabled(True)

def update_zoom_buttons_colors():
    current_zoom = ui.zoom_slider.value()
    if (current_zoom == ui.zoom_slider.minimum()):
        ui.zoom_out_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.zoom_out_button.setEnabled(False)
    else:
        ui.zoom_out_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.zoom_out_button.setEnabled(True)
    if (current_zoom == ui.zoom_slider.maximum()):
        ui.zoom_in_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.zoom_in_button.setEnabled(False)
    else:
        ui.zoom_in_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.zoom_in_button.setEnabled(True)

qdarktheme.enable_hi_dpi()
app = QApplication([])

# apply the dark theme to the app
# see <https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html>
primary_color = "#528bff"
qdarktheme.setup_theme(
    custom_colors = {
        "primary": primary_color,
        "background": "#21252b",
        "border": "#474a4f",
        "foreground": "#d7d7d5",
        "scrollbar.background": "#282c34",
        "scrollbarSlider.background": "#3b414d",
        "scrollbarSlider.disabledBackground": "#3b414d",
        "scrollbarSlider.activeBackground": "#4e5563",
        "scrollbarSlider.hoverBackground": "#414855",
    }
)

window = QMainWindow()
aboutbox = QDialog()
new_doc_dialog = QDialog()

ui = Ui_MainWindow()
ui.setupUi(window)

# A4 layout
width = 2480
height = 3508
start_zoom = 0.3

# table of pages (QGraphicsScene)
pages = [create_empty_page()]
current_page = 0
update_page_change_buttons_colors()
update_zoom_buttons_colors()

# Bravura font, see <https://github.com/steinbergmedia/bravura/releases> and <https://w3c.github.io/smufl/latest/index.html> documentation
font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/Bravura.otf")

# check wether font loaded
if font_loaded == -1:
    print("Failed to load musicfont")

font = QFont("Bravura", 100)
text_item = QGraphicsTextItem(str(chr(int("1D11A", 16))*10 + str(chr(int("E030", 16)))), parent=None)
text_item.setDefaultTextColor(Qt.black)
text_item.setFont(font)
pages[0].addItem(text_item)

text_item = QGraphicsTextItem(str(chr(int("E099", 16))) + str(chr(int("EC46", 16))) + str(chr(int("EC62", 16))) + str(chr(int("E4E5", 16))) + str(chr(int("E0A2", 16))), parent=None)
text_item.setDefaultTextColor(Qt.black)
text_item.setFont(font)
pages[0].addItem(text_item)

# object which is needed to render the scene
# view can change when the scene changes (new page), but setWidget will never be called again
ui.view.setScene(pages[0])
ui.zoom_slider.setValue(int(start_zoom * 100))
apply_zoom()
ui.view.verticalScrollBar().setValue(ui.view.verticalScrollBar().minimum())
ui.view.horizontalScrollBar().setValue(ui.view.horizontalScrollBar().minimum())

# setup dialog ui
aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)
new_doc_dialog_ui = Ui_NewDocumentDialog()
new_doc_dialog_ui.setupUi(new_doc_dialog)

# menubar actions
ui.action_about.triggered.connect(aboutbox.show)
ui.action_new.triggered.connect(new_doc_dialog.show)
ui.zoom_slider.valueChanged.connect(apply_zoom)
ui.zoom_in_button.clicked.connect(zoom_in)
ui.zoom_out_button.clicked.connect(zoom_out)
ui.new_page_button.clicked.connect(new_page)
ui.delete_page_button.clicked.connect(delete_page)
ui.next_page_button.clicked.connect(next_page)
ui.previous_page_button.clicked.connect(previous_page)

window.show()
app.exec()
