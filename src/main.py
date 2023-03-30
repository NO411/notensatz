"""
main.py: Notensatzprogramm, grundlegende Programmstruktur
"""

import app
import ui_misc
import saving
import page_handling

__author__ = "Noah Weiler"

def main():
    app.init()
    app.pages = [page_handling.create_empty_page()]
    ui_misc.update_page_change_buttons_colors()
    ui_misc.update_zoom_buttons_colors()

    # object which is needed to render the scene
    # view can change when the scene changes (new page)
    app.ui.view.setScene(app.pages[0])
    ui_misc.apply_zoom()
    app.ui.view.verticalScrollBar().setValue(app.ui.view.verticalScrollBar().minimum())
    app.ui.view.horizontalScrollBar().setValue(app.ui.view.horizontalScrollBar().minimum())

    # menubar actions
    app.ui.action_save.triggered.connect(saving.save)
    app.ui.action_about.triggered.connect(app.aboutbox.show)
    app.ui.action_new.triggered.connect(app.new_doc_dialog.show)
    app.ui.zoom_slider.valueChanged.connect(ui_misc.apply_zoom)
    app.ui.zoom_in_button.clicked.connect(ui_misc.zoom_in)
    app.ui.zoom_out_button.clicked.connect(ui_misc.zoom_out)
    app.ui.new_page_button.clicked.connect(page_handling.new_page)
    app.ui.delete_page_button.clicked.connect(page_handling.delete_page)
    app.ui.next_page_button.clicked.connect(page_handling.next_page)
    app.ui.previous_page_button.clicked.connect(page_handling.previous_page)

    app.window.show()
    app.app.exec()

if __name__ == "__main__":
    main()
