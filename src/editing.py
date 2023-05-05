from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF

from app import App
from edit_items import EditScene
from symbol_button import SymbolButton

def edit_update(mouse_pos: QPointF, app: App):
	app.document_ui.edit_object.setPos(mouse_pos.x(), mouse_pos.y())

def on_button_pressed(app: App, button: SymbolButton):
	if (button.group_key != "Werkzeuge"):
		app.document_ui.edit_object.change_text(SymbolButton.SYMBOLS[button.group_key]["buttons"][button.n_symbol][0])
	else:
		app.document_ui.edit_object.change_text()

def custom_move(self: EditScene, event: QGraphicsSceneMouseEvent):
	edit_update(event.scenePos(), self.app)