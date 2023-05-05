from PyQt5.QtWidgets import QGraphicsBlurEffect, QLabel, QPushButton, QMenu, QHBoxLayout, QApplication, QMainWindow, QDialog, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QFileInfo
from PyQt5.QtGui import QFont, QFontMetrics, QPainter

# from <https://pypi.org/project/pyqtdarktheme/>
import qdarktheme
import json
from typing import List

# window / dialog imports
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog
from document import DocumentUi
from symbol_button import SymbolButton
from settings import Settings

# intern imports
from fonts import load_fonts

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
		self.symbols_box_buttons: List[List[SymbolButton]] = [[] for _ in SymbolButton.SYMBOLS]
		self.box_tabs_layouts: List[QHBoxLayout] = []

		self.init_symbol_buttons()

		# setup welcome screen
		self.setup_welcome_screen(app)

	def init_symbol_buttons(self):
		# setup symbol buttons
		n_group = 0
		for group_key, group in SymbolButton.SYMBOLS.items():
			self.symbols_box.addTab(QWidget(), group_key)
			tab_widget = self.symbols_box.widget(n_group)
			self.box_tabs_layouts.append(QHBoxLayout(tab_widget))
			self.box_tabs_layouts[n_group].setContentsMargins(3, 3, 3, 3)
			self.box_tabs_layouts[n_group].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

			for n_symbol, _ in enumerate(group["buttons"]):
				box_button = SymbolButton(tab_widget, group_key, n_symbol)

				self.box_tabs_layouts[n_group].addWidget(box_button)
				self.symbols_box_buttons[n_group].append(box_button)
			n_group += 1

	def end_welcome_screen(self):
		self.in_welcome_screen = False

		# remove all graphics effects and enable ui
		self.centralwidget.setEnabled(True)
		self.centralwidget.setGraphicsEffect(None)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.welcome_label.setParent(None)
		self.welcome_button_new.setParent(None)
		self.welcome_button_open.setParent(None)
		self.menubar.findChild(QMenu, "menu_edit").setEnabled(True)
		self.action_save.setEnabled(True)
		self.action_save_as.setEnabled(True)
		self.action_export.setEnabled(True)

	def setup_welcome_screen(self, app):
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
		self.welcome_label.setStyleSheet(f"color: {Settings.Gui.PRIMARY_COLOR}; background-color: transparent")

		font_metrics = QFontMetrics(self.welcome_label.font())
		text_width = font_metrics.boundingRect(self.welcome_label.text()).width() + 10
		text_height = font_metrics.boundingRect(self.welcome_label.text()).height()
		self.welcome_label.setFixedSize(text_width, text_height)

		self.welcome_button_new = QPushButton("Neue Datei", app.window)
		self.welcome_button_open = QPushButton("Datei öffnen", app.window)
		self.welcome_button_new.setDefault(True)

		edit_menu = self.menubar.findChild(QMenu, "menu_edit")
		edit_menu.setEnabled(False)
		self.action_save.setEnabled(False)
		self.action_save_as.setEnabled(False)
		self.action_export.setEnabled(False)

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

		settings = Settings.Document.DEFAULT_SETTINGS

		# open saved document settings
		if (QFileInfo(Settings.Document.SETTINGS_FILENAME).exists()):
			with open(Settings.Document.SETTINGS_FILENAME, "r") as f:
				settings = json.load(f)
			if (Settings.Document.DEFAULT_SETTINGS != settings):
				self.save_settings_check_box.setChecked(True)

		self.set_settings(settings)

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
		self.set_settings(Settings.Document.DEFAULT_SETTINGS)
		self.update_voice_combo_boxes(True)

	def set_settings(self, settings: dict):
		self.heading_line_edit.setText(settings["heading"])
		self.sub_heading_line_edit.setText(settings["sub_heading"])
		self.composer_line_edit.setText(settings["composer"])
		self.tempo_line_edit.setText(settings["tempo"])
		self.key_signatures_combo_box.setCurrentIndex(settings["key_signature"])
		self.staves_spin_box.setValue(settings["staves"])
		self.piano_checkbox.setChecked(settings["piano_checkbox"])
		self.time_signature_combo_box.setCurrentIndex(settings["time_signature_combo_box"])

	def get_settings(self):
		settings = {
			"heading": self.heading_line_edit.text(),
			"sub_heading": self.sub_heading_line_edit.text(),
			"composer": self.composer_line_edit.text(),
			"tempo": self.tempo_line_edit.text(),
			"key_signature": self.key_signatures_combo_box.currentIndex(),
			"staves": self.staves_spin_box.value(),
			"piano_checkbox": self.piano_checkbox.isChecked(),
			"time_signature_combo_box": self.time_signature_combo_box.currentIndex(),
		}
		return settings
	
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

		super().__init__([])

		load_fonts()
		# apply the dark theme to the app
		# see <https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html>
		qdarktheme.setup_theme(Settings.Gui.THEME, Settings.Gui.CORNER_SHAPE, Settings.Gui.CUSTOM_COLORS)

		self.document_ui = DocumentUi()

		# status vars
		self.current_file_name = ""
		self.current_file_saved = False
		self.show_warning_box = True
		self.current_page = 0

		# windows
		self.window = MainWindow()
		self.aboutbox = QDialog()
		self.new_doc_dialog = QDialog()

		self.window.resizeEvent = self.window_resize

		# setup uis
		self.ui = App_Ui(self)
		self.aboutbox_ui = Ui_AboutBox()
		self.new_doc_dialog_ui = NewDocumentDialogUI()
		self.aboutbox_ui.setupUi(self.aboutbox)
		self.new_doc_dialog_ui.setupUi(self.new_doc_dialog)

		# remove standard ?-help symbols
		self.new_doc_dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
		self.aboutbox.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

	def set_scene(self, page_index):
		"""page_index must be >= 0"""
		self.current_page = page_index
		self.ui.view.setScene(self.document_ui.pages[self.current_page].qt())

	def window_resize(self, event):
		if (self.ui.in_welcome_screen):
			self.ui.welcome_label.move((self.window.width() - self.ui.welcome_label.width()) / 2, (self.window.height() - self.ui.welcome_label.height()) / 2)
			self.ui.welcome_button_new.move((self.window.width() - self.ui.welcome_button_new.width()) / 2 + self.ui.welcome_button_new.width() / 2 + 10, self.ui.welcome_label.y() + self.ui.welcome_label.height() + 20)
			self.ui.welcome_button_open.move((self.window.width() - self.ui.welcome_button_open.width()) / 2 - self.ui.welcome_button_open.width() / 2 - 10, self.ui.welcome_label.y() + self.ui.welcome_label.height() + 20)
	def end_welcome_screen(self):
		self.window.resizeEvent = None
		self.ui.end_welcome_screen()
