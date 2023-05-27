"""
main.py: ♫ Notensatzprogramm, grundlegende Programmstruktur
"""

from app import App
from ui_misc import UiMiscHandler
from saving import SavingHander
from page_handling import PageHandler
from edit_items import EditScene
from editing import custom_move, unselect_buttons, custom_pressed, setup_edit
from misc import get_abs_path

from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

__author__ = "Noah Weiler"

def main():
	app = App()

	# enable editing logic
	EditScene.custom_move = custom_move
	EditScene.custom_pressed = custom_pressed
	EditScene.custom_setup_edit = setup_edit

	# modules
	ui_misc = UiMiscHandler(app)
	page_handling = PageHandler(app, ui_misc)
	saving = SavingHander(app, page_handling)

	app.window.close_signal.connect(lambda: saving.handle_close_event(app, app.quit))
	app.window.close_signal.connect(lambda: saving.save_document_settings())

	app.document_ui.pages = [page_handling.create_empty_page(1)]
	app.set_scene(0)

	# ui adjustments which need functions of other modules
	ui_misc.apply_zoom()
	ui_misc.update_page_change_buttons_colors()
	ui_misc.update_zoom_buttons_colors()
	app.ui.view.verticalScrollBar().setValue(app.ui.view.verticalScrollBar().minimum())
	app.ui.view.horizontalScrollBar().setValue(app.ui.view.horizontalScrollBar().minimum())

	# menubar actions
	app.ui.action_tutorial.triggered.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(get_abs_path(__file__, "../doc/Anleitung.pdf"))))
	app.ui.action_doc.triggered.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(get_abs_path(__file__, "../doc/Dokumentation.pdf"))))
	app.ui.action_about.triggered.connect(app.aboutbox.show)
	app.ui.action_about.triggered.connect(lambda: unselect_buttons(app))
	app.ui.action_new.triggered.connect(lambda: saving.handle_close_event(app, app.new_doc_dialog.show))
	app.ui.action_new.triggered.connect(lambda: unselect_buttons(app))
	app.ui.action_open.triggered.connect(lambda: saving.handle_close_event(app, saving.open_file))
	app.ui.action_open.triggered.connect(lambda: unselect_buttons(app))
	app.ui.action_save_as.triggered.connect(saving.save_as)
	app.ui.action_save_as.triggered.connect(lambda: unselect_buttons(app))
	app.ui.action_save.triggered.connect(saving.save_file)
	app.ui.action_save.triggered.connect(lambda: unselect_buttons(app))
	app.ui.action_export.triggered.connect(saving.export)
	app.ui.action_export.triggered.connect(lambda: unselect_buttons(app))

	# buttons and other gui elements
	app.ui.zoom_slider.valueChanged.connect(ui_misc.apply_zoom)
	app.ui.zoom_in_button.clicked.connect(ui_misc.zoom_in)
	app.ui.zoom_out_button.clicked.connect(ui_misc.zoom_out)
	app.ui.next_page_button.clicked.connect(page_handling.next_page)
	app.ui.previous_page_button.clicked.connect(page_handling.previous_page)

	for buttons in app.ui.symbols_box_buttons:
		for symbol_button in buttons:
			symbol_button.clicked.connect(lambda: unselect_buttons(app, symbol_button.sender()))

	# welcome screen buttons:
	app.ui.welcome_button_new.clicked.connect(app.new_doc_dialog.show)
	app.ui.welcome_button_open.clicked.connect(saving.open_file)

	# create new document
	app.new_doc_dialog_ui.ok_button.clicked.connect(page_handling.create_new_document)

	# show and execute the app
	app.window.show()
	app.exec()

if __name__ == "__main__":
	main()
