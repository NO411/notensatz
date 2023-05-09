from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QColor

from app import App
from edit_items import EditScene, Musicitem
from symbol_button import SymbolButton
from settings import Settings
from misc import bound_in_intervals
from notation_system import Bar, TimeSignature

from typing import List

def setup_edit(self: EditScene, app: App):
	self.app = app

	for i in range(20):
		self.edit_objects.append(Musicitem("", QColor(Settings.Gui.PRIMARY_COLOR)))
		self.addItem(self.edit_objects[i].qt())
		self.edit_objects[i].qt().setZValue(1)

def reset_edit_objects(scene: EditScene):
	# reset edit object(s)
	for obj in scene.edit_objects:
		obj.change_text()
		obj.qt().setTransform(QTransform().scale(1, 1))

def edit_update(scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	reset_edit_objects(scene)

	if (selected_button is None):
		return
	
	scene.current_system = app.document_ui.get_closest_system(mouse_pos, app.current_page)
	scene.current_stave = scene.current_system.get_closest_stave(mouse_pos)
	# just the line number
	scene.current_line = scene.current_stave.get_closest_line(mouse_pos)
	scene.current_bar_n = scene.current_system.get_closest_bar_n(mouse_pos)

	if (selected_button.group_key == "Sonstige"):
		# barline
		if (selected_button.n_symbol == 1):
			#  positioning
			bar_x = get_nearest_possible_pos(scene.current_stave.bars, mouse_pos, Bar.MIN_BAR_DIST)
			
			if (bar_x != None):
				new_bar = scene.edit_objects[0]
				new_bar.change_text("barlineSingle")
				new_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_height() / Musicitem.EM))
				new_bar.setPos(bar_x - new_bar.qt().sceneBoundingRect().width() / 2, scene.current_system.get_bottom_y())

	elif (selected_button.group_key == "Noten" or selected_button.group_key == "Vorzeichen"):
		# notes and accidentals positioning
		#y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(scene.current_line)
		#x_bound = get_nearest_possible_pos(scene.current_stave.bars, mouse_pos, Musicitem.EM / 2)
		#current_edit_obj.setPos(x_bound, y)
		...
	elif (selected_button.group_key == "Pausen"):
		#if (len(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol]) > 2):
		#	current_edit_obj.change_text(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol][2])
		#rest_x = get_nearest_possible_pos(scene.current_stave.bars, mouse_pos, Musicitem.EM / 2)
		#line = 2
		#if (selected_button.n_symbol == 0):
		#	line = 3
		#current_edit_obj.setPos(rest_x, scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
		...
	elif (selected_button.group_key == "Taktarten"):
		bar_line_x = scene.current_system.staves[0].bars[scene.current_bar_n].qt().scenePos().x()

		# time signature positioning
		for n, stave in enumerate(scene.current_system.staves):
			scene.edit_objects[n].change_text(SymbolButton.SYMBOLS["Taktarten"]["buttons"][selected_button.n_symbol][0])
			scene.edit_objects[n].setPos(bar_line_x + TimeSignature.BAR_LINE_DISTANCE, stave.qt().scenePos().y() + Musicitem.EM)

def edit_pressed(scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	if (selected_button is None):
		return

	# tools
	...

	# symbols
	if (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1 and scene.edit_objects[0].qt().toPlainText() != ""):
			for n, stave in enumerate(scene.current_system.staves):
				stave.add_bar(scene.edit_objects[0], n == 0)

	elif (selected_button.group_key == "Taktarten"):
		for n, stave in enumerate(scene.current_system.staves):
			stave.bars[scene.current_bar_n].show_time_signature(SymbolButton.SYMBOLS["Taktarten"]["buttons"][selected_button.n_symbol][1])
	
	# remove the selected item from the current pos
	edit_update(scene, mouse_pos, app, selected_button)

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
		reset_edit_objects(page.qt())

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