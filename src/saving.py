from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFileDialog, QGraphicsTextItem
from PyQt5.QtCore import Qt

import app
from document_text import DocumentTextitem

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

    # remove highlights (they would appear gray in the pdf)
    for scene in app.document_ui.pages:
        for item in scene.items():
            if (type(item) == DocumentTextitem or type(item) == QGraphicsTextItem):
                item.remove_highlight()

    for i, scene in enumerate(app.document_ui.pages):
        scene.render(p)
        if i != len(app.document_ui.pages) - 1:
            printer.newPage()
    p.end()

def export():
    filename, _ = QFileDialog.getSaveFileName(app.ui.centralwidget, "Notensatz exportieren", "notensatz.pdf", "*.pdf")
    if filename:
        export_to_pdf(filename)