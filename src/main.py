"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

# pyqt5 imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrinter

# window / dialog imports
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog

# other imports
# from <https://pypi.org/project/pyqtdarktheme/>
import qdarktheme
import json

__author__ = "Noah Weiler"

# symbols that will be implemented
# map of the symbols shown on the buttons in the symbols box
# indexes MUST match with the indexes in the designer
symbols = [
    # notes
    [# [unicode key, tooltip text]
        ["noteWhole", "ganze Note"],
        ["noteHalfUp", "halbe Note"],
        ["noteQuarterUp", "viertel Note"],
        ["note8thUp", "achtel Note"],
        ["note16thUp", "sechszehntel Note"],
        ["note32ndUp", "zweiunddreißigstel Note"],
        ["note64thUp", "vierundsechszigstel Note"],
        ["metAugmentationDot", "Punktierung"],
    ],
    # articulation
    [
        ["articAccentAbove", "Akzent"],
        ["articStaccatoAbove", "Staccato"],
        ["articTenutoAbove", "Tenuto"],
        ["keyboardPedalPed", "Pedal"],
        ["keyboardPedalUp", "Pedal loslassen"],
    ],
    # dynamics
    [
        ["dynamicMP", "mezzopiano"],
        ["dynamicPiano", "piano"],
        ["dynamicPP", "pianissimo"],
        ["dynamicPPP", "pianopianissimo"],
        ["dynamicPF", "pianoforte"],
        ["dynamicFortePiano", "fortepiano"],
        ["dynamicMF", "mezzoforte"],
        ["dynamicForte", "forte"],
        ["dynamicFF", "fortissimo"],
        ["dynamicFFF", "fortefortissimo"],
        ["dynamicCrescendoHairpin", "crescendo"],
        ["dynamicDiminuendoHairpin", "decrescendo"],
    ],
    # rests
    [
        ["restWholeLegerLine", "ganze Pause"],
        ["restHalfLegerLine", "halbe pause"],
        ["restQuarter", "viertel Pause"],
        ["rest8th", "achtel Pause"],
        ["rest16th", "sechszehntel Pause"],
        ["rest32nd", "zweiunddreißigstel Pause"],
        ["rest64th", "vierundsechszigstel Pause"],
        ["metAugmentationDot", "Punktierung"],
    ],
    # accidentals
    [
        ["accidentalSharp", "Kreuz"],
        ["accidentalFlat", "b"],
        ["accidentalDoubleSharp", "Doppelkreuz"],
        ["accidentalNatural", "Auflösung"],
        ["accidentalDoubleFlat", "doppel b"],
    ],
    # time signatures
    [
        ["timeSigCommon", "Viervierteltakt"],
        ["timeSigCutCommon", "Zweivierteltakt"],
    ],
    # misc
    [
        ["repeatRight", "Wiederholung"],
        ["gClef", "Violinchlüssel"],
        ["cClef", "C-Schlüssel"],
        ["fClef", "Bassschlüssel"],
    ],
]


def get_symbol(smufl_name):
    return str(chr(int(font_metadata[smufl_name][2:], 16)))

def apply_zoom():
    new_zoom = ui.zoom_slider.value() / 100
    ui.view.resetTransform()
    ui.view.scale(new_zoom, new_zoom)
    ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")
    update_zoom_buttons_colors()

def zoom_in():
    ui.zoom_slider.setValue(ui.zoom_slider.value() + 1)
    apply_zoom()

def zoom_out():
    ui.zoom_slider.setValue(ui.zoom_slider.value() - 1)
    apply_zoom()

def create_empty_page():
    new_page = QGraphicsScene(0, 0, width, height)
    # white background
    rect = QGraphicsRectItem(0, 0, width, height)
    rect.setBrush(QBrush(Qt.white))
    new_page.addItem(rect)
    return new_page

def update_page_info_and_button_text():
    ui.current_page_label.setText("Seite " + str(current_page + 1) + " von " + str(len(pages)))
    update_page_change_buttons_colors()

