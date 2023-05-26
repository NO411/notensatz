# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt5_designer_uis/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("Notensatz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pyqt5_designer_uis\\../assets/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("pyqt5_designer_uis\\../../assets/icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAnimated(True)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, 9, 9, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.symbols_box = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.symbols_box.sizePolicy().hasHeightForWidth())
        self.symbols_box.setSizePolicy(sizePolicy)
        self.symbols_box.setMinimumSize(QtCore.QSize(0, 100))
        self.symbols_box.setMaximumSize(QtCore.QSize(16777215, 100))
        self.symbols_box.setSizeIncrement(QtCore.QSize(0, 100))
        self.symbols_box.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.symbols_box.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.symbols_box.setElideMode(QtCore.Qt.ElideLeft)
        self.symbols_box.setUsesScrollButtons(False)
        self.symbols_box.setDocumentMode(False)
        self.symbols_box.setTabsClosable(False)
        self.symbols_box.setMovable(True)
        self.symbols_box.setTabBarAutoHide(False)
        self.symbols_box.setObjectName("symbols_box")
        self.horizontalLayout.addWidget(self.symbols_box)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.view = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.view.setMouseTracking(False)
        self.view.setTabletTracking(False)
        self.view.setAcceptDrops(True)
        self.view.setAutoFillBackground(False)
        brush = QtGui.QBrush(QtGui.QColor(40, 44, 52))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.view.setBackgroundBrush(brush)
        self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        self.bottom_frame = QtWidgets.QFrame(self.centralwidget)
        self.bottom_frame.setMinimumSize(QtCore.QSize(0, 35))
        self.bottom_frame.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bottom_frame.setObjectName("bottom_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.bottom_frame)
        self.gridLayout.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.delete_last_system_button = QtWidgets.QPushButton(self.bottom_frame)
        self.delete_last_system_button.setFlat(False)
        self.delete_last_system_button.setObjectName("delete_last_system_button")
        self.gridLayout.addWidget(self.delete_last_system_button, 0, 4, 1, 1)
        self.new_system_button = QtWidgets.QPushButton(self.bottom_frame)
        self.new_system_button.setDefault(True)
        self.new_system_button.setFlat(False)
        self.new_system_button.setObjectName("new_system_button")
        self.gridLayout.addWidget(self.new_system_button, 0, 3, 1, 1)
        self.zoom_in_button = QtWidgets.QPushButton(self.bottom_frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.zoom_in_button.setFont(font)
        self.zoom_in_button.setFlat(True)
        self.zoom_in_button.setObjectName("zoom_in_button")
        self.gridLayout.addWidget(self.zoom_in_button, 0, 12, 1, 1)
        self.next_page_button = QtWidgets.QPushButton(self.bottom_frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.next_page_button.setFont(font)
        self.next_page_button.setFlat(True)
        self.next_page_button.setObjectName("next_page_button")
        self.gridLayout.addWidget(self.next_page_button, 0, 2, 1, 1)
        self.previous_page_button = QtWidgets.QPushButton(self.bottom_frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.previous_page_button.setFont(font)
        self.previous_page_button.setFlat(True)
        self.previous_page_button.setObjectName("previous_page_button")
        self.gridLayout.addWidget(self.previous_page_button, 0, 1, 1, 1)
        self.zoom_label = QtWidgets.QLabel(self.bottom_frame)
        self.zoom_label.setObjectName("zoom_label")
        self.gridLayout.addWidget(self.zoom_label, 0, 13, 1, 1)
        self.zoom_out_button = QtWidgets.QPushButton(self.bottom_frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.zoom_out_button.setFont(font)
        self.zoom_out_button.setCheckable(False)
        self.zoom_out_button.setChecked(False)
        self.zoom_out_button.setAutoDefault(False)
        self.zoom_out_button.setDefault(False)
        self.zoom_out_button.setFlat(True)
        self.zoom_out_button.setObjectName("zoom_out_button")
        self.gridLayout.addWidget(self.zoom_out_button, 0, 10, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 9, 1, 1)
        self.current_page_label = QtWidgets.QLabel(self.bottom_frame)
        font = QtGui.QFont()
        font.setItalic(False)
        self.current_page_label.setFont(font)
        self.current_page_label.setObjectName("current_page_label")
        self.gridLayout.addWidget(self.current_page_label, 0, 0, 1, 1)
        self.zoom_slider = QtWidgets.QSlider(self.bottom_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_slider.sizePolicy().hasHeightForWidth())
        self.zoom_slider.setSizePolicy(sizePolicy)
        self.zoom_slider.setMinimumSize(QtCore.QSize(100, 0))
        self.zoom_slider.setMaximumSize(QtCore.QSize(100, 16777215))
        self.zoom_slider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(150)
        self.zoom_slider.setSingleStep(1)
        self.zoom_slider.setOrientation(QtCore.Qt.Horizontal)
        self.zoom_slider.setObjectName("zoom_slider")
        self.gridLayout.addWidget(self.zoom_slider, 0, 11, 1, 1)
        self.verticalLayout.addWidget(self.bottom_frame)
        self.bottom_frame.raise_()
        self.view.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_edit = QtWidgets.QMenu(self.menubar)
        self.menu_edit.setObjectName("menu_edit")
        MainWindow.setMenuBar(self.menubar)
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_close = QtWidgets.QAction(MainWindow)
        self.action_close.setObjectName("action_close")
        self.action_doc = QtWidgets.QAction(MainWindow)
        self.action_doc.setObjectName("action_doc")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_save_as = QtWidgets.QAction(MainWindow)
        self.action_save_as.setObjectName("action_save_as")
        self.action_export = QtWidgets.QAction(MainWindow)
        self.action_export.setObjectName("action_export")
        self.action_edit_heading = QtWidgets.QAction(MainWindow)
        self.action_edit_heading.setObjectName("action_edit_heading")
        self.action_edit_composer = QtWidgets.QAction(MainWindow)
        self.action_edit_composer.setObjectName("action_edit_composer")
        self.action_edit_subheading = QtWidgets.QAction(MainWindow)
        self.action_edit_subheading.setObjectName("action_edit_subheading")
        self.action_edit_tempo = QtWidgets.QAction(MainWindow)
        self.action_edit_tempo.setObjectName("action_edit_tempo")
        self.action_tutorial = QtWidgets.QAction(MainWindow)
        self.action_tutorial.setObjectName("action_tutorial")
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addAction(self.action_export)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_close)
        self.menu_help.addAction(self.action_tutorial)
        self.menu_help.addAction(self.action_doc)
        self.menu_help.addAction(self.action_about)
        self.menu_edit.addAction(self.action_edit_heading)
        self.menu_edit.addAction(self.action_edit_subheading)
        self.menu_edit.addAction(self.action_edit_composer)
        self.menu_edit.addAction(self.action_edit_tempo)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.symbols_box.setCurrentIndex(-1)
        self.action_close.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.delete_last_system_button.setText(_translate("MainWindow", "Letztes System löschen"))
        self.new_system_button.setText(_translate("MainWindow", "Neues System"))
        self.zoom_in_button.setText(_translate("MainWindow", "+"))
        self.next_page_button.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#000000;\">Nächste Seite</span></p></body></html>"))
        self.next_page_button.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.next_page_button.setText(_translate("MainWindow", "🡢"))
        self.previous_page_button.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#000000;\">Vorherige Seite</span></p></body></html>"))
        self.previous_page_button.setText(_translate("MainWindow", "🡠"))
        self.zoom_label.setText(_translate("MainWindow", "0%"))
        self.zoom_out_button.setText(_translate("MainWindow", "-"))
        self.current_page_label.setText(_translate("MainWindow", "Seite 1 von 1"))
        self.menu_file.setTitle(_translate("MainWindow", "Datei"))
        self.menu_help.setTitle(_translate("MainWindow", "Hilfe"))
        self.menu_edit.setTitle(_translate("MainWindow", "Bearbeiten"))
        self.action_new.setText(_translate("MainWindow", "Neu"))
        self.action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_open.setText(_translate("MainWindow", "Öffnen"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_save.setText(_translate("MainWindow", "Speichern"))
        self.action_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_close.setText(_translate("MainWindow", "Beenden"))
        self.action_close.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_doc.setText(_translate("MainWindow", "Dokumentation"))
        self.action_about.setText(_translate("MainWindow", "Über uns"))
        self.action_save_as.setText(_translate("MainWindow", "Speichern unter"))
        self.action_save_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.action_export.setText(_translate("MainWindow", "Exportieren"))
        self.action_export.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_edit_heading.setText(_translate("MainWindow", "Titel ändern"))
        self.action_edit_composer.setText(_translate("MainWindow", "Komponist ändern"))
        self.action_edit_subheading.setText(_translate("MainWindow", "Unterüberschrift ändern"))
        self.action_edit_tempo.setText(_translate("MainWindow", "Tempoangabe ändern"))
        self.action_tutorial.setText(_translate("MainWindow", "Anleitung"))
