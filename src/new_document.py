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
        NewDocumentDialog.resize(400, 450)
        NewDocumentDialog.setMinimumSize(QtCore.QSize(400, 450))
        NewDocumentDialog.setMaximumSize(QtCore.QSize(400, 450))
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
        self.tempo_label = QtWidgets.QLabel(NewDocumentDialog)
        self.tempo_label.setObjectName("tempo_label")
        self.labels_layout.addWidget(self.tempo_label)
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
        self.tempo_line_edit = QtWidgets.QLineEdit(NewDocumentDialog)
        self.tempo_line_edit.setObjectName("tempo_line_edit")
        self.line_edits_layout.addWidget(self.tempo_line_edit)
        self.text_fields_layout.addLayout(self.line_edits_layout)
        self.settings_layout.addLayout(self.text_fields_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.settings_layout.addItem(spacerItem)
        self.specific_settings_layout = QtWidgets.QHBoxLayout()
        self.specific_settings_layout.setObjectName("specific_settings_layout")
        self.time_signature_group_box = QtWidgets.QGroupBox(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_signature_group_box.sizePolicy().hasHeightForWidth())
        self.time_signature_group_box.setSizePolicy(sizePolicy)
        self.time_signature_group_box.setObjectName("time_signature_group_box")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.time_signature_group_box)
        self.horizontalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.time_signature_combo_box = QtWidgets.QComboBox(self.time_signature_group_box)
        self.time_signature_combo_box.setObjectName("time_signature_combo_box")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.time_signature_combo_box.addItem("")
        self.horizontalLayout_3.addWidget(self.time_signature_combo_box)
        self.specific_settings_layout.addWidget(self.time_signature_group_box)
        self.key_signature_group_box = QtWidgets.QGroupBox(NewDocumentDialog)
        self.key_signature_group_box.setObjectName("key_signature_group_box")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.key_signature_group_box)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.key_signatures_combo_box = QtWidgets.QComboBox(self.key_signature_group_box)
        self.key_signatures_combo_box.setObjectName("key_signatures_combo_box")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.key_signatures_combo_box.addItem("")
        self.horizontalLayout_4.addWidget(self.key_signatures_combo_box)
        self.specific_settings_layout.addWidget(self.key_signature_group_box)
        self.settings_layout.addLayout(self.specific_settings_layout)
        self.voices_group_box = QtWidgets.QGroupBox(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voices_group_box.sizePolicy().hasHeightForWidth())
        self.voices_group_box.setSizePolicy(sizePolicy)
        self.voices_group_box.setObjectName("voices_group_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.voices_group_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.voices_top_layout = QtWidgets.QHBoxLayout()
        self.voices_top_layout.setObjectName("voices_top_layout")
        self.staffs_label = QtWidgets.QLabel(self.voices_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffs_label.sizePolicy().hasHeightForWidth())
        self.staffs_label.setSizePolicy(sizePolicy)
        self.staffs_label.setObjectName("staffs_label")
        self.voices_top_layout.addWidget(self.staffs_label)
        self.staves_spin_box = QtWidgets.QSpinBox(self.voices_group_box)
        self.staves_spin_box.setFrame(True)
        self.staves_spin_box.setMinimum(1)
        self.staves_spin_box.setMaximum(4)
        self.staves_spin_box.setProperty("value", 2)
        self.staves_spin_box.setObjectName("staves_spin_box")
        self.voices_top_layout.addWidget(self.staves_spin_box)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.voices_top_layout.addItem(spacerItem1)
        self.piano_checkbox = QtWidgets.QCheckBox(self.voices_group_box)
        self.piano_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.piano_checkbox.setAutoFillBackground(False)
        self.piano_checkbox.setChecked(False)
        self.piano_checkbox.setAutoExclusive(False)
        self.piano_checkbox.setTristate(False)
        self.piano_checkbox.setObjectName("piano_checkbox")
        self.voices_top_layout.addWidget(self.piano_checkbox)
        self.verticalLayout.addLayout(self.voices_top_layout)
        self.voices_bottom_layout = QtWidgets.QHBoxLayout()
        self.voices_bottom_layout.setObjectName("voices_bottom_layout")
        self.voices_labels_layout = QtWidgets.QVBoxLayout()
        self.voices_labels_layout.setObjectName("voices_labels_layout")
        self.voice_1_label = QtWidgets.QLabel(self.voices_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voice_1_label.sizePolicy().hasHeightForWidth())
        self.voice_1_label.setSizePolicy(sizePolicy)
        self.voice_1_label.setObjectName("voice_1_label")
        self.voices_labels_layout.addWidget(self.voice_1_label)
        self.voice_2_label = QtWidgets.QLabel(self.voices_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voice_2_label.sizePolicy().hasHeightForWidth())
        self.voice_2_label.setSizePolicy(sizePolicy)
        self.voice_2_label.setObjectName("voice_2_label")
        self.voices_labels_layout.addWidget(self.voice_2_label)
        self.voice_3_label = QtWidgets.QLabel(self.voices_group_box)
        self.voice_3_label.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voice_3_label.sizePolicy().hasHeightForWidth())
        self.voice_3_label.setSizePolicy(sizePolicy)
        self.voice_3_label.setObjectName("voice_3_label")
        self.voices_labels_layout.addWidget(self.voice_3_label)
        self.voice_4_label = QtWidgets.QLabel(self.voices_group_box)
        self.voice_4_label.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voice_4_label.sizePolicy().hasHeightForWidth())
        self.voice_4_label.setSizePolicy(sizePolicy)
        self.voice_4_label.setObjectName("voice_4_label")
        self.voices_labels_layout.addWidget(self.voice_4_label)
        self.voices_bottom_layout.addLayout(self.voices_labels_layout)
        self.voices_combo_boxes_layout = QtWidgets.QVBoxLayout()
        self.voices_combo_boxes_layout.setObjectName("voices_combo_boxes_layout")
        self.voice_1_combo_box = QtWidgets.QComboBox(self.voices_group_box)
        self.voice_1_combo_box.setObjectName("voice_1_combo_box")
        self.voice_1_combo_box.addItem("")
        self.voice_1_combo_box.addItem("")
        self.voice_1_combo_box.addItem("")
        self.voice_1_combo_box.addItem("")
        self.voices_combo_boxes_layout.addWidget(self.voice_1_combo_box)
        self.voice_2_combo_box = QtWidgets.QComboBox(self.voices_group_box)
        self.voice_2_combo_box.setObjectName("voice_2_combo_box")
        self.voice_2_combo_box.addItem("")
        self.voice_2_combo_box.addItem("")
        self.voice_2_combo_box.addItem("")
        self.voice_2_combo_box.addItem("")
        self.voices_combo_boxes_layout.addWidget(self.voice_2_combo_box)
        self.voice_3_combo_box = QtWidgets.QComboBox(self.voices_group_box)
        self.voice_3_combo_box.setEnabled(False)
        self.voice_3_combo_box.setObjectName("voice_3_combo_box")
        self.voice_3_combo_box.addItem("")
        self.voice_3_combo_box.addItem("")
        self.voice_3_combo_box.addItem("")
        self.voice_3_combo_box.addItem("")
        self.voices_combo_boxes_layout.addWidget(self.voice_3_combo_box)
        self.voice_4_combo_box = QtWidgets.QComboBox(self.voices_group_box)
        self.voice_4_combo_box.setEnabled(False)
        self.voice_4_combo_box.setObjectName("voice_4_combo_box")
        self.voice_4_combo_box.addItem("")
        self.voice_4_combo_box.addItem("")
        self.voice_4_combo_box.addItem("")
        self.voice_4_combo_box.addItem("")
        self.voices_combo_boxes_layout.addWidget(self.voice_4_combo_box)
        self.voices_bottom_layout.addLayout(self.voices_combo_boxes_layout)
        self.verticalLayout.addLayout(self.voices_bottom_layout)
        self.settings_layout.addWidget(self.voices_group_box)
        self.verticalLayout_5.addLayout(self.settings_layout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.buttons_layout.setObjectName("buttons_layout")
        self.save_settings_check_box = QtWidgets.QCheckBox(NewDocumentDialog)
        self.save_settings_check_box.setObjectName("save_settings_check_box")
        self.buttons_layout.addWidget(self.save_settings_check_box)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(spacerItem3)
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
        self.buttons_layout.addWidget(self.ok_button)
        self.abort_button = QtWidgets.QPushButton(NewDocumentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.abort_button.sizePolicy().hasHeightForWidth())
        self.abort_button.setSizePolicy(sizePolicy)
        self.abort_button.setAutoDefault(False)
        self.abort_button.setFlat(False)
        self.abort_button.setObjectName("abort_button")
        self.buttons_layout.addWidget(self.abort_button)
        self.verticalLayout_5.addLayout(self.buttons_layout)

        self.retranslateUi(NewDocumentDialog)
        self.time_signature_combo_box.setCurrentIndex(5)
        self.voice_2_combo_box.setCurrentIndex(0)
        self.voice_3_combo_box.setCurrentIndex(0)
        self.abort_button.clicked.connect(NewDocumentDialog.close)
        QtCore.QMetaObject.connectSlotsByName(NewDocumentDialog)

    def retranslateUi(self, NewDocumentDialog):
        _translate = QtCore.QCoreApplication.translate
        NewDocumentDialog.setWindowTitle(_translate("NewDocumentDialog", "Neues Dokument - Notensatz"))
        self.heading_label.setText(_translate("NewDocumentDialog", "Titel"))
        self.sub_heading_label.setText(_translate("NewDocumentDialog", "Unterüberschrift"))
        self.composer_heading.setText(_translate("NewDocumentDialog", "Komponist / Arrangeur"))
        self.tempo_label.setText(_translate("NewDocumentDialog", "Tempoangabe"))
        self.time_signature_group_box.setTitle(_translate("NewDocumentDialog", "Takttart"))
        self.time_signature_combo_box.setItemText(0, _translate("NewDocumentDialog", "2/4-Takt"))
        self.time_signature_combo_box.setItemText(1, _translate("NewDocumentDialog", "2/2-Takt"))
        self.time_signature_combo_box.setItemText(2, _translate("NewDocumentDialog", "3/2-Takt"))
        self.time_signature_combo_box.setItemText(3, _translate("NewDocumentDialog", "3/4-Takt"))
        self.time_signature_combo_box.setItemText(4, _translate("NewDocumentDialog", "3/8-Takt"))
        self.time_signature_combo_box.setItemText(5, _translate("NewDocumentDialog", "4/4-Takt"))
        self.time_signature_combo_box.setItemText(6, _translate("NewDocumentDialog", "5/4-Takt"))
        self.time_signature_combo_box.setItemText(7, _translate("NewDocumentDialog", "5/8-Takt"))
        self.time_signature_combo_box.setItemText(8, _translate("NewDocumentDialog", "6/4-Takt"))
        self.time_signature_combo_box.setItemText(9, _translate("NewDocumentDialog", "6/8-Takt"))
        self.time_signature_combo_box.setItemText(10, _translate("NewDocumentDialog", "7/8-Takt"))
        self.time_signature_combo_box.setItemText(11, _translate("NewDocumentDialog", "9/8-Takt"))
        self.time_signature_combo_box.setItemText(12, _translate("NewDocumentDialog", "12/8-Takt"))
        self.key_signature_group_box.setTitle(_translate("NewDocumentDialog", "Tonart"))
        self.key_signatures_combo_box.setItemText(0, _translate("NewDocumentDialog", "C-Dur / a-Moll", "0"))
        self.key_signatures_combo_box.setItemText(1, _translate("NewDocumentDialog", "G-Dur / e-Moll", "1#"))
        self.key_signatures_combo_box.setItemText(2, _translate("NewDocumentDialog", "D-Dur / h-Moll", "2#"))
        self.key_signatures_combo_box.setItemText(3, _translate("NewDocumentDialog", "A-Dur / fis-Moll", "3#"))
        self.key_signatures_combo_box.setItemText(4, _translate("NewDocumentDialog", "E-Dur / cis-Moll", "4#"))
        self.key_signatures_combo_box.setItemText(5, _translate("NewDocumentDialog", "H-Dur / gis-Moll", "5#"))
        self.key_signatures_combo_box.setItemText(6, _translate("NewDocumentDialog", "Fis-Dur / dis-Moll", "6#"))
        self.key_signatures_combo_box.setItemText(7, _translate("NewDocumentDialog", "Cis-Dur / ais-Moll", "7#"))
        self.key_signatures_combo_box.setItemText(8, _translate("NewDocumentDialog", "F-Dur / d-Moll", "1b"))
        self.key_signatures_combo_box.setItemText(9, _translate("NewDocumentDialog", "B-Dur / g-Moll", "2b"))
        self.key_signatures_combo_box.setItemText(10, _translate("NewDocumentDialog", "Es-Dur / c-Moll", "3b"))
        self.key_signatures_combo_box.setItemText(11, _translate("NewDocumentDialog", "As-Dur / f-Moll", "4b"))
        self.key_signatures_combo_box.setItemText(12, _translate("NewDocumentDialog", "Des-Dur / b-Moll", "5b"))
        self.key_signatures_combo_box.setItemText(13, _translate("NewDocumentDialog", "Ges-Dur / es-moll", "6b"))
        self.key_signatures_combo_box.setItemText(14, _translate("NewDocumentDialog", "Ces-Dur / as-Moll", "7b"))
        self.voices_group_box.setTitle(_translate("NewDocumentDialog", "Stimmen"))
        self.staffs_label.setText(_translate("NewDocumentDialog", "Anzahl"))
        self.piano_checkbox.setText(_translate("NewDocumentDialog", "mit Klavierstimme"))
        self.voice_1_label.setText(_translate("NewDocumentDialog", "Stimme 1"))
        self.voice_2_label.setText(_translate("NewDocumentDialog", "Stimme 2"))
        self.voice_3_label.setText(_translate("NewDocumentDialog", "Stimme 3"))
        self.voice_4_label.setText(_translate("NewDocumentDialog", "Stimme 4"))
        self.voice_1_combo_box.setItemText(0, _translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_1_combo_box.setItemText(1, _translate("NewDocumentDialog", "Bassschlüssel"))
        self.voice_1_combo_box.setItemText(2, _translate("NewDocumentDialog", "Altschlüssel"))
        self.voice_1_combo_box.setItemText(3, _translate("NewDocumentDialog", "Tenorschlüssel"))
        self.voice_2_combo_box.setCurrentText(_translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_2_combo_box.setItemText(0, _translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_2_combo_box.setItemText(1, _translate("NewDocumentDialog", "Bassschlüssel"))
        self.voice_2_combo_box.setItemText(2, _translate("NewDocumentDialog", "Altschlüssel"))
        self.voice_2_combo_box.setItemText(3, _translate("NewDocumentDialog", "Tenorschlüssel"))
        self.voice_3_combo_box.setCurrentText(_translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_3_combo_box.setItemText(0, _translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_3_combo_box.setItemText(1, _translate("NewDocumentDialog", "Bassschlüssel"))
        self.voice_3_combo_box.setItemText(2, _translate("NewDocumentDialog", "Altschlüssel"))
        self.voice_3_combo_box.setItemText(3, _translate("NewDocumentDialog", "Tenorschlüssel"))
        self.voice_4_combo_box.setItemText(0, _translate("NewDocumentDialog", "Violinschlüssel"))
        self.voice_4_combo_box.setItemText(1, _translate("NewDocumentDialog", "Bassschlüssel"))
        self.voice_4_combo_box.setItemText(2, _translate("NewDocumentDialog", "Altschlüssel"))
        self.voice_4_combo_box.setItemText(3, _translate("NewDocumentDialog", "Tenorschlüssel"))
        self.save_settings_check_box.setText(_translate("NewDocumentDialog", "Einstellungen speichern"))
        self.ok_button.setText(_translate("NewDocumentDialog", "OK"))
        self.ok_button.setShortcut(_translate("NewDocumentDialog", "Return"))
        self.abort_button.setText(_translate("NewDocumentDialog", "Abbrechen"))
        self.abort_button.setShortcut(_translate("NewDocumentDialog", "Esc"))
