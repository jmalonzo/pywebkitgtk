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
import time
from gettext import gettext as _

import gtk
import webkit


class WebToolbar(gtk.Toolbar):
    def __init__(self, browser):
        gtk.Toolbar.__init__(self)

        self._browser = browser
        self._back_forward_list = self._browser.get_back_forward_list()

        self._back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self._back.set_tooltip(gtk.Tooltips(),_('Back'))
        self._back.props.sensitive = False
        self._back.connect('clicked', self._go_back_cb)
        self.insert(self._back, -1)

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

        self.insert(gtk.SeparatorToolItem(), -1)

        # location entry
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
        can_go_back = self._browser.can_go_back()
        self._back.props.sensitive = can_go_back

        can_go_forward = self._browser.can_go_forward()
        self._forward.props.sensitive = can_go_forward

    def _entry_activate_cb(self, entry):
        self._browser.open(entry.props.text)

    def _go_back_cb(self, button):
        self._browser.go_back()

    def _go_forward_cb(self, button):
        self._browser.go_forward()

    def _title_changed_cb(self, widget, frame, title):
        self._set_address(frame.get_uri())

    def _stop_and_reload_cb(self, button):
        if self._loading:
            self._browser.stop_loading()
        else:
            self._browser.reload()

    def _show_stop_icon(self):
        self._stop_and_reload.set_stock_id(gtk.STOCK_CANCEL)

    def _show_reload_icon(self):
        self._stop_and_reload.set_stock_id(gtk.STOCK_REFRESH)


class BrowserPage(webkit.WebView):
    def __init__(self):
	webkit.WebView.__init__(self)

class WebStatusBar(gtk.Statusbar):
    def __init__(self):
        gtk.Statusbar.__init__(self)
        self.iconbox = gtk.EventBox()
        self.iconbox.add(gtk.image_new_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_BUTTON))
        self.pack_start(self.iconbox, False, False, 6)
        self.iconbox.hide_all()

    def display(self, text, context=None):
        cid = self.get_context_id("pywebkitgtk")
        self.push(cid, str(text))

    def show_javascript_info(self):
        self.iconbox.show()

    def hide_javascript_info(self):
        self.iconbox.hide()


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
        self._browser.connect("populate-popup", self._populate_popup)
#        self._browser.connect("navigation-requested", self._navigation_requested_cb)

        self._browser.connect("console-message",
                              self._javascript_console_message_cb)
        self._browser.connect("script-alert",
                              self._javascript_script_alert_cb)
        self._browser.connect("script-confirm",
                              self._javascript_script_confirm_cb)
        self._browser.connect("script-prompt",
                              self._javascript_script_prompt_cb)

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
            self._set_title(_("Loading %s - %s") % (frame.get_title(),frame.get_uri()))
        self._toolbar.set_loading(True)

    def _loading_stop_cb(self, page, frame):
        # FIXME: another frame may still be loading?
        self._toolbar.set_loading(False)

    def _loading_progress_cb(self, page, progress):
        self._set_progress(_("%s%s loaded") % (progress, '%'))

    def _set_progress(self, progress):
        self._statusbar.display(progress)

    def _title_changed_cb(self, widget, frame, title):
        self._set_title(_("%s") % title)

    def _hover_link_cb(self, page, title, url):
    	if page and url:
	   self._statusbar.display(url)
	else:
 	   self._statusbar.display('')

    def _statusbar_text_changed_cb(self, page, text):
        if text:
            self._statusbar.display(text)

    def _icon_loaded_cb(self):
        print "icon loaded"

    def _selection_changed_cb(self):
        print "selection changed"

    def _set_scroll_adjustments_cb(self, page, hadjustment, vadjustment):
        self._scrolled_window.props.hadjustment = hadjustment
        self._scrolled_window.props.vadjustment = vadjustment

    def _navigation_requested_cb(self, page, frame, networkRequest):
        print "navigation requested cb"
        return 1 # fixme

    def _javascript_console_message_cb(self, page, message, line, sourceid):
        self._statusbar.show_javascript_info()

    def _javascript_script_alert_cb(self, page, frame, message):
        pass

    def _javascript_script_confirm_cb(self, page, frame, message, isConfirmed):
        pass

    def _javascript_script_prompt_cb(self, page, frame, message, default, text):
        pass

    def _populate_popup(self, view, menu):
        aboutitem = gtk.MenuItem(label="About PyWebKit")
        menu.append(aboutitem)
        aboutitem.connect('activate', self._about_pywebkitgtk_cb)
        menu.show_all()

    def _about_pywebkitgtk_cb(self, widget):
        self._browser.open("http://live.gnome.org/PyWebKitGtk")



if __name__ == "__main__":
    webbrowser = WebBrowser()
    gtk.main()

