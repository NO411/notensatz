from PyQt5.QtWidgets import QGraphicsSceneMouseEvent
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QTransform, QColor

from app import App
from edit_items import EditScene
from symbol_button import SymbolButton
from settings import Settings
from misc import bound_in_intervals, find_overlap_intervals, bound
from notation_system import Musicitem, MusicitemGroup, Rest, Clef, Note, Bar
from fonts import get_specification

from copy import deepcopy
from typing import List, Union


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

        if (scene.moving):
            obj.qt().setDefaultTextColor(QColor(Settings.Gui.MOVE_COLOR))
        else:
            obj.qt().setDefaultTextColor(QColor(Settings.Gui.PRIMARY_COLOR))


def edit_update(scene: EditScene, mouse_pos: QPointF, app: App, group = "", symbol = -1):
    reset_edit_objects(scene)

    if (group == ""):
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

    if (group == "Noten"):
        if (symbol < 7):
            note_edit_update(scene, mouse_pos, symbol)
        elif (symbol == 7):
            position_dot(scene, mouse_pos)

    elif (group == "Pausen"):
        if (symbol < 7):
            scene.edit_objects[0].change_text(Rest.SYMBOLS[symbol])

            next_bar_x = get_next_bar_x(scene)

            line = 2
            if (symbol == 0):
                line = 3

            places = current_bar.find_places([scene.edit_objects[0]], next_bar_x)
            if (len(places) >= 1):
                rest_x = bound_in_intervals(mouse_pos.x(), places)
                scene.edit_objects[0].set_real_pos(rest_x,
                                                   scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
                scene.successful = True
            else:
                scene.edit_objects[0].change_text()
        elif (symbol == 7):
            position_dot(scene, mouse_pos)

    elif (group == "Artikulation"):
        free_position(scene, mouse_pos, group, symbol)
    elif (group == "Dynamik"):
        free_position(scene, mouse_pos, group, symbol)
    elif (group == "Vorzeichen"):
        accidental = scene.edit_objects[0]
        accidental.change_text(SymbolButton.SYMBOLS["Vorzeichen"]["buttons"][symbol][0])

        y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(scene.current_line)

        # check wether accidental would fit into the bar
        places = scene.current_stave.bars[scene.current_bar_n].find_places([accidental], get_next_bar_x(scene))

        x = bound_in_intervals(mouse_pos.x(), places)

        if (x != None):
            accidental.set_real_pos(x, y)
            scene.successful = True
        else:
            accidental.change_text()

    elif (group == "Taktarten"):
        bar_line_x = current_bar.qt().scenePos().x()

        space = True

        for n, stave in enumerate(scene.current_system.staves):
            scene.edit_objects[n].change_text(SymbolButton.SYMBOLS["Taktarten"]["buttons"][symbol][0])
            intervals = stave.bars[scene.current_bar_n].find_places([scene.edit_objects[n]], get_next_bar_x(scene))
            if ((len(intervals) == 0 or intervals[0][0] != stave.bars[
                scene.current_bar_n].qt().scenePos().x() + Musicitem.MIN_OBJ_DIST) and not stave.bars[
                scene.current_bar_n].time_signature_visible):
                space = False
                break

        if (space):
            # time signature positioning
            for n, stave in enumerate(scene.current_system.staves):
                scene.edit_objects[n].set_real_pos(bar_line_x + Musicitem.MIN_OBJ_DIST,
                                                   stave.qt().scenePos().y() + Musicitem.EM)

            scene.successful = True

        else:
            for n, stave in enumerate(scene.current_system.staves):
                scene.edit_objects[n].change_text()

    elif (group == "N-Tolen"):
        scene.edit_objects[0].change_text("tuplet" + str(symbol + 2))
        scene.edit_objects[0].set_real_pos(
            bound(mouse_pos.x(), Settings.Layout.MARGIN,
                  Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.edit_objects[0].get_real_width()),
            bound(mouse_pos.y(), Settings.Layout.MARGIN - scene.edit_objects[0].get_real_height(),
                  Settings.Layout.HEIGHT - Settings.Layout.MARGIN)
        )
        scene.successful = True

    elif (group == "Sonstige"):
        # barline
        if (symbol == 1):
            new_bar = scene.edit_objects[0]
            piano_bar = scene.edit_objects[1]
            new_bar.change_text("barlineSingle")
            piano_bar.change_text("barlineSingle")

            #  positioning
            places_ = []
            start = current_bar.get_start()
            end = Bar.get_end([scene.edit_objects[0]], get_next_bar_x(scene))
            for stave in scene.current_system.staves:
                places_.append(
                    stave.bars[scene.current_bar_n].find_places([scene.edit_objects[0]], get_next_bar_x(scene)))

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
                        new_bar.qt().setTransform(
                            QTransform().scale(1, scene.current_system.get_other_voices_height() / Musicitem.EM))
                        new_bar.set_real_pos(bar_x, scene.current_system.get_bottom_other_voices_y())
                    else:
                        new_bar.change_text()

                    # two bar lines, for each bar, one for piano and one for the other voices
                    piano_bar.qt().setTransform(
                        QTransform().scale(1, scene.current_system.get_piano_height() / Musicitem.EM))
                    piano_bar.set_real_pos(bar_x, scene.current_system.get_bottom_y())
                    scene.successful = True
            else:
                new_bar.change_text()
                piano_bar.change_text()

        elif (1 < symbol < 5):
            clef = scene.edit_objects[0]
            clef.change_text(Clef.SYMBOLS[symbol - 2]["smufl_key"])

            next_bar_x = get_next_bar_x(scene)

            # determine line to put clef on
            closest_line = scene.current_stave.get_closest_line(mouse_pos, 1)
            dists = []
            for line in Clef.SYMBOLS[symbol - 2]["lines"]:
                dists.append(abs(line - closest_line))

            line = Clef.SYMBOLS[symbol - 2]["lines"][dists.index(min(dists))]

            places = current_bar.find_places([clef], next_bar_x)
            if (len(places) >= 1):
                clef_x = bound_in_intervals(mouse_pos.x(), places)
                clef.set_real_pos(clef_x, scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line))
                scene.successful = True
            else:
                clef.change_text()
        elif (symbol == 0 or symbol > 4):
            free_position(scene, mouse_pos, group, symbol)
    elif (group == "Werkzeuge"):
        if (symbol == 0):
            scene.successful = delete_item_edit_update(scene, mouse_pos, QColor(Settings.Gui.DELETE_COLOR))
        elif (symbol == 1):
            scene.successful = delete_item_edit_update(scene, mouse_pos, QColor(Settings.Gui.MOVE_COLOR))


