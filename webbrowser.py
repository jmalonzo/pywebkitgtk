#!/usr/bin/env python
# Copyright (C) 2006, Red Hat, Inc.
# Copyright (C) 2007, One Laptop Per Child
# Copyright (C) 2007 Jan Alonzo <jmalonzo@unpluggable.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import logging
from gettext import gettext as _

import gtk
import webkitgtk


class WebToolbar(gtk.Toolbar):
    def __init__(self, browser):
        gtk.Toolbar.__init__(self)

        self._browser = browser

        self._back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self._back.set_tooltip(gtk.Tooltips(),_('Back'))
        self._back.props.sensitive = False
        self._back.connect('clicked', self._go_back_cb)
        self.insert(self._back, -1)
        self._back.show()

        self._forward = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self._forward.set_tooltip(gtk.Tooltips(),_('Forward'))
        self._forward.props.sensitive = False
        self._forward.connect('clicked', self._go_forward_cb)
        self.insert(self._forward, -1)
        self._forward.show()

        self._stop_and_reload = gtk.ToolButton(gtk.STOCK_REFRESH)
        self._stop_and_reload.connect('clicked', self._stop_and_reload_cb)
        self.insert(self._stop_and_reload, -1)
        self._stop_and_reload.show()
        self._loading = False

        self._entry = gtk.Entry()
        self._entry.connect('activate', self._entry_activate_cb)
        self._current_uri = None

        entry_item = gtk.ToolItem()
        entry_item.set_expand(True)
        entry_item.add(self._entry)
        self._entry.show()

        self.insert(entry_item, -1)
        entry_item.show()

        self._browser.connect("title-changed", self._title_changed_cb)
        self._entry.grab_focus()

    def set_loading(self, loading):
        self._loading = loading

        if self._loading:
            self._show_stop_icon()
            self._stop_and_reload.set_tooltip(gtk.Tooltips(),_('Stop'))
        else:
            self._show_reload_icon()
            self._stop_and_reload.set_tooltip(gtk.Tooltips(),_('Reload'))
        self._update_navigation_buttons()

    def _set_address(self, address):
        self._entry.props.text = address
        self._current_uri = address

    def _update_navigation_buttons(self):
        can_go_back = self._browser.can_go_backward()
        self._back.props.sensitive = can_go_back

        can_go_forward = self._browser.can_go_forward()
        self._forward.props.sensitive = can_go_forward

    def _entry_activate_cb(self, entry):
        self._browser.open(entry.props.text)
        #self._browser.grab_focus()

    def _go_back_cb(self, button):
        self._browser.go_backward()

    def _go_forward_cb(self, button):
        self._browser.go_forward()

    def _title_changed_cb(self, widget, title, uri):
        self._set_address(uri)

    def _stop_and_reload_cb(self, button):
        if self._loading:
            self._browser.stop_loading()
        else:
            self._browser.reload()

    def _show_stop_icon(self):
        self._stop_and_reload.set_stock_id(gtk.STOCK_MEDIA_STOP)

    def _show_reload_icon(self):
        self._stop_and_reload.set_stock_id(gtk.STOCK_REFRESH)


class BrowserPage(webkitgtk.Page):
    def __init__(self):
	webkitgtk.Page.__init__(self)

class WebStatusBar(gtk.Statusbar):
    def __init__(self):
        gtk.Statusbar.__init__(self)

    def display(self, text, context=None):
        cid = self.get_context_id("pywebkitgtk")
        self.push(cid, str(text))


class WebBrowser(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        logging.debug("initializing web browser window")

        self._loading = False
        self._browser= BrowserPage()
        self._browser.connect('load-started', self._loading_start_cb)
        self._browser.connect('load-progress-changed', self._loading_progress_cb)
        self._browser.connect('load-finished', self._loading_stop_cb)
        self._browser.connect("title-changed", self._title_changed_cb)
        self._browser.connect("hovering-over-link", self._hover_link_cb)
        self._browser.connect("status-bar-text-changed", self._statusbar_text_changed_cb)
        self._browser.connect("icon-loaded", self._icon_loaded_cb)
        self._browser.connect("selection-changed", self._selection_changed_cb)
        self._browser.connect("set-scroll-adjustments", self._set_scroll_adjustments_cb)

        self._scrolled_window = gtk.ScrolledWindow()
        self._scrolled_window.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
        self._scrolled_window.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
        self._scrolled_window.add(self._browser)
        self._scrolled_window.show_all()

        self._toolbar = WebToolbar(self._browser)

        self._statusbar = WebStatusBar()

        vbox = gtk.VBox(spacing=4)
        vbox.pack_start(self._toolbar, expand=False, fill=False)
        vbox.pack_start(self._scrolled_window)
        vbox.pack_end(self._statusbar, expand=False, fill=False)

        self.add(vbox)
        self.set_default_size(600, 480)

        self.connect('destroy', gtk.main_quit)

        about = """
<html><head><title>About</title></head><body>
<h1>Welcome to <code>webbrowser.py</code></h1>
<p><a href="http://live.gnome.org/PyWebKitGtk">Homepage</a></p>
</body></html>
"""
        self._browser.load_string(about, "text/html", "iso-8859-15", "about:")

        self.show_all()

    def _set_title(self, title):
        self.props.title = title

    def _loading_start_cb(self, page, frame):
        main_frame = self._browser.get_main_frame()
        if frame is main_frame:
            self._set_title(_("Loading %s - %s") % (frame.get_title(),frame.get_location()))
        self._toolbar.set_loading(True)

    def _loading_stop_cb(self, page, frame):
        # FIXME: another frame may still be loading?
        self._toolbar.set_loading(False)

    def _loading_progress_cb(self, page, progress):
        self._set_progress(_("%s%s loaded") % (progress, '%'))

    def _set_progress(self, progress):
        self._statusbar.display(progress)

    def _title_changed_cb(self, widget, title, uri):
        self._set_title(_("%s - %s") % (title,uri))

    def _hover_link_cb(self, url, base_url):
        print "link ", url, ' ', base_url

    def _statusbar_text_changed_cb(self, page, text):
        print "status ", text

    def _icon_loaded_cb(self):
        print "icon loaded"

    def _selection_changed_cb(self):
        print "selection changed"

    def _set_scroll_adjustments_cb(self, page, hadjustment, vadjustment):
        self._scrolled_window.props.hadjustment = hadjustment
        self._scrolled_window.props.vadjustment = vadjustment

if __name__ == "__main__":
    webbrowser = WebBrowser()
    gtk.main()

