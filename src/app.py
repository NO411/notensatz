from PyQt5.QtWidgets import QGraphicsBlurEffect, QLabel, QPushButton, QMenu, QHBoxLayout, QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics, QPainter

# from <https://pypi.org/project/pyqtdarktheme/>
import qdarktheme

# window / dialog imports
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog
from document import DocumentUi

# intern imports
from fonts import load_fonts, get_symbol
from notation_system import TimeSignature

class App_Ui(Ui_MainWindow):
	def __init__(self, app):
		super().__init__()
		self.setupUi(app.window)
		# this is for rendering staves correctly
		self.view.setRenderHint(QPainter.Antialiasing)

		# other ui setups
		# (seperately to not get overriden by the pyqt5 designer...)
		self.start_zoom = 0.3
		self.zoom_slider.setValue(int(self.start_zoom * 100))
		self.zoom_out_button.setFixedWidth(self.zoom_out_button.height())
		self.symbols_box_buttons = []
		self.box_tabs_layouts = []

		# welcome screen:
		# blur effect:
		self.in_welcome_screen = True
		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(12)
		self.centralwidget.setGraphicsEffect(self.blur_effect)
		self.centralwidget.setEnabled(False)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		label_font = QFont()
		label_font.setPointSize(20)
		label_font.setBold(True)

		self.welcome_label = QLabel("Willkommen!", app.window)
		self.welcome_label.setFont(label_font)
		self.welcome_label.setStyleSheet(f"color: {app.primary_color}; background-color: transparent")

		font_metrics = QFontMetrics(self.welcome_label.font())
		text_width = font_metrics.boundingRect(self.welcome_label.text()).width() + 10
		text_height = font_metrics.boundingRect(self.welcome_label.text()).height()
		self.welcome_label.setFixedSize(text_width, text_height)

		self.welcome_button_new = QPushButton("Neue Datei", app.window)
		self.welcome_button_new.setDefault(True)

		self.welcome_button_open = QPushButton("Datei öffnen", app.window)
		self.welcome_button_new.setDefault(True)

		edit_menu = self.menubar.findChild(QMenu, "menu_edit")
		edit_menu.setEnabled(False)

		self.action_save.setEnabled(False)
		self.action_save_as.setEnabled(False)
		self.action_export.setEnabled(False)

		self.init_symbol_buttons(app)

	def init_symbol_buttons(self, app):
		# setup symbol buttons
		for i, symbol_class in enumerate(app.symbols):
			self.symbols_box_buttons.insert(0, [])

			tab_widget = self.symbols_box.widget(i)
			self.box_tabs_layouts.insert(i, QHBoxLayout(tab_widget))
			self.box_tabs_layouts[i].setContentsMargins(3, 3, 3, 3)
			self.box_tabs_layouts[i].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			for name in symbol_class:
				# name[0]: unicode key
				# name[1]: tooltip text
				box_button = QPushButton(tab_widget)
				description = ""
				if (type(name[0]) == str):
					description = name[0]
				else:
					description = TimeSignature.join_unicode_combi(name[0])
				box_button.setObjectName(description + "Button")
				box_button.setFixedSize(35, 60)
				box_button.setFlat(True)
				box_button.setCheckable(True)
				box_button.setToolTip(name[1])
				box_button.setStyleSheet("QToolTip {color: black}")
				label = QLabel(get_symbol(name[0]), box_button)
				font = QFont("Bravura", 20)
				label.setFont(font)
				label.setAlignment(Qt.AlignHCenter)
				label.setGeometry(0, -20, box_button.width(), 100)

				self.box_tabs_layouts[i].addWidget(box_button)
				self.symbols_box_buttons[i].append(box_button)

class MainWindow(QMainWindow):
	close_signal = pyqtSignal()

	def __init__(self):
		super().__init__()

	def closeEvent(self, event):
		self.close_signal.emit()
		event.ignore()

