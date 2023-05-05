from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF

from app import App
from edit_items import EditScene

def edit_update(mouse_pos: QPointF, app: App):
	app.document_ui.edit_object.setPos(mouse_pos.x(), mouse_pos.y())

def custom_move(self: EditScene, event: QGraphicsSceneMouseEvent):
	edit_update(event.scenePos(), self.app)