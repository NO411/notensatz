from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QDesktopServices
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QFileInfo, QUrl

from app import App
from document import DocumentUi
from page_handling import PageHandler
from edit_items import DocumentTextitem
from settings import Settings
from editing import unselect_buttons

import pickle
import json

class SavingHander():
	def __init__(self, app:App, page_handling:PageHandler):
		self.app = app
		self.page_handling = page_handling

	def export_to_pdf(self, filename):
		# preparations for printing
		unselect_buttons(self.app)

		printer = QPrinter (QPrinter.HighResolution)
		printer.setPageSize(QPrinter.A4)
		printer.setOrientation(QPrinter.Portrait)
		printer.setOutputFormat(QPrinter.PdfFormat)
		printer.setOutputFileName(filename)

		printer.setPageMargins(0, 0, 0, 0, QPrinter.DevicePixel)
		printer.setColorMode(QPrinter.Color)
		printer.setResolution(300)

		p = QPainter(printer)

		for i, page in enumerate(self.app.document_ui.pages):

			# remove highlights (they would appear gray in the pdf)
			for item in page.qt().items():
				if (type(item) == DocumentTextitem):
					item.remove_highlight()

			page.qt().render(p)
			if i != len(self.app.document_ui.pages) - 1:
				printer.newPage()
		p.end()

	def generate_filename(self):
		# generate a filename out of the heading and the composer and remove unwanted chars
		ret = self.app.document_ui.heading.qt().toPlainText() + " - " + self.app.document_ui.composer.qt().toPlainText()
		forbidden_chars = '\\/:*?"<>|'
		for char in forbidden_chars:
			ret = ret.replace(char, "")

		return ret[:260]

	def export(self):
		filename, _ = QFileDialog.getSaveFileName(self.app.ui.centralwidget, "Notensatz exportieren", self.generate_filename() + ".pdf", "*.pdf")
		if (filename):
			self.export_to_pdf(filename)

			# open pdf in extern viewer, if successfull
			if (QFileInfo(filename).exists()):
				QDesktopServices.openUrl(QUrl.fromLocalFile(filename))

	def save_data(self, file_name):
		with open(file_name, "wb") as f:
			pickle.dump(self.app.document_ui, f)

	def save_as(self):
		filename, _ = QFileDialog.getSaveFileName(self.app.ui.centralwidget, "Notensatz speichern", self.generate_filename() + "." + Settings.Document.FILE_EXTENSION, "*." + Settings.Document.FILE_EXTENSION)
		if filename:
			self.save_data(filename)
			self.app.current_file_name = filename
			self.app.current_file_saved = True

	def save_file(self):
		if (QFileInfo(self.app.current_file_name).exists() or self.app.current_file_saved):
			self.save_data(self.app.current_file_name)
		else:
			self.save_as()

	def open_data(self, filename):
		with open(filename, "rb") as f:
			data: DocumentUi = pickle.load(f)
			self.app.document_ui = data
			self.app.document_ui.reassemble()
			self.page_handling.setup_document()

	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self.app.ui.centralwidget, "Notensatz öffnen", "", "*." + Settings.Document.FILE_EXTENSION)
		if filename:
			self.app.current_file_name = filename
			self.app.current_file_saved = True
			self.open_data(filename)
			# remove blur effect and enable centralwidget if still in welcome screen
			if (self.app.ui.in_welcome_screen):
				self.app.end_welcome_screen()

	def handle_close_event(self, app: App, action):
		if (not self.app.ui.in_welcome_screen):
			close_box = QMessageBox(QMessageBox.Question, "Notensatz", "Wollen Sie das aktuelle Dokument speichern?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, app.window)
			close_box.setDefaultButton(QMessageBox.Yes)
			close_box.button(QMessageBox.Save).setText("Speichern")
			close_box.button(QMessageBox.Discard).setText("Nicht speichern")
			close_box.button(QMessageBox.Cancel).setText("Abbrechen")
			result = close_box.exec_()

			if (result == QMessageBox.Cancel):
				return

			if result == QMessageBox.Save:
				self.save_file()
		
		# e.g. app.quit
		action()

	def save_document_settings(self):
		json_settings = json.dumps(self.app.new_doc_dialog_ui.get_settings(), indent="\t")
		with open(Settings.Document.SETTINGS_FILENAME, "w") as f:
			f.write(json_settings)