class NewDocumentDialogUI(Ui_NewDocumentDialog):
	def setupUi(self, NewDocumentDialog):
		super().setupUi(NewDocumentDialog)
		self.voices_labels = [self.voice_1_label, self.voice_2_label, self.voice_3_label, self.voice_4_label]
		self.voices_combo_boxes = [self.voice_1_combo_box, self.voice_2_combo_box, self.voice_3_combo_box, self.voice_4_combo_box]
		self.staves_spin_box.valueChanged.connect(lambda: self.update_voice_combo_boxes(False))
	
	def update_voice_combo_boxes(self, reset: bool):
		for i in range(1, self.staves_spin_box.maximum() + 1):
			index = i - 1
			if (i > self.staves_spin_box.value()):
				self.voices_labels[index].setEnabled(False)
				self.voices_combo_boxes[index].setEnabled(False)
				self.voices_combo_boxes[index].setCurrentIndex(0)
			else:
				self.voices_labels[index].setEnabled(True)
				self.voices_combo_boxes[index].setEnabled(True)
				if (reset):
					self.voices_combo_boxes[index].setCurrentIndex(0)
		if (self.staves_spin_box.value() == 1):
			self.piano_checkbox.setEnabled(False)
		else:
			self.piano_checkbox.setEnabled(True)
	
	def reset(self):
		self.heading_line_edit.setText("")
		self.sub_heading_line_edit.setText("")
		self.composer_line_edit.setText("")
		self.tempo_line_edit.setText("")
		self.key_signatures_combo_box.setCurrentIndex(0)
		self.staves_spin_box.setValue(2)
		self.piano_checkbox.setEnabled(True)
		self.piano_checkbox.setChecked(False)
		self.update_voice_combo_boxes(True)
		self.time_signature_combo_box.setCurrentIndex(5)
	
	def get_clefs(self):
		"""return a lsit of clefs, like "Violinschlüssel", "Bassschlüssel", "Altschlüssel" or "Tenorschlüssel" """
		ret: list[str] = []
		for combo_box in self.voices_combo_boxes:
			if (combo_box.isEnabled()):
				ret.append(combo_box.currentText())
		return ret

