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

ui.label = QLabel(ui.frame)
ui.label.setPixmap(QPixmap("../assets/icon.png"))
ui.label.move(10, 10)

def triggerwhatever():
    ui.label.move(0, ui.verticalScrollBar.value())

# setup dialog ui
aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)
new_doc_dialog_ui = Ui_NewDocumentDialog()
new_doc_dialog_ui.setupUi(new_doc_dialog)

# menubar actions
ui.action_about.triggered.connect(aboutbox.show)
ui.action_new.triggered.connect(new_doc_dialog.show)
ui.verticalScrollBar.valueChanged.connect(triggerwhatever)
ui.verticalScrollBar.setRange(0, 100)

window.show()
app.exec()
