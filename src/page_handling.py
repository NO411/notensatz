from PyQt5.QtWidgets import QMessageBox, QCheckBox

from app import App
from ui_misc import UiMiscHandler
from document import Page, DocumentTextitem, DocumentUi
from notation_system import Bar, TimeSignature, KeySignature
from fonts import real_font_size

class PageHandler():
	def __init__(self, app:App, ui_misc:UiMiscHandler):
		self.app = app
		# object which can change app ui
		self.ui_misc = ui_misc

	def create_empty_page(self, page_number: int, new_first_page=False, heading_text="", sub_heading_text="", composer_text=""):
		new_page = Page(page_number)

		if (new_first_page):
			if (heading_text == ""):
				heading_text = "Titel"
			if (sub_heading_text == ""):
				sub_heading_text = "Unterüberschrift"
			if (composer_text == ""):
				composer_text = "Komponist / Arrangeur"

			heading = DocumentTextitem(True, heading_text, real_font_size(20, Page.HEIGHT), Page.MARGIN, "center", True)
			sub_heading = DocumentTextitem(True, sub_heading_text, real_font_size(12, Page.HEIGHT), heading.y() + heading.boundingRect().height(), "center", False)
			composer = DocumentTextitem(True, composer_text, real_font_size(12, Page.HEIGHT), sub_heading.y() + sub_heading.boundingRect().height(), "right", True)

			new_page.scene.addItem(heading)
			new_page.scene.addItem(sub_heading)
			new_page.scene.addItem(composer)

			self.app.document_ui.heading = heading
			self.app.document_ui.sub_heading = sub_heading
			self.app.document_ui.composer = composer

			self.app.ui.action_edit_heading.triggered.connect(lambda : self.edit_text("heading"))
			self.app.ui.action_edit_subheading.triggered.connect(lambda : self.edit_text("sub_heading"))
			self.app.ui.action_edit_composer.triggered.connect(lambda : self.edit_text("composer"))
		
		return new_page

	def update_page_info_and_button_text(self):
		self.app.ui.current_page_label.setText("Seite " + str(self.app.current_page + 1) + " von " + str(len(self.app.document_ui.pages)))
		self.ui_misc.update_page_change_buttons_colors()

	def new_page(self):
		self.app.current_page += 1
		new_page = self.create_empty_page(self.app.current_page + 1)

		if (len(self.app.document_ui.pages) == self.app.current_page):
			self.app.document_ui.pages.append(new_page)
		else:
			self.app.document_ui.pages.insert(self.app.current_page, new_page)
		self.app.ui.view.setScene(self.app.document_ui.pages[self.app.current_page].scene)
		self.update_page_info_and_button_text()

		for i, page in enumerate(self.app.document_ui.pages):
			if (i > self.app.current_page):
				page.increase_page_number()

	def delete_page(self):
		if (self.app.current_page == 0):
			info_box = QMessageBox(QMessageBox.Information, "Information", "Sie können die erste Seite nicht komplett löschen, da sie den Titel usw. enthält.", QMessageBox.Yes)
			info_box.setDefaultButton(QMessageBox.Yes)
			info_box.button(QMessageBox.Yes).setText("OK")
			result = info_box.exec_()
			return

		if (self.app.show_warning_box):
			warning_box = QMessageBox(QMessageBox.Information, "Seite Löschen", f"Wollen Sie die Seite {self.app.current_page + 1} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
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

		self.app.document_ui.pages.pop(self.app.current_page)
		self.app.current_page -= 1
		if (self.app.current_page < 0):
			self.app.current_page = 0
		if (len(self.app.document_ui.pages) == 0):
			self.app.document_ui.pages.append(self.create_empty_page(1, True))

		self.app.ui.view.setScene(self.app.document_ui.pages[self.app.current_page].scene)
		self.update_page_info_and_button_text()

		for i, page in enumerate(self.app.document_ui.pages):
			if (i > self.app.current_page):
				page.decrease_page_number()

	def next_page(self):
		if (self.app.current_page + 1 < len(self.app.document_ui.pages)):
			self.app.current_page += 1
			self.app.ui.view.setScene(self.app.document_ui.pages[self.app.current_page].scene)
			self.update_page_info_and_button_text()

	def previous_page(self):
		if (self.app.current_page > 0):
			self.app.current_page -= 1
			self.app.ui.view.setScene(self.app.document_ui.pages[self.app.current_page].scene)
			self.update_page_info_and_button_text()

	def create_new_document(self):
		# disconnect old signals / slots:
		self.app.ui.action_edit_heading.triggered.disconnect()
		self.app.ui.action_edit_subheading.triggered.disconnect()
		self.app.ui.action_edit_composer.triggered.disconnect()

		# remove blur effect and enable centralwidget if still in welcome screen
		if (self.app.ui.in_welcome_screen):
			self.app.end_welcome_screen()

		self.app.current_page = 0
		self.app.document_ui = DocumentUi()
		self.app.document_ui.pages = [self.create_empty_page(1, True, self.app.new_doc_dialog_ui.heading_line_edit.text(), self.app.new_doc_dialog_ui.sub_heading_line_edit.text(), self.app.new_doc_dialog_ui.composer_line_edit.text())]
		self.app.ui.view.setScene(self.app.document_ui.pages[0].scene)
		self.update_page_info_and_button_text()

		time_signature_key = self.app.new_doc_dialog_ui.time_signature_combo_box.currentText()
		first_bar = Bar(TimeSignature(TimeSignature.signatures_map[time_signature_key][0], TimeSignature.signatures_map[time_signature_key][1]))
		self.app.document_ui.setup(
			self.app.new_doc_dialog_ui.staves_spin_box.value(),
			first_bar,
			self.app.new_doc_dialog_ui.piano_checkbox.isChecked(),
			self.app.new_doc_dialog_ui.get_clefs(),
			KeySignature(self.app.new_doc_dialog_ui.key_signatures_combo_box.currentText())
		)

		# close dialog and eventually save the settings
		self.app.new_doc_dialog.close()
		if (not self.app.new_doc_dialog_ui.save_settings_check_box.isChecked()):
			self.app.new_doc_dialog_ui.reset()

	def edit_text(self, text_field):
		# "move" ui to text fields
		self.app.current_page = 0
		self.app.ui.view.setScene(self.app.document_ui.pages[self.app.current_page].scene)
		self.app.ui.view.verticalScrollBar().setValue(self.app.ui.view.verticalScrollBar().minimum())
		self.update_page_info_and_button_text()

		if (text_field == "heading"):
			self.app.document_ui.heading.setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "sub_heading"):
			self.app.document_ui.sub_heading.setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum() / 2)
		elif (text_field == "composer"):
			self.app.document_ui.composer.setFocus()
			self.app.ui.view.horizontalScrollBar().setValue(self.app.ui.view.horizontalScrollBar().maximum())