def free_position(scene: EditScene, mouse_pos: QPointF, group = "", symbol = -1):
    scene.edit_objects[0].change_text(
        SymbolButton.SYMBOLS[group]["buttons"][symbol][0])
    scene.edit_objects[0].set_real_pos(
        bound(mouse_pos.x(), Settings.Layout.MARGIN,
              Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.edit_objects[0].get_real_width()),
        bound(mouse_pos.y(), Settings.Layout.MARGIN - scene.edit_objects[0].get_real_height(),
              Settings.Layout.HEIGHT - Settings.Layout.MARGIN)
    )
    scene.successful = True


def position_dot(scene: EditScene, mouse_pos: QPointF):
    dot = scene.edit_objects[0]
    dot.change_text("metAugmentationDot")

    line = scene.current_stave.get_closest_line(mouse_pos, 1, 0.5)
    y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(line)

    # check wether dot would fit into the bar
    places = scene.current_stave.bars[scene.current_bar_n].find_places([dot], get_next_bar_x(scene))

    x = bound_in_intervals(mouse_pos.x(), places)

    if (x != None):
        dot.set_real_pos(x, y)
        scene.successful = True
    else:
        dot.change_text()


def note_edit_update(scene: EditScene, mouse_pos: QPointF, symbol = -1):
    note = scene.edit_objects[0]
    items = [note]

    # notes positioning
    note.change_text(Note.SYMBOLS[2])
    if (symbol < 2):
        note.change_text(Note.SYMBOLS[symbol])

    # add notehead
    # note_x and all relative positions will be updated again
    note_x = 0
    note_y = scene.current_stave.qt().scenePos().y() + Musicitem.get_line_y(scene.current_line)
    note.set_real_pos(note_x, note_y)

    if (symbol > 0):
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
            stem_y = note_y + stem.get_real_height() - Musicitem.spec_to_px(stem_spec["stemDownNW"][1])
            correction /= 2

        stem.set_real_pos(stem_x + Musicitem.spec_to_px(correction), stem_y)

        # add flag
        if (symbol > 2):
            flag_y = stem.get_real_relative_y() - stem.get_real_height()
            direction = "Up"

            # flip flag
            if (scene.current_line >= 2):
                direction = "Down"
                flag_y = stem_y

            flag = scene.edit_objects[2]
            items.append(flag)
            flag.change_text(Note.FLAGS[symbol - 3] + direction)
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
            if (symbol == 0):
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


def point_in_rect(point: QPointF, rect: QRectF, tolerance: float = 0):
    return rect.x() - tolerance <= point.x() and rect.x() + rect.width() + tolerance >= point.x() and rect.y() - tolerance <= point.y() and rect.y() + rect.height() + tolerance >= point.y()


def set_last(scene):
    scene.last_bar_n = scene.current_bar_n
    scene.last_stave = scene.current_stave
    scene.last_system = scene.current_system


