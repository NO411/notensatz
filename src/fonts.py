from PyQt5.QtGui import QFontDatabase
from json import load

# global jsons
font_metadata = None
glyphnames = None

def get_unicode(smufl_name):
	return int(glyphnames[smufl_name]["codepoint"][2:], 16)

def get_symbol(smufl_name):
	return str(chr(get_unicode(smufl_name)))

def get_specification(key1, key2):
	return font_metadata[key1][key2]

def load_fonts():
	global font_metadata, glyphnames

	# Bravura font, see <https://github.com/steinbergmedia/bravura/releases> and <https://w3c.github.io/smufl/latest/index.html> documentation
	font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/Bravura.otf")
	# Times New Roman font, see <https://freefontsfamily.com/times-new-roman-font-free/#google_vignette>
	# (should be included in Windows anyways)
	text_font_loaded = QFontDatabase().addApplicationFont("../assets/bravura_font/redist/otf/times new roman.ttf")

	# json file for specifications like measurements
	font_metadata_file = open("../assets/bravura_font/redist/bravura_metadata.json")
	font_metadata = load(font_metadata_file)
	font_metadata_file.close()

	# needed for symbol unicodes
	glyphnames_file = open("glyphnames.json")
	glyphnames = load(glyphnames_file)
	# example:
	# print(glyphnames["noteHalfUp"])
	glyphnames_file.close()

# get em, which all other specifications depend on
def get_one_em(pt: float, pixel_height: int):
	# physical page height in inches
	height = 11.69
	# number of pixels / physical size in inches
	dpi = pixel_height / height
    
	# 72pt = 1inch
	return pt * (dpi / 72)

# converts font sizes to real font sizes on a real A4 page
def real_font_size(pt: float, pixel_height: int):
	# physical page height in inches
	height = 11.69
	# number of pixels / physical size in inches
	dpi = pixel_height / height

	pixels = get_one_em(pt, pixel_height)
    
    # calculate the real font size for A4 page
	return pixels * (pixel_height / height) / dpi / 1.333
