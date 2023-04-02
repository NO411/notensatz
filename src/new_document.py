# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt5_designer_uis/new_document.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewDocumentDialog(object):
    def setupUi(self, NewDocumentDialog):
        NewDocumentDialog.setObjectName("NewDocumentDialog")
        NewDocumentDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NewDocumentDialog.resize(400, 300)
        NewDocumentDialog.setMinimumSize(QtCore.QSize(400, 300))
        NewDocumentDialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pyqt5_designer_uis\\../../assets/icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        NewDocumentDialog.setWindowIcon(icon)
        NewDocumentDialog.setSizeGripEnabled(False)
        NewDocumentDialog.setModal(True)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(NewDocumentDialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.setObjectName("settings_layout")
        self.text_fields_layout = QtWidgets.QHBoxLayout()
        self.text_fields_layout.setObjectName("text_fields_layout")
        self.labels_layout = QtWidgets.QVBoxLayout()
        self.labels_layout.setObjectName("labels_layout")
        self.heading_label = QtWidgets.QLabel(NewDocumentDialog)
        self.heading_label.setObjectName("heading_label")
        self.labels_layout.addWidget(self.heading_label)
        self.sub_heading_label = QtWidgets.QLabel(NewDocumentDialog)
        self.sub_heading_label.setObjectName("sub_heading_label")
        self.labels_layout.addWidget(self.sub_heading_label)
        self.composer_heading = QtWidgets.QLabel(NewDocumentDialog)
        self.composer_heading.setObjectName("composer_heading")
        self.labels_layout.addWidget(self.composer_heading)
        self.text_fields_layout.addLayout(self.labels_layout)
        self.line_edits_layout = QtWidgets.QVBoxLayout()
        self.line_edits_layout.setObjectName("line_edits_layout")
        self.heading_line_edit = QtWidgets.QLineEdit(NewDocumentDialog)
        self.heading_line_edit.setInputMask("")
        self.heading_line_edit.setText("")
        self.heading_line_edit.setObjectName("heading_line_edit")
        self.line_edits_layout.addWidget(self.heading_line_edit)
        self.sub_heading_line_edit = QtWidgets.QLineEdit(NewDocumentDialog)
        self.sub_heading_line_edit.setObjectName("sub_heading_line_edit")
        self.line_edits_layout.addWidget(self.sub_heading_line_edit)
        self.composer_line_edit = QtWidgets.QLineEdit(NewDocumentDialog)
        self.composer_line_edit.setObjectName("composer_line_edit")
        self.line_edits_layout.addWidget(self.composer_line_edit)
        self.text_fields_layout.addLayout(self.line_edits_layout)
        self.settings_layout.addLayout(self.text_fields_layout)
        self.place_holder = QtWidgets.QWidget(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.place_holder.sizePolicy().hasHeightForWidth())
        self.place_holder.setSizePolicy(sizePolicy)
        self.place_holder.setObjectName("place_holder")
        self.settings_layout.addWidget(self.place_holder)
        self.verticalLayout_5.addLayout(self.settings_layout)
        self.buttons_ayout = QtWidgets.QHBoxLayout()
        self.buttons_ayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.buttons_ayout.setObjectName("buttons_ayout")
        self.save_settings_check_box = QtWidgets.QCheckBox(NewDocumentDialog)
        self.save_settings_check_box.setObjectName("save_settings_check_box")
        self.buttons_ayout.addWidget(self.save_settings_check_box)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_ayout.addItem(spacerItem)
        self.ok_button = QtWidgets.QPushButton(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok_button.sizePolicy().hasHeightForWidth())
        self.ok_button.setSizePolicy(sizePolicy)
        self.ok_button.setAutoDefault(False)
        self.ok_button.setDefault(True)
        self.ok_button.setFlat(False)
        self.ok_button.setObjectName("ok_button")
        self.buttons_ayout.addWidget(self.ok_button)
        self.abort_button = QtWidgets.QPushButton(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.abort_button.sizePolicy().hasHeightForWidth())
        self.abort_button.setSizePolicy(sizePolicy)
        self.abort_button.setAutoDefault(False)
        self.abort_button.setFlat(False)
        self.abort_button.setObjectName("abort_button")
        self.buttons_ayout.addWidget(self.abort_button)
        self.verticalLayout_5.addLayout(self.buttons_ayout)

        self.retranslateUi(NewDocumentDialog)
        self.abort_button.clicked.connect(NewDocumentDialog.close)
        QtCore.QMetaObject.connectSlotsByName(NewDocumentDialog)

    def retranslateUi(self, NewDocumentDialog):
        _translate = QtCore.QCoreApplication.translate
        NewDocumentDialog.setWindowTitle(_translate("NewDocumentDialog", "Neues Dokument - Notensatz"))
        self.heading_label.setText(_translate("NewDocumentDialog", "Titel"))
        self.sub_heading_label.setText(_translate("NewDocumentDialog", "Unterüberschrift"))
        self.composer_heading.setText(_translate("NewDocumentDialog", "Komponist / Arrangeur"))
        self.save_settings_check_box.setText(_translate("NewDocumentDialog", "Einstellungen speichern"))
        self.ok_button.setText(_translate("NewDocumentDialog", "OK"))
        self.abort_button.setText(_translate("NewDocumentDialog", "Abbrechen"))
