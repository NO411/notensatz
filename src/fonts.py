from PyQt5.QtGui import QFontDatabase
from json import load
from typing import List, Union
from settings import Settings

# global jsons
font_metadata = None
glyphnames = None
icons = None


def get_unicode(smufl_name: str) -> int:
    return int(glyphnames[smufl_name]["codepoint"][2:], 16)


def unicode_to_string(u: int):
    return str(chr(u))


def get_symbol(smufl_name: Union[str, List[str]]):
    ret = ""
    if (type(smufl_name) == str):
        ret = unicode_to_string(get_unicode(smufl_name))
    else:
        for part in smufl_name:
            ret += str(chr(get_unicode(part)))
    return ret


def get_specification(key1, key2):
    if (key1 in font_metadata):
        if (key2 in font_metadata[key1]):
            return font_metadata[key1][key2]
    return None


def get_icon(key: str):
    return str(chr(int(icons[key]["unicode"], 16)))


def load_fonts():
    global font_metadata, glyphnames, icons

    # Bravura font, see <https://github.com/steinbergmedia/bravura/releases> and <https://w3c.github.io/smufl/latest/index.html> documentation
    QFontDatabase().addApplicationFont("assets/fonts/bravura/otfs/Bravura.otf")
    # Times New Roman font, see <https://freefontsfamily.com/times-new-roman-font-free/#google_vignette>
    # (should be included in Windows anyways)
    QFontDatabase().addApplicationFont("assets/fonts/times_new_roman/otfs/times new roman.ttf")

    # Font Awesome 6, see <https://fontawesome.com/download>
    QFontDatabase().addApplicationFont("assets/fonts/fontawesome/otfs/Font Awesome Solid.otf")

    # json file for specifications like measurements
    with open("assets/fonts/bravura/metadata/bravura_metadata.json", "r") as f:
        font_metadata = load(f)

    # needed for symbol unicodes
    with open("assets/fonts/bravura/metadata/glyphnames.json", "r") as f:
        glyphnames = load(f)

    with open("assets/fonts/fontawesome/metadata/icons.json", "r") as f:
        icons = load(f)


# get em, which all other specifications depend on
def get_one_em(pt: float):
    # physical page height in inches
    height = 11.69
    # number of pixels / physical size in inches
    dpi = Settings.Layout.HEIGHT / height

    # 72pt = 1inch
    return pt * (dpi / 72)


# converts font sizes to real font sizes on a real A4 page
def real_font_size(pt: float):
    # physical page height in inches
    height = 11.69
    # number of pixels / physical size in inches
    dpi = Settings.Layout.HEIGHT / height

    pixels = get_one_em(pt)

    # calculate the real font size for A4 page
    return pixels * (Settings.Layout.HEIGHT / height) / dpi / 1.333
