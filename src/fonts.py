from PyQt5.QtGui import QFontDatabase
import json

font_metadata = None

def get_symbol(smufl_name):
    return str(chr(int(font_metadata[smufl_name][2:], 16)))

def load_fonts():
    global font_metadata

    # Bravura font, see <https://github.com/steinbergmedia/bravura/releases> and <https://w3c.github.io/smufl/latest/index.html> documentation
    font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/Bravura.otf")
    # Times New Roman font, see <https://freefontsfamily.com/times-new-roman-font-free/#google_vignette>
    # (should be included in Windows anyways)
    text_font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/times new roman.ttf")

    # needed for symbol unicodes
    font_metadata_file = open("../assets/bravura_font/unicodes_list.json")
    font_metadata = json.load(font_metadata_file)
    # example:
    # print(font_metadata["noteHalfUp"])
    font_metadata_file.close()