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
import qdarktheme

__author__ = "Noah Weiler"

app = QApplication([])

# apply the dark theme to the app
qdarktheme.setup_theme()

window = QMainWindow()
aboutbox = QDialog()
new_doc_dialog = QDialog()

ui = Ui_MainWindow()
ui.setupUi(window)
# to be sure this is really called
ui.scrollArea.setWidgetResizable(True)

# A4 layout
scene = QGraphicsScene(0, 0, 2480, 3508)
# white background
scene.setBackgroundBrush(QBrush(Qt.white))

# example how to add something to a scene
pixmap = QPixmap("../assets/icon.png")
scene.addPixmap(pixmap)
textitem = scene.addText("QGraphics is (not) fun!")
textitem.setPos(100, 100)

# object which is needed to render the scene, attached to the scroll area
# view can change when the scene changes (new page), but setWidget will never be called again
view = QGraphicsView(scene)
ui.scrollArea.setWidget(view)

# setup dialog ui
aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)
new_doc_dialog_ui = Ui_NewDocumentDialog()
new_doc_dialog_ui.setupUi(new_doc_dialog)

# menubar actions
ui.action_about.triggered.connect(aboutbox.show)
ui.action_new.triggered.connect(new_doc_dialog.show)

window.show()
app.exec()
