from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QColor

from app import App
from edit_items import EditScene, Musicitem
from symbol_button import SymbolButton
from settings import Settings
from misc import bound_in_intervals, find_overlap_intervals, bound
from notation_system import Rest, Clef, Note, Bar
from fonts import get_specification

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

	# TODO
	# replace all 'free_position' calls with a more specific positioning algorithm

	if (selected_button.group_key == "Noten"):
		if (selected_button.n_symbol < 7):
			note_edit_update(scene, mouse_pos, selected_button)
		elif (selected_button.n_symbol == 7):
			free_position(scene, mouse_pos, selected_button)

	elif (selected_button.group_key == "Pausen"):
		if (selected_button.n_symbol < 7):
			scene.edit_objects[0].change_text(Rest.SYMBOLS[selected_button.n_symbol])

			next_bar_x = get_next_bar_x(scene)

			line = 2
			if (selected_button.n_symbol == 0):
				line = 3

			places = current_bar.find_places([scene.edit_objects[0]], next_bar_x)
			if (len(places) >= 1):
				rest_x = bound_in_intervals(mouse_pos.x(), places)
				scene.edit_objects[0].set_real_pos(rest_x, scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
				scene.successful = True
			else:
				scene.edit_objects[0].change_text()
		elif (selected_button.n_symbol == 7):
			free_position(scene, mouse_pos, selected_button)

	elif (selected_button.group_key == "Artikulation"):
		free_position(scene, mouse_pos, selected_button)
	elif (selected_button.group_key == "Dynamik"):
		free_position(scene, mouse_pos, selected_button)
	elif (selected_button.group_key == "Vorzeichen"):
		free_position(scene, mouse_pos, selected_button)
	elif (selected_button.group_key == "Taktarten"):
		bar_line_x = current_bar.qt().scenePos().x()

		space = True

		for n, stave in enumerate(scene.current_system.staves):
			scene.edit_objects[n].change_text(SymbolButton.SYMBOLS["Taktarten"]["buttons"][selected_button.n_symbol][0])
			intervals = stave.bars[scene.current_bar_n].find_places([scene.edit_objects[n]], get_next_bar_x(scene))
			if ((len(intervals) == 0 or intervals[0][0] != stave.bars[scene.current_bar_n].qt().scenePos().x() + Musicitem.MIN_OBJ_DIST) and not stave.bars[scene.current_bar_n].time_signature_visible):
				space = False
				break

		if (space):
			# time signature positioning
			for n, stave in enumerate(scene.current_system.staves):
				scene.edit_objects[n].set_real_pos(bar_line_x + Musicitem.MIN_OBJ_DIST, stave.qt().scenePos().y() + Musicitem.EM)

			scene.successful = True
		
		else:
			for n, stave in enumerate(scene.current_system.staves):
				scene.edit_objects[n].change_text()
	
	elif (selected_button.group_key == "N-Tolen"):
		scene.edit_objects[0].change_text("tuplet" + str(selected_button.n_symbol + 2))
		scene.edit_objects[0].set_real_pos(
			bound(mouse_pos.x(), Settings.Layout.MARGIN, Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.edit_objects[0].get_real_width()),
			bound(mouse_pos.y(), Settings.Layout.MARGIN - scene.edit_objects[0].get_real_height(), Settings.Layout.HEIGHT - Settings.Layout.MARGIN)
		)
		scene.successful = True

	elif (selected_button.group_key == "Sonstige"):
		# barline
		if (selected_button.n_symbol == 1):
			new_bar = scene.edit_objects[0]
			piano_bar = scene.edit_objects[1]
			new_bar.change_text("barlineSingle")
			piano_bar.change_text("barlineSingle")

			#  positioning
			places_ = []
			start = current_bar.get_start()
			end = Bar.get_end([scene.edit_objects[0]], get_next_bar_x(scene))
			for stave in scene.current_system.staves:
				places_.append(stave.bars[scene.current_bar_n].find_places([scene.edit_objects[0]], get_next_bar_x(scene)))

			places = find_overlap_intervals(places_, [start, end])
			if (len(places) > 0):

				bar_x = bound_in_intervals(mouse_pos.x(), places)

				if (not app.document_ui.with_piano):
					
					new_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_height() / Musicitem.EM))
					new_bar.set_real_pos(bar_x, scene.current_system.get_bottom_y())
					piano_bar.change_text()
					scene.successful = True
				else:
					if (app.document_ui.staves > 2):
						new_bar.change_text("barlineSingle")
						new_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_other_voices_height() / Musicitem.EM))
					else:
						new_bar.change_text()

					# two bar lines, for each bar, one for piano and one for the other voices
					# change pos of the new_bar even if not needed, it will be used by the add_bar algorithm
					new_bar.set_real_pos(bar_x, scene.current_system.get_bottom_other_voices_y())
					piano_bar.qt().setTransform(QTransform().scale(1, scene.current_system.get_piano_height() / Musicitem.EM))
					piano_bar.set_real_pos(bar_x, scene.current_system.get_bottom_y())
					scene.successful = True
					
			else:
				new_bar.change_text()
				piano_bar.change_text()
			
		elif (1 < selected_button.n_symbol < 5):
			scene.edit_objects[0].change_text(Clef.SYMBOLS[selected_button.n_symbol - 2]["smufl_key"])

			next_bar_x = get_next_bar_x(scene)
			
			# determine line to put clef on
			closest_line = scene.current_stave.get_closest_line(mouse_pos, 1)
			dists = []
			for line in Clef.SYMBOLS[selected_button.n_symbol - 2]["lines"]:
				dists.append(abs(line - closest_line))
			
			line = Clef.SYMBOLS[selected_button.n_symbol - 2]["lines"][dists.index(min(dists))]

			places = current_bar.find_places([scene.edit_objects[0]], next_bar_x)
			if (len(places) >= 1):
				clef_x = bound_in_intervals(mouse_pos.x(), places)
				scene.edit_objects[0].set_real_pos(clef_x, scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
				scene.successful = True
			else:
				scene.edit_objects[0].change_text()
		elif (selected_button.n_symbol == 0 or selected_button.n_symbol > 4):
			free_position(scene, mouse_pos, selected_button)
	elif (selected_button.group_key == "Werkzeuge"):
		...

def free_position(scene: EditScene, mouse_pos: QPointF, selected_button: SymbolButton):
	scene.edit_objects[0].change_text(SymbolButton.SYMBOLS[selected_button.group_key]["buttons"][selected_button.n_symbol][0])
	scene.edit_objects[0].set_real_pos(
		bound(mouse_pos.x(), Settings.Layout.MARGIN, Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.edit_objects[0].get_real_width()),
		bound(mouse_pos.y(), Settings.Layout.MARGIN - scene.edit_objects[0].get_real_height(), Settings.Layout.HEIGHT - Settings.Layout.MARGIN)
	)
	scene.successful = True

def note_edit_update(scene: EditScene, mouse_pos: QPointF, selected_button: SymbolButton):
	note = scene.edit_objects[0]
	items = [note]

	# notes positioning
	note.change_text(Note.SYMBOLS[2])
	if (selected_button.n_symbol < 2):
		note.change_text(Note.SYMBOLS[selected_button.n_symbol])

	# add notehead
	# note_x and all relative positions will be updated again
	note_x = 0
	note_y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(scene.current_line)
	note.set_real_pos(note_x, note_y)

	if (selected_button.n_symbol > 0):
		# add stem
		stem = scene.edit_objects[1]
		items.append(stem)

		stem.change_text("stem")
		stem_spec = get_specification("glyphsWithAnchors", "noteheadBlack")
		stem_x = note.get_real_relative_x() + note.get_real_width() - stem.get_real_width()
		stem_y = note_y - Musicitem.spec_to_px(stem_spec["stemUpSE"][1])
		correction = 0.045
		
		# flip stem
		if (scene.current_line >= 2):
			stem_x = note.get_real_relative_x()
			stem_y = note_y - stem.get_real_height() - Musicitem.spec_to_px(stem_spec["stemDownNW"][1])
			correction /= 2
		
		stem.set_real_pos(stem_x + Musicitem.spec_to_px(correction), stem_y)

		# add flag
		if (selected_button.n_symbol > 2):
			flag_y = stem.get_real_relative_y() + stem.get_real_height()
			direction = "Up"

			# flip flag
			if (scene.current_line >= 2):
				direction = "Down"
				flag_y = stem_y

			flag = scene.edit_objects[2]
			items.append(flag)
			flag.change_text(Note.FLAGS[selected_button.n_symbol - 3] + direction)
			flag.set_real_pos(stem_x, flag_y)

	# add leger lines eventually
	# bottom to top
	interval = [int(min(4, scene.current_line)), int(max(0, scene.current_line))]
	o = 3
	# seems like metadata are not 100% correct
	leger_correction = 0.07
	for line in range(interval[0], interval[1] + 1):
		if (line < 0 or line > 4):
			line_type = "legerLine"
			if (selected_button.n_symbol == 0):
				line_type = "legerLineWide"
			leger_line = scene.edit_objects[o]
			items.append(leger_line)
			leger_line.change_text(line_type)
			leger_line_x = note.get_real_relative_x() - (leger_line.get_real_width() - note.get_real_width()) / 2
			leger_line.set_real_pos(leger_line_x + Musicitem.spec_to_px(leger_correction), scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
			o += 1

	# check wether all items would fit together in the bar
	places = scene.current_stave.bars[scene.current_bar_n].find_places(items, get_next_bar_x(scene))

	# reposition everything
	note_x = bound_in_intervals(mouse_pos.x(), places)
	
	if (note_x != None):
		for item in items:
			item.set_real_x(item.get_real_relative_x() + note_x)

		scene.successful = True

	if (len(places) == 0 or note_x == None):
		scene.successful = False
		# clear everything
		for obj in scene.edit_objects:
			obj.change_text()

def edit_pressed(scene: EditScene, mouse_pos: QPointF, app: App, selected_button: SymbolButton):
	if (selected_button is None or scene.successful == False):
		return
	if (selected_button.group_key == "Noten"):
		if (selected_button.n_symbol < 7):
			scene.current_stave.bars[scene.current_bar_n].add_note(scene.edit_objects[0], scene.edit_objects[1], scene.edit_objects[2], [item for item in scene.edit_objects if item.key[:9] == "legerLine"])
		elif (selected_button.n_symbol == 7):
			scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	elif (selected_button.group_key == "Pausen"):
		if (selected_button.n_symbol < 7):
			scene.current_stave.bars[scene.current_bar_n].add_rest(scene.edit_objects[0])
		elif (selected_button.n_symbol == 7):
			scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
		
	# --
	# this will be specified in more detail later
	elif (selected_button.group_key == "Artikulation"):
		scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	elif (selected_button.group_key == "Dynamik"):
		scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	elif (selected_button.group_key == "Vorzeichen"):
		scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	# --
	
	elif (selected_button.group_key == "Taktarten"):
		for n, stave in enumerate(scene.current_system.staves):
			stave.bars[scene.current_bar_n].show_time_signature(SymbolButton.SYMBOLS["Taktarten"]["buttons"][selected_button.n_symbol][1])
	elif (selected_button.group_key == "N-Tolen"):
		scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	elif (selected_button.group_key == "Sonstige"):
		if (selected_button.n_symbol == 1):
			for n, stave in enumerate(scene.current_system.staves):
				stave.add_bar(scene.edit_objects, app.document_ui.staves, n, app.document_ui.with_piano)
		elif (1 < selected_button.n_symbol < 5):
			scene.current_stave.bars[scene.current_bar_n].add_clef(scene.edit_objects[0], selected_button.n_symbol - 2)
		elif (selected_button.n_symbol == 0 or selected_button.n_symbol > 4):
			scene.current_stave.bars[scene.current_bar_n].add_free_item(scene.edit_objects[0])
	elif (selected_button.group_key == "Werkzeuge"):
		...
	
	# remove the selected item from the current pos
	edit_update(scene, mouse_pos, app, selected_button)

def get_next_bar_x(scene: EditScene) -> float:
	next_bar_x = Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.current_system.right_bar_line.get_real_width()
	if (scene.current_bar_n != len(scene.current_stave.bars) - 1):
		next_bar_x = scene.current_stave.bars[scene.current_bar_n + 1].qt().scenePos().x() - scene.current_system.staves[0].bars[scene.current_bar_n + 1].left_bar_line.get_real_width()
	return next_bar_x

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