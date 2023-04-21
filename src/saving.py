from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QDesktopServices
from PyQt5.QtWidgets import QFileDialog, QGraphicsTextItem
from PyQt5.QtCore import QFileInfo, QUrl

from app import App
from document import DocumentUi
from page_handling import PageHandler
from page import DocumentTextitem

import pickle

class SavingHander():
	def __init__(self, app:App, page_handling:PageHandler):
		self.app = app
		self.page_handling = page_handling

	def export_to_pdf(self, filename):
		# fix black border!!
		# maybe with small upscale to hide them

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
			print(len(page.scene.qt().items()))
			for item in page.scene.qt().items():
				if (type(item) == DocumentTextitem):
					item.remove_highlight()

			page.scene.qt().render(p)
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
		testItem = self.app.document_ui# N_QGraphicsLineItem(QGraphicsLineItem(1, 2, 3, 4))
		with open(file_name, "wb") as f:
			pickle.dump(testItem, f)

	def save_as(self):
		filename, _ = QFileDialog.getSaveFileName(self.app.ui.centralwidget, "Notensatz speichern", self.generate_filename() + "." + self.app.file_extension, "*." + self.app.file_extension)
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

			print(data.heading.qt().toPlainText())

		#self.page_handling.setup_new_document(data["heading"], data["sub_heading"], data["composer"], data["tempo"])
		#self.app.document_ui = pickledata

	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self.app.ui.centralwidget, "Notensatz öffnen", "", "*." + self.app.file_extension)
		if filename:
			self.app.current_file_name = filename
			self.app.current_file_saved = True
			self.open_data(filename)
			# remove blur effect and enable centralwidget if still in welcome screen
			if (self.app.ui.in_welcome_screen):
				self.app.end_welcome_screen()
