"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

from PyQt5.QtWidgets import *
import qdarktheme
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox

__author__ = "Noah Weiler"

app = QApplication([])

# apply the dark theme to the app
qdarktheme.setup_theme()

window = QMainWindow()
aboutbox = QDialog()


ui = Ui_MainWindow()
ui.setupUi(window)

aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)

ui.action_about.triggered.connect(aboutbox.show)

window.show()
app.exec()
