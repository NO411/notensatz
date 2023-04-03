import app

def apply_zoom():
	new_zoom = app.ui.zoom_slider.value() / 100
	app.ui.view.resetTransform()
	app.ui.view.scale(new_zoom, new_zoom)
	app.ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")
	update_zoom_buttons_colors()

def zoom_in():
	app.ui.zoom_slider.setValue(app.ui.zoom_slider.value() + 1)
	apply_zoom()

def zoom_out():
	app.ui.zoom_slider.setValue(app.ui.zoom_slider.value() - 1)
	apply_zoom()

def update_page_change_buttons_colors():
	if (app.current_page == 0):
		app.ui.previous_page_button.setStyleSheet("QPushButton {color: #474a4f}")
		app.ui.previous_page_button.setEnabled(False)
	else:
		app.ui.previous_page_button.setStyleSheet(f"QPushButton {{color: {app.primary_color}}}")
		app.ui.previous_page_button.setEnabled(True)
	if (app.current_page + 1 == len(app.document_ui.pages)):
		app.ui.next_page_button.setStyleSheet("QPushButton {color: #474a4f}")
		app.ui.next_page_button.setEnabled(False)
	else:
		app.ui.next_page_button.setStyleSheet(f"QPushButton {{color: {app.primary_color}}}")
		app.ui.next_page_button.setEnabled(True)

def update_zoom_buttons_colors():
	current_zoom = app.ui.zoom_slider.value()
	if (current_zoom == app.ui.zoom_slider.minimum()):
		app.ui.zoom_out_button.setStyleSheet("QPushButton {color: #474a4f}")
		app.ui.zoom_out_button.setEnabled(False)
	else:
		app.ui.zoom_out_button.setStyleSheet(f"QPushButton {{color: {app.primary_color}}}")
		app.ui.zoom_out_button.setEnabled(True)
	if (current_zoom == app.ui.zoom_slider.maximum()):
		app.ui.zoom_in_button.setStyleSheet("QPushButton {color: #474a4f}")
		app.ui.zoom_in_button.setEnabled(False)
	else:
		app.ui.zoom_in_button.setStyleSheet(f"QPushButton {{color: {app.primary_color}}}")
		app.ui.zoom_in_button.setEnabled(True)

def unselect_buttons(n_class, index):
	for c, _ in enumerate(app.symbols):
		for i, symbol_button in enumerate(app.ui.symbols_box_buttons[c]):
			if (i != index and c != n_class and symbol_button.isChecked()):
				symbol_button.setChecked(False)