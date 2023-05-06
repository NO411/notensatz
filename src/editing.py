from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform

from app import App
from edit_items import EditScene, Musicitem
from symbol_button import SymbolButton
from settings import Settings
from misc import bound

def edit_update(mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	app.document_ui.pages[app.current_page].edit_object.change_text()
	if (selected_button is None):
		return

	if (selected_button.group_key != "Werkzeuge"):
		app.document_ui.pages[app.current_page].edit_object.change_text(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol][0])
	
	current_system = app.document_ui.get_closest_system(mouse_pos, app.current_page)
	current_stave = current_system.get_closest_stave(mouse_pos)
	# just the line number
	current_line = current_stave.get_closest_line(mouse_pos)
	current_edit_obj = app.document_ui.pages[app.current_page].edit_object

	current_edit_obj.qt().setTransform(QTransform().scale(1, 1))
	if (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1):
			current_edit_obj.qt().setTransform(QTransform().scale(1, current_system.get_height() / Musicitem.EM))
			current_edit_obj.setPos(bound(mouse_pos.x(), current_system.qt().x(), Settings.Layout.WIDTH - Settings.Layout.MARGIN), current_system.get_bottom_y())

	if (selected_button.group_key == "Noten" or selected_button.group_key == "Vorzeichen"):
		y = current_stave.qt().sceneBoundingRect().y() + Musicitem.EM - current_line * (Musicitem.EM / 4)
		current_edit_obj.setPos(bound(mouse_pos.x(), current_system.qt().x(), Settings.Layout.WIDTH - Settings.Layout.MARGIN), y)

def edit_pressed(mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	...

def on_button_pressed(app: App, pressed_button: SymbolButton):
	for buttons in app.ui.symbols_box_buttons:
		for button in buttons:
			same_button = button.group_key == pressed_button.group_key and button.n_symbol == pressed_button.n_symbol
			if (not same_button and button.isChecked()):
				button.setChecked(False)
	app.document_ui.pages[app.current_page].edit_object.change_text()

def get_selected_button(app: App) -> SymbolButton:
	selected_button: SymbolButton = None
	for buttons in app.ui.symbols_box_buttons:
			for button in buttons:
				if (button.isChecked()):
					selected_button = button
					break
	return selected_button
					
def custom_move(self: EditScene, event: QGraphicsSceneMouseEvent):
	edit_update(event.scenePos(), self.app, get_selected_button(self.app))

def custom_pressed(self: EditScene, event: QGraphicsSceneMouseEvent):
	if (event.button() == Qt.LeftButton):
		edit_pressed(event.scenePos(), self.app, get_selected_button(self.app))