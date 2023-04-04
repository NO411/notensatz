from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFileDialog, QGraphicsTextItem
from PyQt5.QtCore import QFileInfo

import app
from document_text import DocumentTextitem
import page_handling

import json

def export_to_pdf(filename):
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

	for i, scene in enumerate(app.document_ui.pages):

		# remove highlights (they would appear gray in the pdf)
		for item in scene.items():
			if (type(item) == DocumentTextitem or type(item) == QGraphicsTextItem):
				item.remove_highlight()

		scene.render(p)
		if i != len(app.document_ui.pages) - 1:
			printer.newPage()
	p.end()

def export():
	filename, _ = QFileDialog.getSaveFileName(app.ui.centralwidget, "Notensatz exportieren", app.document_ui.heading.toPlainText() + ".pdf", "*.pdf")
	if filename:
		export_to_pdf(filename)

def save_data(file_name):
	data = {
		"heading": app.document_ui.heading.toPlainText(),
		"sub_heading": app.document_ui.sub_heading.toPlainText(),
		"composer": app.document_ui.composer.toPlainText(),
		"pages": [],
	}

	for x,_ in enumerate(app.document_ui.pages):
		data["pages"].append({})

	with open(file_name, "w") as file_:
		json.dump(data, file_, indent="\t")

def save_as():
	filename, _ = QFileDialog.getSaveFileName(app.ui.centralwidget, "Notensatz speichern", app.document_ui.heading.toPlainText() + "." + app.file_extension, "*." + app.file_extension)
	if filename:
		save_data(filename)
		app.current_file_name = filename
		app.current_file_saved = True

def save_file():
	if (QFileInfo(app.current_file_name).exists() or app.current_file_saved):
		save_data(app.current_file_name)
	else:
		save_as()

def open_data(filename):
	data = {}
	with open(filename, "r") as file_:
		data = json.load(file_)

	app.document_ui.pages = [page_handling.create_empty_page(True, data["heading"], data["sub_heading"], data["composer"])]
	for x, _ in enumerate(data["pages"]):
		if (x != 0):
			app.document_ui.pages.append(page_handling.create_empty_page(False))

	app.current_page = 0
	app.ui.view.setScene(app.document_ui.pages[0])
	page_handling.update_page_info_and_button_text()
		

def open_file():
	filename, _ = QFileDialog.getOpenFileName(app.ui.centralwidget, "Notensatz öffnen", "", "*." + app.file_extension)
	if filename:
		app.current_file_name = filename
		app.current_file_saved = True
		open_data(filename)
		# remove blur effect and enable centralwidget if still in welcome screen
		if (app.in_welcome_screen):
			app.end_welcome_screen()