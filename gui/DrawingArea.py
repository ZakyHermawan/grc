"""
Copyright 2007, 2008, 2009, 2010 Free Software Foundation, Inc.
This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

from __future__ import absolute_import

from gi.repository import Gtk, Gdk, GObject

from . import Constants, Colors


class DrawingArea(Gtk.DrawingArea):
    """
    DrawingArea is the gtk pixel map that graphical elements may draw themselves on.
    The drawing area also responds to mouse and key events.
    """

    def __init__(self, flow_graph):
        """
        DrawingArea contructor.
        Connect event handlers.

        Args:
            main_window: the main_window containing all flow graphs
        """
        Gtk.DrawingArea.__init__(self)

        self._flow_graph = flow_graph

        self.zoom_factor = 1.0
        self.ctrl_mask = False
        self.mod1_mask = False
        self.button_state = [False] * 10

        # self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.connect('realize', self._handle_window_realize)
        self.connect('draw', self.draw)
        self.connect('motion-notify-event', self._handle_mouse_motion)
        self.connect('button-press-event', self._handle_mouse_button_press)
        self.connect('button-release-event', self._handle_mouse_button_release)
        self.connect('scroll-event', self._handle_mouse_scroll)
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.SCROLL_MASK |
            Gdk.EventMask.LEAVE_NOTIFY_MASK |
            Gdk.EventMask.ENTER_NOTIFY_MASK
            #Gdk.EventMask.FOCUS_CHANGE_MASK
        )

        # setup drag and drop
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.connect('drag-data-received', self._handle_drag_data_received)
        self.drag_dest_set_target_list(None)
        self.drag_dest_add_text_targets()

        # setup the focus flag
        self._focus_flag = False
        self.get_focus_flag = lambda: self._focus_flag
        def _handle_notify_event(widget, event, focus_flag): self._focus_flag = focus_flag
        self.connect('leave-notify-event', _handle_notify_event, False)
        self.connect('enter-notify-event', _handle_notify_event, True)
        # todo: fix
#        self.set_flags(Gtk.CAN_FOCUS)  # self.set_can_focus(True)
#        self.connect('focus-out-event', self._handle_focus_lost_event)

    ##########################################################################
    ## Handlers
    ##########################################################################
    def _handle_drag_data_received(self, widget, drag_context, x, y, selection_data, info, time):
        """
        Handle a drag and drop by adding a block at the given coordinate.
        """
        self._flow_graph.add_new_block(selection_data.get_text(), (x, y))

    def _handle_mouse_scroll(self, widget, event):
        if event.get_state() & Gdk.ModifierType.SHIFT_MASK:
            if event.direction == Gdk.ScrollDirection.UP:
                event.direction = Gdk.ScrollDirection.LEFT
            else:
                event.direction = Gdk.ScrollDirection.RIGHT

        elif event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            change = 1.2 if event.direction == Gdk.ScrollDirection.UP else 1/1.2
            zoom_factor = min(max(self.zoom_factor * change, 0.1), 5.0)

            if zoom_factor != self.zoom_factor:
                self.zoom_factor = zoom_factor
                self.queue_draw()
            return True

        return False

    def _handle_mouse_button_press(self, widget, event):
        """
        Forward button click information to the flow graph.
        """
        self.grab_focus()
        self.ctrl_mask = event.get_state() & Gdk.ModifierType.CONTROL_MASK
        self.mod1_mask = event.get_state() & Gdk.ModifierType.MOD1_MASK
        self.button_state[event.button] = True

        if event.button == 1:
            double_click = (event.type == Gdk.EventType._2BUTTON_PRESS)
            self.button_state[1] = not double_click
            self._flow_graph.handle_mouse_selector_press(
                double_click=double_click,
                coordinate=self._translate_event_coords(event),
            )
        elif event.button == 3:
            self._flow_graph.handle_mouse_context_press(
                coordinate=self._translate_event_coords(event),
                event=event,
            )

    def _handle_mouse_button_release(self, widget, event):
        """
        Forward button release information to the flow graph.
        """
        self.ctrl_mask = event.get_state() & Gdk.ModifierType.CONTROL_MASK
        self.mod1_mask = event.get_state() & Gdk.ModifierType.MOD1_MASK
        self.button_state[event.button] = False
        if event.button == 1:
            self._flow_graph.handle_mouse_selector_release(
                coordinate=self._translate_event_coords(event),
            )

    def _handle_mouse_motion(self, widget, event):
        """
        Forward mouse motion information to the flow graph.
        """
        self.ctrl_mask = event.get_state() & Gdk.ModifierType.CONTROL_MASK
        self.mod1_mask = event.get_state() & Gdk.ModifierType.MOD1_MASK

        if self.button_state[1]:
            self._auto_scroll(event)

        self._flow_graph.handle_mouse_motion(
            coordinate=self._translate_event_coords(event),
        )

    def _auto_scroll(self, event):
        x, y = event.x, event.y
        scrollbox = self.get_parent().get_parent()

        w, h = self._flow_graph.get_max_coords(initial=(x, y))
        self.set_size_request(w + 100, h + 100)

        def scroll(pos, adj):
            """scroll if we moved near the border"""
            adj_val = adj.get_value()
            adj_len = adj.get_page_size()
            if pos - adj_val > adj_len - Constants.SCROLL_PROXIMITY_SENSITIVITY:
                adj.set_value(adj_val + Constants.SCROLL_DISTANCE)
                adj.emit('changed')
            elif pos - adj_val < Constants.SCROLL_PROXIMITY_SENSITIVITY:
                adj.set_value(adj_val - Constants.SCROLL_DISTANCE)
                adj.emit('changed')

        scroll(x, scrollbox.get_hadjustment())
        scroll(y, scrollbox.get_vadjustment())

    def _handle_window_realize(self, widget):
        """
        Called when the window is realized.
        Update the flowgraph, which calls new pixmap.
        """
        self._flow_graph.update()
        w, h = self._flow_graph.get_max_coords()
        self.set_size_request(w + 100, h + 100)

    def draw(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        cr.set_source_rgba(*Colors.FLOWGRAPH_BACKGROUND_COLOR)
        cr.rectangle(0, 0, width, height)

        cr.scale(self.zoom_factor, self.zoom_factor)
        cr.fill()

        self._flow_graph.draw(cr)

    def _translate_event_coords(self, event):
        return event.x / self.zoom_factor, event.y / self.zoom_factor

    def _handle_focus_lost_event(self, widget, event):
        # don't clear selection while context menu is active
        if not self._flow_graph.get_context_menu().flags() & Gtk.VISIBLE:
            self._flow_graph.unselect()
            self._flow_graph.update_selected()
            self._flow_graph.queue_draw()
