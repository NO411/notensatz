from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QColor

from app import App
from edit_items import EditScene, Musicitem
from symbol_button import SymbolButton
from settings import Settings
from misc import bound_in_intervals, bound
from notation_system import Bar, Rest

from typing import List

def setup_edit(self: EditScene, app: App):
	self.app = app

	for i in range(20):
		self.edit_objects.append(Musicitem("", QColor(Settings.Gui.PRIMARY_COLOR)))
		self.addItem(self.edit_objects[i].qt())
		self.edit_objects[i].qt().setZValue(1)

def reset_edit_objects(scene: EditScene):
	scene.successful = False
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
	scene.current_bar_n = scene.current_stave.get_closest_bar_n(mouse_pos)
	# current bar of the current stave
	current_bar = scene.current_stave.bars[scene.current_bar_n]
	# just the line number
	scene.current_line = scene.current_stave.get_closest_line(mouse_pos)

	if (selected_button.group_key == "Sonstige"):
		# barline
		if (selected_button.n_symbol == 1):
			#  positioning
			bar_x = get_nearest_possible_pos(scene.current_stave.bars, mouse_pos, Musicitem.MIN_OBJ_DIST)
			
			if (bar_x != None):
				new_bar = scene.edit_objects[0]
				if (not app.document_ui.with_piano):
					new_bar.change_text("barlineSingle")
					new_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_height() / Musicitem.EM))
					new_bar.set_real_pos(bar_x, scene.current_system.get_bottom_y())

					scene.successful = True
				else:
					if (app.document_ui.staves > 2):
						new_bar.change_text("barlineSingle")
						new_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_other_voices_height() / Musicitem.EM))

					# two bar lines, for each bar, one for piano and one for the other voices
					# change pos of the new_bar even if not needed, it will be used by the add_bar algorithm
					new_bar.set_real_pos(bar_x, scene.current_system.get_bottom_other_voices_y())

					piano_bar = scene.edit_objects[1]
					piano_bar.change_text("barlineSingle")
					piano_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_piano_height() / Musicitem.EM))
					piano_bar.set_real_pos(bar_x, scene.current_system.get_bottom_y())

					scene.successful = True

	elif (selected_button.group_key == "Noten"):
		# notes positioning
		#y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(scene.current_line)
		#x_bound = get_nearest_possible_pos(scene.current_stave.bars, mouse_pos, Musicitem.EM / 2)
		#current_edit_obj.setPos(x_bound, y)
		...
	elif (selected_button.group_key == "Vorzeichen"):
		...
	elif (selected_button.group_key == "Pausen"):
		if (selected_button.n_symbol <= 6):
			scene.edit_objects[0].change_text(Rest.SYMBOLS[selected_button.n_symbol])

			next_bar_x = Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.current_system.right_bar_line.get_real_width()
			if (scene.current_bar_n != len(scene.current_stave.bars) - 1):
				next_bar_x = scene.current_stave.bars[scene.current_bar_n + 1].qt().scenePos().x() - scene.current_system.staves[0].bars[scene.current_bar_n + 1].left_bar_line.get_real_width()

			line = 2
			if (selected_button.n_symbol == 0):
				line = 3

			places = current_bar.find_places(scene.edit_objects[0], next_bar_x)
			if (len(places) >= 1):
				rest_x = bound_in_intervals(mouse_pos.x(), places)
				scene.edit_objects[0].set_real_pos(rest_x, scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
				scene.successful = True

	elif (selected_button.group_key == "Taktarten"):
		bar_line_x = current_bar.qt().scenePos().x()

		# time signature positioning
		for n, stave in enumerate(scene.current_system.staves):
			scene.edit_objects[n].change_text(SymbolButton.SYMBOLS["Taktarten"]["buttons"][selected_button.n_symbol][0])
			scene.edit_objects[n].set_real_pos(bar_line_x + Musicitem.MIN_OBJ_DIST, stave.qt().scenePos().y() + Musicitem.EM)

		scene.successful = True

def edit_pressed(scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	if (selected_button is None or scene.successful == False):
		return

	# tools
	...

	# symbols
	if (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1 and scene.edit_objects[0].qt().toPlainText() != ""):
			for n, stave in enumerate(scene.current_system.staves):
				stave.add_bar(scene.edit_objects, app.document_ui.staves, n, app.document_ui.with_piano)

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