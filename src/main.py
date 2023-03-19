"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

from PyQt5.QtWidgets import *
import qdarktheme
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog

__author__ = "Noah Weiler"

app = QApplication([])

# apply the dark theme to the app
qdarktheme.setup_theme()

window = QMainWindow()
aboutbox = QDialog()
new_doc_dialog = QDialog()

ui = Ui_MainWindow()
ui.setupUi(window)

aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)
new_doc_dialog_ui = Ui_NewDocumentDialog()
new_doc_dialog_ui.setupUi(new_doc_dialog)

ui.action_about.triggered.connect(aboutbox.show)
ui.action_new.triggered.connect(new_doc_dialog.show)

window.show()
app.exec()
