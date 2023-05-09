from PyQt5.QtWidgets import QMessageBox, QCheckBox

from app import App
from ui_misc import UiMiscHandler
from edit_items import Page, DocumentTextitem
from document import DocumentUi
from notation_system import KeySignature
from fonts import real_font_size
from settings import Settings
from editing import unselect_buttons

class PageHandler():
	def __init__(self, app: App, ui_misc: UiMiscHandler):
		self.app = app
		# object which can change app ui
		self.ui_misc = ui_misc

	def create_empty_page(self, page_number: int, new_first_page=False, heading_text="", sub_heading_text="", composer_text="", tempo_text=""):
		new_page = Page(page_number)

		if (new_first_page):
			if (heading_text == ""):
				heading_text = "Titel"
			if (sub_heading_text == ""):
				sub_heading_text = "Unterüberschrift"
			if (composer_text == ""):
				composer_text = "Komponist / Arrangeur"
			if (tempo_text == ""):
				tempo_text = "Tempoangabe"

			heading = DocumentTextitem(True, heading_text, real_font_size(20), Settings.Layout.MARGIN, "center", Settings.Layout.MARGIN, True)
			sub_heading = DocumentTextitem(True, sub_heading_text, real_font_size(12), heading.qt().y() + heading.qt().sceneBoundingRect().height(), "center", Settings.Layout.MARGIN, False)
			composer = DocumentTextitem(True, composer_text, real_font_size(12), sub_heading.qt().y() + sub_heading.qt().sceneBoundingRect().height(), "right", Settings.Layout.MARGIN, True)
			tempo = DocumentTextitem(True, tempo_text, real_font_size(12), composer.qt().y() + composer.qt().sceneBoundingRect().height(), "left", 2 * Settings.Layout.MARGIN, True)

			new_page.qt().addItem(heading.qt())
			new_page.qt().addItem(sub_heading.qt())
			new_page.qt().addItem(composer.qt())
			new_page.qt().addItem(tempo.qt())

			self.app.document_ui.heading = heading
			self.app.document_ui.sub_heading = sub_heading
			self.app.document_ui.composer = composer
			self.app.document_ui.tempo = tempo

		return new_page

	def update_page_info_and_button_text(self):
		self.app.ui.current_page_label.setText("Seite " + str(self.app.current_page + 1) + " von " + str(len(self.app.document_ui.pages)))
		self.ui_misc.update_page_change_buttons_colors()

	def new_page(self):
		new_page = self.create_empty_page(len(self.app.document_ui.pages) + 1)

		self.app.document_ui.pages.append(new_page)
		self.app.set_scene(len(self.app.document_ui.pages) - 1)
		self.update_page_info_and_button_text()

	def delete_page(self):
		self.app.set_scene(len(self.app.document_ui.pages) - 2)
		self.app.document_ui.pages.pop(len(self.app.document_ui.pages) - 1)
		self.update_page_info_and_button_text()

	def next_page(self):
		if (self.app.current_page + 1 < len(self.app.document_ui.pages)):
			self.app.set_scene(self.app.current_page + 1)
			self.update_page_info_and_button_text()

	def previous_page(self):
		if (self.app.current_page > 0):
			self.app.set_scene(self.app.current_page - 1)
			self.update_page_info_and_button_text()

	def reconnect(self):
		if (not self.app.ui.in_welcome_screen):
			# disconnect old functions if it is not the first document
			# without, it would lead into unwanted behaviour
			self.app.ui.new_system_button.clicked.disconnect()
			self.app.ui.delete_last_system_button.clicked.disconnect()
			self.app.ui.action_edit_heading.triggered.disconnect()
			self.app.ui.action_edit_subheading.triggered.disconnect()
			self.app.ui.action_edit_composer.triggered.disconnect()
			self.app.ui.action_edit_tempo.triggered.disconnect()

		self.app.ui.new_system_button.clicked.connect(self.new_system)
		self.app.ui.delete_last_system_button.clicked.connect(self.delete_last_system)
		self.app.ui.action_edit_heading.triggered.connect(lambda : self.edit_text("heading"))
		self.app.ui.action_edit_subheading.triggered.connect(lambda : self.edit_text("sub_heading"))
		self.app.ui.action_edit_composer.triggered.connect(lambda : self.edit_text("composer"))
		self.app.ui.action_edit_tempo.triggered.connect(lambda : self.edit_text("tempo"))

	def setup_document(self):
		self.app.set_scene(0)
		self.update_page_info_and_button_text()

		self.reconnect()

		for page in self.app.document_ui.pages:
			page.qt().setup_edit(self.app)

	def setup_new_document(self, heading, sub_heading, composer, tempo):
		# create new document with empty (apart from texts) page
		self.app.document_ui = DocumentUi()
		self.app.document_ui.pages = [self.create_empty_page(1, True, heading, sub_heading, composer, tempo)]
		# also reconnects all actions
		self.setup_document()

		# remove blur effect and enable centralwidget if still in welcome screen
		if (self.app.ui.in_welcome_screen):
			self.app.end_welcome_screen()

	def create_new_document(self):
		self.app.current_file_saved = False
		self.app.current_file_name = ""

		self.setup_new_document(
			self.app.new_doc_dialog_ui.heading_line_edit.text(),
			self.app.new_doc_dialog_ui.sub_heading_line_edit.text(),
			self.app.new_doc_dialog_ui.composer_line_edit.text(),
			self.app.new_doc_dialog_ui.tempo_line_edit.text()
		)

		# setup document (adding first system)
		self.app.document_ui.setup(
			self.app.new_doc_dialog_ui.staves_spin_box.value(),
			self.app.new_doc_dialog_ui.time_signature_combo_box.currentText(),
			self.app.new_doc_dialog_ui.piano_checkbox.isChecked(),
			self.app.new_doc_dialog_ui.get_clefs(),
			KeySignature(self.app.new_doc_dialog_ui.key_signatures_combo_box.currentText())
		)

		# close dialog and eventually save / reset the settings
		self.app.new_doc_dialog.close()
		if (not self.app.new_doc_dialog_ui.save_settings_check_box.isChecked()):
			self.app.new_doc_dialog_ui.reset()
	
	def set_last_system_page(self):
		self.app.set_scene(len(self.app.document_ui.pages) - 1)
		self.update_page_info_and_button_text()

	def new_system(self):
		add_new_page = self.app.document_ui.add_new_system()
		if (add_new_page):
			self.new_page()
			self.app.document_ui.systems[-1].page_index += 1

		self.app.document_ui.pages[-1].qt().addItem(self.app.document_ui.systems[-1].qt())
		self.set_last_system_page()

		unselect_buttons(self.app)

	def delete_last_system(self):
		if (len(self.app.document_ui.systems) < 2):
			info_box = QMessageBox(QMessageBox.Information, "Information", "Sie können das erste System nicht löschen.", QMessageBox.Yes, self.app.window)
			info_box.setDefaultButton(QMessageBox.Yes)
			info_box.button(QMessageBox.Yes).setText("OK")
			result = info_box.exec_()
			return

		if (self.app.show_warning_box):
			warning_box = QMessageBox(QMessageBox.Information, "System Löschen", "Wollen Sie das letzte System wirklich löschen?", QMessageBox.Yes | QMessageBox.No, self.app.window)
			warning_box.setDefaultButton(QMessageBox.Yes)
			warning_box.button(QMessageBox.Yes).setText("Ja")
			warning_box.button(QMessageBox.No).setText("Nein")
			check_box = QCheckBox("Nicht mehr nachfragen", warning_box)
			warning_box.setCheckBox(check_box)

			result = warning_box.exec_()

			if (result == QMessageBox.No):
				return

			if (check_box.isChecked()):
				self.app.show_warning_box = False

		self.app.document_ui.delete_last_system()
		
		# check for an empty last page
		if (self.app.document_ui.systems[-1].page_index != len(self.app.document_ui.pages) - 1):
			self.delete_page()

		self.set_last_system_page()

		unselect_buttons(self.app)

	def edit_text(self, text_field):
		# "move" ui to text fields
		self.app.set_scene(0)
		self.app.ui.view.verticalScrollBar().setValue(self.app.ui.view.verticalScrollBar().minimum())
		self.update_page_info_and_button_text()

		unselect_buttons(self.app)

		if (text_field == "heading"):
			self.app.document_ui.heading.qt().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "sub_heading"):
			self.app.document_ui.sub_heading.qt().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "composer"):
			self.app.document_ui.composer.qt().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum())
		elif (text_field == "tempo"):
			self.app.document_ui.tempo.qt().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().minimum())
