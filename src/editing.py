from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsItem
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform

from app import App
from edit_items import EditScene, Musicitem
from symbol_button import SymbolButton
from settings import Settings
from misc import bound, bound_in_intervals
from notation_system import Bar

from typing import List

def edit_update(edit_scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	edit_scene.edit_object.change_text()
	if (selected_button is None):
		return

	current_edit_obj = edit_scene.edit_object

	if (selected_button.group_key != "Werkzeuge"):
		current_edit_obj.change_text(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol][0])
	
	edit_scene.current_system = app.document_ui.get_closest_system(mouse_pos, app.current_page)
	edit_scene.current_stave = edit_scene.current_system.get_closest_stave(mouse_pos)
	# just the line number
	edit_scene.current_line = edit_scene.current_stave.get_closest_line(mouse_pos)

	current_edit_obj.qt().setTransform(QTransform().scale(1, 1))
	x_bound = bound(mouse_pos.x(), edit_scene.current_system.staves[0].bars[0].qt().scenePos().x(), Settings.Layout.WIDTH - Settings.Layout.MARGIN)
	if (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1):
			# barline positioning
			current_edit_obj.qt().setTransform(QTransform().scale(1, edit_scene.current_system.get_height() / Musicitem.EM))
			bar_x = get_nearest_possible_pos(edit_scene.current_stave.bars, mouse_pos, Bar.MIN_BAR_DIST)
			
			if (bar_x is None):
				current_edit_obj.change_text()
			else:
				current_edit_obj.setPos(bar_x - current_edit_obj.qt().sceneBoundingRect().width() / 2, edit_scene.current_system.get_bottom_y())

	elif (selected_button.group_key == "Noten" or selected_button.group_key == "Vorzeichen"):
		# notes and accidentals positioning
		y = edit_scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(edit_scene.current_line)
		current_edit_obj.setPos(x_bound, y)

	elif (selected_button.group_key == "Pausen"):
		if (len(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol]) > 2):
			current_edit_obj.change_text(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol][2])
		rest_x = get_nearest_possible_pos(edit_scene.current_stave.bars, mouse_pos, Musicitem.EM / 2)
		line = 2
		if (selected_button.n_symbol == 0):
			line = 3
		current_edit_obj.setPos(rest_x, edit_scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))

def edit_pressed(edit_scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	if (selected_button is None):
		return

	# tools
	...

	# symbols
	if (edit_scene.edit_object.qt().toPlainText() == ""):
		return

	if (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1):
			for n, stave in enumerate(edit_scene.current_system.staves):
				stave.add_bar(edit_scene.edit_object, n == 0)
	
	# remove the selected item from the current pos
	edit_update(edit_scene, mouse_pos, app, selected_button)

def get_nearest_possible_pos(bars: List[Bar], mouse_pos: QPointF, dist: float):
	# keep distance to the other bar lines for a consistent look
	bar_line_intervals = []
	for n, bar in enumerate(bars):
		next_bar_x = 0
		bar_x = bar.qt().scenePos().x()
		
		if (n != len(bars) - 1):
			next_bar_x = bars[n + 1].qt().scenePos().x()
		else:
			next_bar_x = Settings.Layout.WIDTH - Settings.Layout.MARGIN

		if (next_bar_x - bar_x > dist * 2):
			bar_line_intervals.append([bar_x + dist, next_bar_x - dist])
	
	return bound_in_intervals(mouse_pos.x(), bar_line_intervals)

def unselect_buttons(app: App, pressed_button: SymbolButton = None):
	for buttons in app.ui.symbols_box_buttons:
		for button in buttons:
			if (pressed_button is None or (not (button.group_key == pressed_button.group_key and button.n_symbol == pressed_button.n_symbol) and button.isChecked())):
				button.setChecked(False)

	for page in app.document_ui.pages:
		page.qt().edit_object.change_text()

def get_selected_button(app: App) -> SymbolButton:
	selected_button: SymbolButton = None
	for buttons in app.ui.symbols_box_buttons:
		for button in buttons:
			if (button.isChecked()):
				selected_button = button
				break
	return selected_button
					
def custom_move(self: EditScene, event: QGraphicsSceneMouseEvent):
	edit_update(self, event.scenePos(), self.app, get_selected_button(self.app))

def custom_pressed(self: EditScene, event: QGraphicsSceneMouseEvent):
	if (event.button() == Qt.LeftButton):
		edit_pressed(self, event.scenePos(), self.app, get_selected_button(self.app))