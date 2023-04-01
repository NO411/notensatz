from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

# from <https://pypi.org/project/pyqtdarktheme/>
import qdarktheme

# window / dialog imports
from mainwindow import Ui_MainWindow
from aboutbox import Ui_AboutBox
from new_document import Ui_NewDocumentDialog

# intern imports
from fonts import load_fonts, get_symbol

class DocumentUi:
    def __init__(self):
        # table of QGraphicsScenes
        self.pages = None

        # references of the objects stored in the scene to be able to access them
        # because it is not always possible to determine the index of the item in the pages[x].items() list
        self.title = None
        self.composer = None

app = None
document_ui = None

symbols = None
show_warning_box = None
current_page = None
# A4 layout
width = None
height = None
start_zoom = None
margin = None

primary_color = None

window = None
aboutbox = None
new_doc_dialog = None
ui = None

def init_symbol_buttons():
    global ui, symbols
    # setup symbol buttons
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

# will be called in main.py
def init():
    global symbols, show_warning_box, current_page, width, height, start_zoom, primary_color, app, window, aboutbox, new_doc_dialog, ui, document_ui, margin

    qdarktheme.enable_hi_dpi()
    
    app = QApplication([])

    load_fonts()
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

    document_ui = DocumentUi()
    document_ui.pages = []

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
    show_warning_box = True
    current_page = 0
    # A4 layout
    width = 2480
    height = 3508
    start_zoom = 0.3
    # default margin: ca. 1.54 cm
    # default paper width: 21 cm
    # margin / width = [default margin] / [default paper width]
    # -> margin = width * [default margin] / [default paper width]
    margin = width * 1.54 / 21

    window = QMainWindow()
    aboutbox = QDialog()
    new_doc_dialog = QDialog()

    ui = Ui_MainWindow()
    ui.setupUi(window)

    # other ui setups
    # (seperately to not get overriden by the pyqt5 designer...)
    ui.zoom_slider.setValue(int(start_zoom * 100))
    ui.zoom_out_button.setFixedWidth(ui.zoom_out_button.height())
    ui.symbols_box_buttons = []
    ui.box_tabs_layouts = []

    # setup dialog ui
    aboutbox_ui = Ui_AboutBox()
    aboutbox_ui.setupUi(aboutbox)
    new_doc_dialog_ui = Ui_NewDocumentDialog()
    new_doc_dialog_ui.setupUi(new_doc_dialog)

    init_symbol_buttons()