def delete_item_edit_update(scene: EditScene, mouse_pos: QPointF, color: QColor):
    current_bar = scene.current_stave.bars[scene.current_bar_n]

    # unselect last bar objects
    # if not done, some things in bars will be left selected without being selected actually
    if (scene.last_bar_n != None):
        last_bar = scene.last_stave.bars[scene.last_bar_n]

        for stave in scene.last_system.staves:
            for bar in stave.bars:
                if (bar.left_bar_line != None):
                    bar.left_bar_line.unselect()

        for stave in scene.last_system.staves:
            for bar in stave.bars:
                if (bar.time_signature_visible):
                    bar.time_signature.unselect()

        for item in last_bar.objects:
            item.unselect()

        for item in scene.last_system.free_objects:
            item.unselect()

    # select item if mousepos in bounding rect
    # tolerance to make it more user friendly
    tolerance = Musicitem.MIN_OBJ_DIST / 3

    # we have 4 item storages in the bar which are all handled differently
    for stave in scene.current_system.staves:
        for n, bar in enumerate(stave.bars):
            # check wether a barline is selected
            if (bar.left_bar_line != None and point_in_rect(mouse_pos, bar.left_bar_line.get_bounding_rect(),
                                                            tolerance)):

                # then select all barlines
                for stave in scene.current_system.staves:
                    if (stave.bars[n].left_bar_line != None):
                        stave.bars[n].left_bar_line.select(color)

                # and the time signature if visible, because (logically) it will be removed
                for stave in scene.current_system.staves:
                    if (stave.bars[n].time_signature_visible):
                        stave.bars[n].time_signature.select(color)

                set_last(scene)
                return True

    for stave in scene.current_system.staves:
        # check wether a barline is selected
        if (point_in_rect(mouse_pos, stave.bars[scene.current_bar_n].time_signature.get_bounding_rect(), tolerance) and
                stave.bars[scene.current_bar_n].time_signature_visible):

            for stave in scene.current_system.staves:
                stave.bars[scene.current_bar_n].time_signature.select(color)

            set_last(scene)
            return True

    for item in current_bar.objects:
        # check wether mouse_pos collides
        if (point_in_rect(mouse_pos, item.get_bounding_rect(), tolerance)):
            item.select(color)

            set_last(scene)
            return True

    for item in scene.current_system.free_objects:
        if (point_in_rect(mouse_pos, item.get_bounding_rect(), tolerance)):
            item.select(color)

            set_last(scene)
            return True

    return False


def edit_pressed(scene: EditScene, mouse_pos: QPointF, app: App, group, symbol):
    if (group == "" or scene.successful == False):
        return

    added_item: List[Union[Musicitem, MusicitemGroup]] = []
    moving_set = False

    if (group == "Noten"):
        if (symbol < 7):
            note = scene.current_stave.bars[scene.current_bar_n].add_note(
                scene.edit_objects[0],
                scene.edit_objects[1],
                scene.edit_objects[2],
                [item for item in scene.edit_objects if item.key[:9] == "legerLine"]
            )
            added_item.append(note)
        elif (symbol == 7):
            added_item.append(add_simple_item(scene))
    elif (group == "Pausen"):
        if (symbol < 7):
            added_item.append(scene.current_stave.bars[scene.current_bar_n].add_rest(scene.edit_objects[0]))
        elif (symbol == 7):
            added_item.append(add_simple_item(scene))

    # --
    # this will be specified in more detail later
    elif (group == "Artikulation"):
        added_item.append(add_free_item(scene))
    elif (group == "Dynamik"):
        added_item.append(add_free_item(scene))
    elif (group == "Vorzeichen"):
        added_item.append(add_simple_item(scene))
    # --

    elif (group == "Taktarten"):
        for n, stave in enumerate(scene.current_system.staves):
            added_item.append(stave.bars[scene.current_bar_n].show_time_signature(
                SymbolButton.SYMBOLS["Taktarten"]["buttons"][symbol][1]))
    elif (group == "N-Tolen"):
        added_item.append(add_free_item(scene))
    elif (group == "Sonstige"):
        if (symbol == 1):
            for n, stave in enumerate(scene.current_system.staves):
                barline = stave.add_bar(scene.edit_objects, app.document_ui.staves, n, app.document_ui.with_piano)
                if (barline != None):
                    added_item.append(barline)
        elif (1 < symbol < 5):
            added_item.append(scene.current_stave.bars[scene.current_bar_n].add_clef(scene.edit_objects[0], symbol - 2))
        elif (symbol == 0 or symbol > 4):
            added_item.append(add_free_item(scene))
    elif (group == "Werkzeuge"):
        if (symbol == 0):
            delete_item_pressed(scene)
        elif (symbol == 1):
            group, symbol = delete_item_pressed(scene)

            scene.moving = True
            scene.moving_group = group
            scene.moving_symbol = symbol
            moving_set = True

    for item in added_item:
        # needed by the "moving algorithm" (it actually uses the deleting algorithm)
        item.group = group
        item.symbol = symbol

    if (scene.moving and not moving_set):
        scene.moving = False
        edit_update(scene, mouse_pos, app)
    else:
        # remove the selected item from the current pos
        edit_update(scene, mouse_pos, app, group, symbol)


