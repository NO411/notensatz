from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
import app

def export_to_pdf(path):
    # fix black border!!
    # maybe with small upscale to hide them

    printer = QPrinter (QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)
    printer.setOrientation(QPrinter.Portrait)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(path + "/test.pdf")

    printer.setPageMargins(0, 0, 0, 0, QPrinter.DevicePixel)
    printer.setColorMode(QPrinter.Color)
    printer.setResolution(300)

    p = QPainter(printer)

    for i, scene in enumerate(app.pages):
        scene.render(p)
        if i != len(app.pages) - 1:
            printer.newPage()
    p.end()

def save():
    export_to_pdf("../src")