from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter, QDesktopServices
from PyQt5.QtWidgets import QFileDialog, QGraphicsTextItem
from PyQt5.QtCore import QFileInfo, QUrl

from app import App
from document import DocumentTextitem
from page_handling import PageHandler

import json

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
			for item in page.scene.items():
				if (type(item) == DocumentTextitem or type(item) == QGraphicsTextItem):
					item.remove_highlight()

			page.scene.render(p)
			if i != len(self.app.document_ui.pages) - 1:
				printer.newPage()
		p.end()

	def generate_filename(self):
		# generate a filename out of the heading and the composer and remove unwanted chars
		ret = self.app.document_ui.heading.toPlainText() + " - " + self.app.document_ui.composer.toPlainText()
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

	def save_data(self,file_name):
		data = {
			"heading": self.app.document_ui.heading.toPlainText(),
			"sub_heading": self.app.document_ui.sub_heading.toPlainText(),
			"composer": self.app.document_ui.composer.toPlainText(),
			"pages": 0,
			"bars": [],
		}

		for _ in self.app.document_ui.pages:
			data["pages"] += 1

		#for bar in self.app.document_ui.bars:
		#	data["bars"].append(bar.to_map())

		with open(file_name, "w") as file_:
			json.dump(data, file_, indent="\t")

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
		data = {}
		with open(filename, "r") as file_:
			data = json.load(file_)

		self.app.document_ui.pages = [self.page_handling.create_empty_page(1, True, data["heading"], data["sub_heading"], data["composer"])]
		for x in range(1, data["pages"]):
			self.app.document_ui.pages.append(self.page_handling.create_empty_page(x + 1))

		self.app.current_page = 0
		self.app.ui.view.setScene(self.app.document_ui.pages[0].scene)
		self.page_handling.update_page_info_and_button_text()

	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self.app.ui.centralwidget, "Notensatz öffnen", "", "*." + self.app.file_extension)
		if filename:
			self.app.current_file_name = filename
			self.app.current_file_saved = True
			self.open_data(filename)
			# remove blur effect and enable centralwidget if still in welcome screen
			if (self.app.ui.in_welcome_screen):
				self.app.end_welcome_screen()