"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

from PyQt5.QtWidgets import *
from mainwindow import Ui_MainWindow


__author__ = "Noah Weiler"

app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()

ui.setupUi(window)
window.show()

app.exec()
