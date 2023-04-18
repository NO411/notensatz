from PyQt5.QtWidgets import QMessageBox, QCheckBox
from PyQt5.QtCore import QPointF

from app import App
from ui_misc import UiMiscHandler
from document import Page, DocumentTextitem, DocumentUi
from notation_system import Bar, TimeSignature, KeySignature, System
from fonts import real_font_size

class PageHandler():
	def __init__(self, app:App, ui_misc:UiMiscHandler):
		self.app = app
		# object which can change app ui
		self.ui_misc = ui_misc

	def create_empty_page(self, page_number: int, new_first_page=False, heading_text="", sub_heading_text="", composer_text="", tempo_text = ""):
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

			heading = DocumentTextitem(True, heading_text, real_font_size(20, Page.HEIGHT), Page.MARGIN, "center", Page.MARGIN, True)
			sub_heading = DocumentTextitem(True, sub_heading_text, real_font_size(12, Page.HEIGHT), heading.y() + heading.boundingRect().height(), "center", Page.MARGIN, False)
			composer = DocumentTextitem(True, composer_text, real_font_size(12, Page.HEIGHT), sub_heading.y() + sub_heading.boundingRect().height(), "right", Page.MARGIN, True)
			tempo = DocumentTextitem(True, tempo_text, real_font_size(12, Page.HEIGHT), composer.y() + composer.boundingRect().height(), "left", 2 * Page.MARGIN, True)

			new_page.scene.addItem(heading)
			new_page.scene.addItem(sub_heading)
			new_page.scene.addItem(composer)
			new_page.scene.addItem(tempo)

			self.app.document_ui.set_heading(heading)
			self.app.document_ui.set_sub_heading(sub_heading)
			self.app.document_ui.set_composer(composer)
			self.app.document_ui.set_tempo(tempo)

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

	def setup_new_document(self, heading, sub_heading, composer, tempo):
		# remove blur effect and enable centralwidget if still in welcome screen
		if (self.app.ui.in_welcome_screen):
			self.app.end_welcome_screen()
		else:
			# disconnect old functions if it is not the first document
			# without, it would lead into unwanted behaviour
			self.app.ui.new_system_button.clicked.disconnect()
			self.app.ui.delete_last_system_button.clicked.disconnect()
			self.app.ui.action_edit_heading.triggered.disconnect()
			self.app.ui.action_edit_subheading.triggered.disconnect()
			self.app.ui.action_edit_composer.triggered.disconnect()
			self.app.ui.action_edit_tempo.triggered.disconnect()

		# create new document with empty (apart from texts) page
		self.app.document_ui = DocumentUi()
		self.app.document_ui.pages = [self.create_empty_page(1, True, heading, sub_heading, composer, tempo)]
		self.app.set_scene(0)
		self.update_page_info_and_button_text()

		self.app.ui.new_system_button.clicked.connect(self.new_system)
		self.app.ui.delete_last_system_button.clicked.connect(self.delete_last_system)
		self.app.ui.action_edit_heading.triggered.connect(lambda : self.edit_text("heading"))
		self.app.ui.action_edit_subheading.triggered.connect(lambda : self.edit_text("sub_heading"))
		self.app.ui.action_edit_composer.triggered.connect(lambda : self.edit_text("composer"))
		self.app.ui.action_edit_tempo.triggered.connect(lambda : self.edit_text("tempo"))

	def create_new_document(self):
		self.setup_new_document(
			self.app.new_doc_dialog_ui.heading_line_edit.text(),
			self.app.new_doc_dialog_ui.sub_heading_line_edit.text(),
			self.app.new_doc_dialog_ui.composer_line_edit.text(),
			self.app.new_doc_dialog_ui.tempo_line_edit.text()
		)

		time_signature_key = self.app.new_doc_dialog_ui.time_signature_combo_box.currentText()
		first_bar = Bar(TimeSignature(TimeSignature.signatures_map[time_signature_key][0], TimeSignature.signatures_map[time_signature_key][1]))
		self.app.document_ui.setup(
			self.app.new_doc_dialog_ui.staves_spin_box.value(),
			first_bar,
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

		self.app.document_ui.pages[-1].scene.addItem(self.app.document_ui.systems[-1])
		self.set_last_system_page()

	def delete_last_system(self):
		if (len(self.app.document_ui.systems) < 2):
			info_box = QMessageBox(QMessageBox.Information, "Information", "Sie können das erste System nicht löschen.", QMessageBox.Yes)
			info_box.setDefaultButton(QMessageBox.Yes)
			info_box.button(QMessageBox.Yes).setText("OK")
			result = info_box.exec_()
			return

		if (self.app.show_warning_box):
			warning_box = QMessageBox(QMessageBox.Information, "System Löschen", "Wollen Sie das letzte System wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
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

	def edit_text(self, text_field):
		# "move" ui to text fields
		self.app.set_scene(0)
		self.app.ui.view.verticalScrollBar().setValue(self.app.ui.view.verticalScrollBar().minimum())
		self.update_page_info_and_button_text()

		if (text_field == "heading"):
			self.app.document_ui.get_heading().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "sub_heading"):
			self.app.document_ui.get_sub_heading().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "composer"):
			self.app.document_ui.get_composer().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum())
		elif (text_field == "tempo"):
			self.app.document_ui.get_tempo().setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().minimum())
