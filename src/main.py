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

__author__ = "Noah Weiler"

def apply_zoom():
    new_zoom = ui.zoom_slider.value() / 100
    ui.view.resetTransform()
    ui.view.scale(new_zoom, new_zoom)
    ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")

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

def update_page_info_text():
    ui.current_page_label.setText("Seite " + str(current_page + 1) + " von " + str(len(pages)))

def new_page():
    global current_page
    new_page = create_empty_page()
    if (len(pages) == current_page + 1):
        pages.append(new_page)
    else:
        pages.insert(current_page + 1, new_page)
    current_page += 1
    ui.view.setScene(pages[current_page])
    update_page_info_text()

def delete_page():
    global current_page
    # really?? dialog
    pages.pop(current_page)
    current_page -= 1
    if (current_page < 0):
        current_page = 0
    if (len(pages) == 0):
        pages.append(create_empty_page())

    ui.view.setScene(pages[current_page])
    update_page_info_text()
    
def next_page():
    global current_page
    if (current_page + 1 < len(pages)):
        current_page += 1
        ui.view.setScene(pages[current_page])
        update_page_info_text()

def previous_page():
    global current_page
    if (current_page > 0):
        current_page -= 1
        ui.view.setScene(pages[current_page])
        update_page_info_text()

qdarktheme.enable_hi_dpi()
app = QApplication([])

# apply the dark theme to the app
qdarktheme.setup_theme()
# see <https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html>
#qdarktheme.setup_theme(corner_shape="sharp")
#qdarktheme.setup_theme(custom_colors={"primary": "#ff4a6b"})

window = QMainWindow()
aboutbox = QDialog()
new_doc_dialog = QDialog()

ui = Ui_MainWindow()
ui.setupUi(window)

# A4 layout
width = 2480
height = 3508
start_zoom = 0.3

# table of pages (scenes)
pages = [create_empty_page()]
current_page = 0

# example how to add something to a scene
pixmap = QPixmap("../assets/icon.png")
pages[0].addPixmap(pixmap)

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
ui.zoom_in_button.pressed.connect(zoom_in)
ui.zoom_out_button.pressed.connect(zoom_out)
ui.new_page_button.pressed.connect(new_page)
ui.delete_page_button.pressed.connect(delete_page)
ui.next_page_button.pressed.connect(next_page)
ui.previous_page_button.pressed.connect(previous_page)

window.show()
app.exec()
