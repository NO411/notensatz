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
    view.resetTransform()
    view.scale(new_zoom, new_zoom)
    ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")

def zoom(change):
    ui.zoom_slider.setValue(ui.zoom_slider.value() + change)
    apply_zoom()

def zoom_in():
    zoom(1)

def zoom_out():
    zoom(-1)

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
scene = QGraphicsScene(0, 0, width, height)
# white background
rect = QGraphicsRectItem(0, 0, width, height)
rect.setBrush(QBrush(Qt.white))
scene.addItem(rect)

# example how to add something to a scene
pixmap = QPixmap("../assets/icon.png")
scene.addPixmap(pixmap)

# object which is needed to render the scene, attached to the scroll area
# view can change when the scene changes (new page), but setWidget will never be called again
view = QGraphicsView(scene)
ui.zoom_slider.setValue(int(start_zoom * 100))
apply_zoom()

# set up scroll area which holds the view
# the scrollbars are actually fromn the view widget
ui.scroll_area.setWidget(view)
ui.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
ui.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

window.show()
app.exec()
