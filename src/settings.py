class Settings:
	class Layout:
		# A4 layout
		WIDTH = 2480
		HEIGHT = 3508
		# default margin: ca. 1.54 cm
		# default paper width: 21 cm
		# margin / width = [default margin] / [default paper width]
		# -> margin = width * [default margin] / [default paper width]
		MARGIN = WIDTH * 1.54 / 21
	
	class Symbols:
		FONTSIZE = 24

	class Document:
		DEFAULT_SETTINGS = {
			"heading": "",
			"sub_heading": "",
			"composer": "",
			"tempo": "",
			"key_signature": 0,
			"staves": 2,
			"piano_checkbox": False,
			"time_signature_combo_box": 5,
		}
		SETTINGS_FILENAME = "document_settings.json"
		# nos stands for NOtenSatz
		FILE_EXTENSION = "nos"
	
	class Gui:
		THEME = "dark"
		PRIMARY_COLOR = "#528bff"
		DELETE_COLOR = "#ff528b"
		CUSTOM_COLORS = {
			"primary": PRIMARY_COLOR,
			"background": "#21252b",
			"border": "#474a4f",
			"foreground": "#d7d7d5",
			"scrollbar.background": "#282c34",
			"scrollbarSlider.background": "#3b414d",
			"scrollbarSlider.disabledBackground": "#3b414d",
			"scrollbarSlider.activeBackground": "#4e5563",
			"scrollbarSlider.hoverBackground": "#414855",
		}
		CORNER_SHAPE = "rounded"