def new_page():
    global current_page
    new_page = create_empty_page()
    if (len(pages) == current_page + 1):
        pages.append(new_page)
    else:
        pages.insert(current_page + 1, new_page)
    current_page += 1
    ui.view.setScene(pages[current_page])
    update_page_info_and_button_text()

show_warning_box = True
def delete_page():
    global current_page, show_warning_box

    if (show_warning_box):
        warning_box = QMessageBox(QMessageBox.Warning, "Seite Löschen", f"Wollen Sie die Seite {current_page + 1} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        warning_box.setDefaultButton(QMessageBox.Yes)
        warning_box.button(QMessageBox.Yes).setText("Ja")
        warning_box.button(QMessageBox.No).setText("Nein")
        check_box = QCheckBox("Nicht mehr nachfragen", warning_box)
        warning_box.setCheckBox(check_box)

        result = warning_box.exec_()

        if (result == QMessageBox.No):
            return

        if (check_box.isChecked()):
            show_warning_box = False


    pages.pop(current_page)
    current_page -= 1
    if (current_page < 0):
        current_page = 0
    if (len(pages) == 0):
        pages.append(create_empty_page())

    ui.view.setScene(pages[current_page])
    update_page_info_and_button_text()

def next_page():
    global current_page
    if (current_page + 1 < len(pages)):
        current_page += 1
        ui.view.setScene(pages[current_page])
        update_page_info_and_button_text()

def previous_page():
    global current_page
    if (current_page > 0):
        current_page -= 1
        ui.view.setScene(pages[current_page])
        update_page_info_and_button_text()

def update_page_change_buttons_colors():
    if (current_page == 0):
        ui.previous_page_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.previous_page_button.setEnabled(False)
    else:
        ui.previous_page_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.previous_page_button.setEnabled(True)
    if (current_page + 1 == len(pages)):
        ui.next_page_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.next_page_button.setEnabled(False)
    else:
        ui.next_page_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.next_page_button.setEnabled(True)

def update_zoom_buttons_colors():
    current_zoom = ui.zoom_slider.value()
    if (current_zoom == ui.zoom_slider.minimum()):
        ui.zoom_out_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.zoom_out_button.setEnabled(False)
    else:
        ui.zoom_out_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.zoom_out_button.setEnabled(True)
    if (current_zoom == ui.zoom_slider.maximum()):
        ui.zoom_in_button.setStyleSheet("QPushButton {color: #474a4f}")
        ui.zoom_in_button.setEnabled(False)
    else:
        ui.zoom_in_button.setStyleSheet(f"QPushButton {{color: {primary_color}}}")
        ui.zoom_in_button.setEnabled(True)

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

    for i, scene in enumerate(pages):
        scene.render(p)
        if i != len(pages) - 1:
            printer.newPage()
    p.end()

def save():
    export_to_pdf("../src")

qdarktheme.enable_hi_dpi()
app = QApplication([])

# Bravura font, see <https://github.com/steinbergmedia/bravura/releases> and <https://w3c.github.io/smufl/latest/index.html> documentation
font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/Bravura.otf")
# Times New Roman font, see <https://freefontsfamily.com/times-new-roman-font-free/#google_vignette>
# (should be included in Windows anyways)
text_font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/times new roman.ttf")

# check wether font loaded
if font_loaded == -1:
    print("Failed to load musicfont")

# needed for symbol unicodes
font_metadata_file = open("../assets/bravura_font/unicodes_list.json")
font_metadata = json.load(font_metadata_file)
# example:
# print(font_metadata["noteHalfUp"])
font_metadata_file.close()

# apply the dark theme to the app
# see <https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html>
primary_color = "#528bff"
qdarktheme.setup_theme(
    custom_colors = {
        "primary": primary_color,
        "background": "#21252b",
        "border": "#474a4f",
        "foreground": "#d7d7d5",
        "scrollbar.background": "#282c34",
        "scrollbarSlider.background": "#3b414d",
        "scrollbarSlider.disabledBackground": "#3b414d",
        "scrollbarSlider.activeBackground": "#4e5563",
        "scrollbarSlider.hoverBackground": "#414855",
    },
    corner_shape="rounded"
)

window = QMainWindow()
aboutbox = QDialog()
new_doc_dialog = QDialog()

ui = Ui_MainWindow()
ui.setupUi(window)

# A4 layout
width = 2480
height = 3508
start_zoom = 0.3

# table of pages (QGraphicsScene)
pages = [create_empty_page()]
current_page = 0
update_page_change_buttons_colors()
update_zoom_buttons_colors()

font = QFont("Bravura", 100)
text_item = QGraphicsTextItem(str(chr(int("1D11A", 16))*10 + str(chr(int("E030", 16)))), parent=None)
text_item.setDefaultTextColor(Qt.black)
text_item.setFont(font)
pages[0].addItem(text_item)

text_item = QGraphicsTextItem(str(chr(int("E1D7", 16))) + str(chr(int("EC46", 16))) + str(chr(int("EC62", 16))) + str(chr(int("E4E5", 16))) + str(chr(int("E0A2", 16))), parent=None)
text_item.setDefaultTextColor(Qt.black)
text_item.setFont(font)
pages[0].addItem(text_item)

text_item = QGraphicsTextItem("Titel hinzufügen")
text_item.setFont(QFont("Times New Roman", 150))
text_item.setDefaultTextColor(Qt.black)
pages[0].addItem(text_item)
text_item.setPos(pages[0].sceneRect().width() / 2.0 - 100, 100)
text_item.setTextInteractionFlags(Qt.TextEditorInteraction)


# object which is needed to render the scene
# view can change when the scene changes (new page), but setWidget will never be called again
ui.view.setScene(pages[0])
ui.zoom_slider.setValue(int(start_zoom * 100))
apply_zoom()
ui.view.verticalScrollBar().setValue(ui.view.verticalScrollBar().minimum())
ui.view.horizontalScrollBar().setValue(ui.view.horizontalScrollBar().minimum())


################
# experimental #
################

ui.symbols_box_buttons = []
ui.box_tabs_layouts = []

for i, symbol_class in enumerate(symbols):
    ui.symbols_box_buttons.insert(0, [])

    tab_widget = ui.symbols_box.widget(i)
    ui.box_tabs_layouts.insert(i, QHBoxLayout(tab_widget))
    ui.box_tabs_layouts[i].setContentsMargins(3, 3, 3, 3)
    ui.box_tabs_layouts[i].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    for name in symbol_class:
        # name[0]: unicode key
        # name[1]: tooltip text
        box_button = QPushButton(tab_widget)
        box_button.setObjectName(name[0] + "Button")
        box_button.setFixedSize(35, 60)
        box_button.setFlat(True)
        box_button.setCheckable(True)
        box_button.setToolTip(name[1])
        box_button.setStyleSheet("QToolTip {color: black}")
        label = QLabel(get_symbol(name[0]), box_button)
        font = QFont("Bravura", 20)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter)
        label.setGeometry(0, -20, box_button.width(), 100)

        ui.box_tabs_layouts[i].addWidget(box_button)
        ui.symbols_box_buttons[i].append(box_button)

################

ui.zoom_out_button.setFixedWidth(ui.zoom_out_button.height())

# setup dialog ui
aboutbox_ui = Ui_AboutBox()
aboutbox_ui.setupUi(aboutbox)
new_doc_dialog_ui = Ui_NewDocumentDialog()
new_doc_dialog_ui.setupUi(new_doc_dialog)

# menubar actions
ui.action_save.triggered.connect(save)
ui.action_about.triggered.connect(aboutbox.show)
ui.action_new.triggered.connect(new_doc_dialog.show)
ui.zoom_slider.valueChanged.connect(apply_zoom)
ui.zoom_in_button.clicked.connect(zoom_in)
ui.zoom_out_button.clicked.connect(zoom_out)
ui.new_page_button.clicked.connect(new_page)
ui.delete_page_button.clicked.connect(delete_page)
ui.next_page_button.clicked.connect(next_page)
ui.previous_page_button.clicked.connect(previous_page)

window.show()
app.exec()
