"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from mainwindow import Ui_MainWindow
import assets.breeze_resources


__author__ = "Noah Weiler"

app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()

ui.setupUi(window)
window.show()

app.exec()
