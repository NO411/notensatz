from new_document import Ui_NewDocumentDialog

class NewDocumentDialogUI(Ui_NewDocumentDialog):
	def setupUi(self, NewDocumentDialog):
		super().setupUi(NewDocumentDialog)
		self.voices_labels = [self.voice_1_label, self.voice_2_label, self.voice_3_label, self.voice_4_label]
		self.voices_combo_boxes = [self.voice_1_combo_box, self.voice_2_combo_box, self.voice_3_combo_box, self.voice_4_combo_box]
		self.staves_spin_box.valueChanged.connect(lambda: self.update_voice_combo_boxes(False))
	
	def update_voice_combo_boxes(self, reset: bool):
		for i in range(1, self.staves_spin_box.maximum() + 1):
			index = i - 1
			if (i > self.staves_spin_box.value()):
				self.voices_labels[index].setEnabled(False)
				self.voices_combo_boxes[index].setEnabled(False)
				self.voices_combo_boxes[index].setCurrentIndex(0)
			else:
				self.voices_labels[index].setEnabled(True)
				self.voices_combo_boxes[index].setEnabled(True)
				if (reset):
					self.voices_combo_boxes[index].setCurrentIndex(0)
	
	def reset(self):
		self.heading_line_edit.setText("")
		self.sub_heading_line_edit.setText("")
		self.composer_line_edit.setText("")
		self.fundamental_beats_spin_box.setValue(4)
		self.note_value_combo_box.setCurrentIndex(1)
		self.key_signatures_combo_box.setCurrentIndex(0)
		self.staves_spin_box.setValue(2)
		self.piano_checkbox.setChecked(False)
		self.update_voice_combo_boxes(True)

	
	def get_clefs(self):
		"""return a lsit of clefs, like "Violinschlüssel", "Bassschlüssel", "Altschlüssel" or "Tenorschlüssel" """
		ret: list[str] = []
		for combo_box in self.voices_combo_boxes:
			if (combo_box.isEnabled()):
				ret.append(combo_box.currentText())
		return ret