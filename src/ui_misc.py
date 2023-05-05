from app import App, SymbolButton
from settings import Settings

class UiMiscHandler():
	enabled_button_stylesheet = "QPushButton {color: " + Settings.Gui.PRIMARY_COLOR + "}"
	disabled_button_stylesheet = "QPushButton {color: " + Settings.Gui.CUSTOM_COLORS["border"] + "}"

	def __init__(self, app:App):
		self.app = app

	# functionality for the zoom buttons and the slider
	def apply_zoom(self):
		new_zoom = self.app.ui.zoom_slider.value() / 100
		self.app.ui.view.resetTransform()
		self.app.ui.view.scale(new_zoom, new_zoom)
		self.app.ui.zoom_label.setText(str(int(new_zoom * 100)) + " %")
		self.update_zoom_buttons_colors()

	def zoom_in(self):
		self.app.ui.zoom_slider.setValue(self.app.ui.zoom_slider.value() + 1)
		self.apply_zoom()

	def zoom_out(self):
		self.app.ui.zoom_slider.setValue(self.app.ui.zoom_slider.value() - 1)
		self.apply_zoom()

	def update_page_change_buttons_colors(self):
		if (self.app.current_page == 0):
			self.app.ui.previous_page_button.setStyleSheet(self.disabled_button_stylesheet)
			self.app.ui.previous_page_button.setEnabled(False)
		else:
			self.app.ui.previous_page_button.setStyleSheet(self.enabled_button_stylesheet)
			self.app.ui.previous_page_button.setEnabled(True)
		if (self.app.current_page + 1 == len(self.app.document_ui.pages)):
			self.app.ui.next_page_button.setStyleSheet(self.disabled_button_stylesheet)
			self.app.ui.next_page_button.setEnabled(False)
		else:
			self.app.ui.next_page_button.setStyleSheet(self.enabled_button_stylesheet)
			self.app.ui.next_page_button.setEnabled(True)

	def update_zoom_buttons_colors(self):
		current_zoom = self.app.ui.zoom_slider.value()
		if (current_zoom == self.app.ui.zoom_slider.minimum()):
			self.app.ui.zoom_out_button.setStyleSheet(self.disabled_button_stylesheet)
			self.app.ui.zoom_out_button.setEnabled(False)
		else:
			self.app.ui.zoom_out_button.setStyleSheet(self.enabled_button_stylesheet)
			self.app.ui.zoom_out_button.setEnabled(True)
		if (current_zoom == self.app.ui.zoom_slider.maximum()):
			self.app.ui.zoom_in_button.setStyleSheet(self.disabled_button_stylesheet)
			self.app.ui.zoom_in_button.setEnabled(False)
		else:
			self.app.ui.zoom_in_button.setStyleSheet(self.enabled_button_stylesheet)
			self.app.ui.zoom_in_button.setEnabled(True)

	# remove selection from selected button if an other button is pressed
	def unselect_buttons(self, button: SymbolButton = None):
		for buttons in self.app.ui.symbols_box_buttons:
			for button_ in buttons:
				if (button is None or not (button_.group_key == button.group_key and button_.n_symbol == button.n_symbol) and button_.isChecked()):
					button_.setChecked(False)