def add_free_item(scene: EditScene):
    return scene.current_system.add_free_item(scene.edit_objects[0])


def add_simple_item(scene: EditScene):
    return scene.current_stave.bars[scene.current_bar_n].add_object(deepcopy(scene.edit_objects[0]), True)


def delete_item_pressed(scene: EditScene):
    if (scene.last_bar_n != None):
        last_bar = scene.last_stave.bars[scene.last_bar_n]

        for stave in scene.last_system.staves:
            for n, bar in enumerate(stave.bars):
                if (bar.left_bar_line != None and bar.left_bar_line.selected):
                    # remove bar "head" (barline and time signature)
                    remove_time_signature(n, scene)
                    for stave in scene.last_system.staves:
                        bar = stave.bars[n]
                        if (bar.left_bar_line != None):
                            scene.removeItem(bar.left_bar_line.qt())
                        stave.delete_bar_head(n)
                    scene.last_bar_n = n - 1
                    return "Sonstige", 1

        for stave in scene.last_system.staves:
            for n, bar in enumerate(stave.bars):
                if (bar.time_signature_visible and bar.time_signature.selected):
                    symbol = bar.time_signature.symbol
                    remove_time_signature(n, scene)
                    return "Taktarten", symbol

        group, symbol = check_removing(scene, last_bar.objects)

        if (group != ""):
            return group, symbol

        group, symbol = check_removing(scene, scene.current_system.free_objects)

        if (group != ""):
            return group, symbol

        return "", -1


def remove_time_signature(n_bar: int, scene: EditScene):
    for stave in scene.last_system.staves:
        if (stave.bars[n_bar].time_signature_visible):
            stave.bars[n_bar].hide_time_signature()
            scene.removeItem(stave.bars[n_bar].time_signature.qt())


def check_removing(scene: EditScene, items: List[Union[Musicitem, MusicitemGroup]]):
    for n, item in enumerate(items):
        if (item.selected):
            group = item.group
            symbol = item.symbol
            if (type(item).__bases__[0] == MusicitemGroup):
                for item_ in item.qt().childItems():
                    scene.removeItem(item_)
            else:
                scene.removeItem(item.qt())
            parent = item.qt().group()
            if (parent):
                parent.removeFromGroup(item.qt())
            items.pop(n)
            return group, symbol
        
    return "", -1


def get_next_bar_x(scene: EditScene) -> float:
    next_bar_x = Settings.Layout.WIDTH - Settings.Layout.MARGIN - scene.current_system.right_bar_line.get_real_width()
    if (scene.current_bar_n != len(scene.current_stave.bars) - 1):
        next_bar_x = scene.current_stave.bars[scene.current_bar_n + 1].qt().scenePos().x() - \
                     scene.current_system.staves[0].bars[scene.current_bar_n + 1].left_bar_line.get_real_width()
    return next_bar_x


def unselect_buttons(app: App, pressed_button: SymbolButton = None):
    for buttons in app.ui.symbols_box_buttons:
        for button in buttons:
            if (pressed_button is None or (not (
                    button.group_key == pressed_button.group_key and button.n_symbol == pressed_button.n_symbol) and button.isChecked())):
                button.setChecked(False)

    for page in app.document_ui.pages:
        reset_edit_objects(page.qt())
        page.qt().moving = False


def get_selected_button(app: App) -> SymbolButton:
    selected_button: SymbolButton = None
    for buttons in app.ui.symbols_box_buttons:
        for button in buttons:
            if (button.isChecked()):
                selected_button = button
                break
    return selected_button

def get_group_and_symbol(scene: EditScene, button: SymbolButton):
    group = ""
    symbol = -1

    if (button != None):
        group = button.group_key
        symbol = button.n_symbol

    if (scene.moving):
        group = scene.moving_group
        symbol = scene.moving_symbol

    return group, symbol

def custom_move(self: EditScene, event: QGraphicsSceneMouseEvent):
    button = get_selected_button(self.app)
    group, symbol = get_group_and_symbol(self, button)
    edit_update(self, event.scenePos(), self.app, group, symbol)


def custom_pressed(self: EditScene, event: QGraphicsSceneMouseEvent):
    if (event.button() == Qt.LeftButton):
        button = get_selected_button(self.app)
        group, symbol = get_group_and_symbol(self, button)
        edit_pressed(self, event.scenePos(), self.app, group, symbol)