class App(QApplication):
	def __init__(self):
		qdarktheme.enable_hi_dpi()
	
		self.app = QApplication([])

		load_fonts()
		# apply the dark theme to the app
		# see <https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html>
		self.primary_color = "#528bff"
		qdarktheme.setup_theme(
			custom_colors = {
				"primary": self.primary_color,
				"background": "#21252b",
				"border": "#474a4f",
				"foreground": "#d7d7d5",
				"scrollbar.background": "#282c34",
				"scrollbarSlider.background": "#3b414d",
				"scrollbarSlider.disabledBackground": "#3b414d",
				"scrollbarSlider.activeBackground": "#4e5563",
				"scrollbarSlider.hoverBackground": "#414855",
			},
			corner_shape="rounded"
		)

		self.document_ui = DocumentUi()

		# nos stands for NOtenSatz
		self.file_extension = "nos"
		self.current_file_name = ""
		self.current_file_saved = False

		# symbols that will be implemented
		# map of the symbols shown on the buttons in the symbols box
		# indexes MUST match with the indexes in the designer
		self.symbols = [
			# notes
			[# [unicode key, tooltip text]
			 # this key can also be a list
				["noteWhole", "ganze Note"],
				["noteHalfUp", "halbe Note"],
				["noteQuarterUp", "viertel Note"],
				["note8thUp", "achtel Note"],
				["note16thUp", "sechszehntel Note"],
				["note32ndUp", "zweiunddreißigstel Note"],
				["note64thUp", "vierundsechszigstel Note"],
				["metAugmentationDot", "Punktierung"],
			],
			# articulation
			[
				["articAccentAbove", "Akzent"],
				["articStaccatoAbove", "Staccato"],
				["articTenutoAbove", "Tenuto"],
				["keyboardPedalPed", "Pedal"],
				["keyboardPedalUp", "Pedal loslassen"],
			],
			# dynamics
			[
				["dynamicMP", "mezzopiano"],
				["dynamicPiano", "piano"],
				["dynamicPP", "pianissimo"],
				["dynamicPPP", "pianopianissimo"],
				["dynamicPF", "pianoforte"],
				["dynamicFortePiano", "fortepiano"],
				["dynamicMF", "mezzoforte"],
				["dynamicForte", "forte"],
				["dynamicFF", "fortissimo"],
				["dynamicFFF", "fortefortissimo"],
				["dynamicCrescendoHairpin", "crescendo"],
				["dynamicDiminuendoHairpin", "decrescendo"],
			],
			# rests
			[
				["restWholeLegerLine", "ganze Pause"],
				["restHalfLegerLine", "halbe pause"],
				["restQuarter", "viertel Pause"],
				["rest8th", "achtel Pause"],
				["rest16th", "sechszehntel Pause"],
				["rest32nd", "zweiunddreißigstel Pause"],
				["rest64th", "vierundsechszigstel Pause"],
				["metAugmentationDot", "Punktierung"],
			],
			# accidentals
			[
				["accidentalSharp", "Kreuz"],
				["accidentalFlat", "b"],
				["accidentalDoubleSharp", "Doppelkreuz"],
				["accidentalNatural", "Auflösung"],
				["accidentalDoubleFlat", "doppel b"],
			],
			# time signatures
			[
				[TimeSignature(time_sig_table[0], time_sig_table[1]).gen_unicode_combi(), description]
				for description, time_sig_table in TimeSignature.signatures_map.items()
			],
			# misc
			[
				["repeatDots", "Wiederholung"],
				["barlineSingle", "Taktstrich"],
				["gClefChange", "Violinchlüssel (Wechsel)"],
				["fClefChange", "Bassschlüssel (Wechsel)"],
				["cClefChange", "C-Schlüssel (Wechsel)"],
			],
		]
		
		self.show_warning_box = True
		self.current_page = 0

		self.window = MainWindow()
		self.aboutbox = QDialog()
		self.new_doc_dialog = QDialog()

		# setup main ui
		self.ui = App_Ui(self)
		self.window.resizeEvent = self.window_resize

		# setup dialog ui
		self.aboutbox_ui = Ui_AboutBox()
		self.aboutbox_ui.setupUi(self.aboutbox)
		self.new_doc_dialog_ui = NewDocumentDialogUI()
		self.new_doc_dialog_ui.setupUi(self.new_doc_dialog)

		# remove standard ?-help hymbol
		self.new_doc_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
		self.aboutbox.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

	def set_scene(self, page_index):
		"""page_index must be >= 0"""
		self.current_page = page_index
		self.ui.view.setScene(self.document_ui.pages[self.current_page].scene.qt())

	def window_resize(self, event):
		if (self.ui.in_welcome_screen):
			self.ui.welcome_label.move((self.window.width() - self.ui.welcome_label.width()) / 2, (self.window.height() - self.ui.welcome_label.height()) / 2)
			self.ui.welcome_button_new.move((self.window.width() - self.ui.welcome_button_new.width()) / 2 + self.ui.welcome_button_new.width() / 2 + 10, self.ui.welcome_label.y() + self.ui.welcome_label.height() + 20)
			self.ui.welcome_button_open.move((self.window.width() - self.ui.welcome_button_open.width()) / 2 - self.ui.welcome_button_open.width() / 2 - 10, self.ui.welcome_label.y() + self.ui.welcome_label.height() + 20)
	
	def end_welcome_screen(self):
		self.ui.in_welcome_screen = False
		self.ui.centralwidget.setEnabled(True)
		self.ui.centralwidget.setGraphicsEffect(None)
		self.ui.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.ui.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.ui.welcome_label.setParent(None)
		self.window.resizeEvent = None
		self.ui.welcome_button_new.setParent(None)
		self.ui.welcome_button_open.setParent(None)
		edit_menu = self.ui.menubar.findChild(QMenu, "menu_edit")
		edit_menu.setEnabled(True)
		self.ui.action_save.setEnabled(True)
		self.ui.action_save_as.setEnabled(True)
		self.ui.action_export.setEnabled(True)
