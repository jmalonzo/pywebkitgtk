#!/usr/bin/env python
# Copyright (C) 2006, Red Hat, Inc.
# Copyright (C) 2007, One Laptop Per Child
# Copyright (C) 2007-2008 Jan Alonzo <jmalonzo@unpluggable.com>
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

from gettext import gettext as _

import gobject
import gtk
import pango
import webkit
from inspector import Inspector

ABOUT_PAGE = """
<html><head><title>PyWebKitGtk - About</title></head><body>
<h1>Welcome to <code>webbrowser.py</code></h1>
<p>
<strong>Home:</strong><a
href="http://code.google.com/p/pywebkitgtk/">http://code.google.com/p/pywebkitgtk/</a><br/>
<strong>Wiki:</strong><a
href="http://live.gnome.org/PyWebKitGtk">http://live.gnome.org/PyWebKitGtk</a><br/>
</p>
</body></html>
"""

class BrowserPage(webkit.WebView):

    def __init__(self):
        webkit.WebView.__init__(self)
        settings = self.get_settings()
        settings.set_property("enable-developer-extras", True)

        # scale other content besides from text as well
        self.set_full_content_zoom(True)

        # make sure the items will be added in the end
        # hence the reason for the connect_after
        self.connect_after("populate-popup", self.populate_popup)

    def populate_popup(self, view, menu):
        # zoom buttons
        zoom_in = gtk.ImageMenuItem(gtk.STOCK_ZOOM_IN)
        zoom_in.connect('activate', zoom_in_cb, view)
        menu.append(zoom_in)

        zoom_out = gtk.ImageMenuItem(gtk.STOCK_ZOOM_OUT)
        zoom_out.connect('activate', zoom_out_cb, view)
        menu.append(zoom_out)

        zoom_hundred = gtk.ImageMenuItem(gtk.STOCK_ZOOM_100)
        zoom_hundred.connect('activate', zoom_hundred_cb, view)
        menu.append(zoom_hundred)

        menu.append(gtk.SeparatorMenuItem())

        aboutitem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu.append(aboutitem)
        aboutitem.connect('activate', about_pywebkitgtk_cb, view)

        menu.show_all()
        return False

class ContentPane (gtk.Notebook):

    __gsignals__ = {
        "focus-view-title-changed": (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     (gobject.TYPE_OBJECT, gobject.TYPE_STRING,)),
        "focus-view-load-committed": (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      (gobject.TYPE_OBJECT, gobject.TYPE_OBJECT,))
        }

    def __init__ (self):
        """initialize the content pane"""
        gtk.Notebook.__init__(self)
        self.props.scrollable = True
        self.connect("switch-page", self._switch_page)

        self.show_all()
        self._hovered_uri = None

    def load (self, text):
        """load the given uri in the current web view"""
        child = self.get_nth_page(self.get_current_page())
        view = child.get_child()
        view.open(text)

    def new_tab (self, url=None):
        """creates a new page in a new tab"""
        # create the tab content
        browser = BrowserPage()
        browser.connect("hovering-over-link", self._hovering_over_link_cb)
        browser.connect("populate-popup", self._populate_page_popup_cb)
        browser.connect("load-committed", self._view_load_committed_cb)
        inspector = Inspector(browser.get_web_inspector())

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
        scrolled_window.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
        scrolled_window.add(browser)
        scrolled_window.show_all()

        # load the content
        self._hovered_uri = None
        if not url:
            browser.load_string(ABOUT_PAGE, "text/html", "iso-8859-15", "about")
            url = "about"
        else:
            browser.open(url)

        # create the tab
        label = self.create_tab_label(url, scrolled_window)
        label.show_all()

        new_tab_number = self.append_page(scrolled_window, label)
        self.set_tab_label_packing(scrolled_window, False, False, gtk.PACK_START)
        self.set_tab_label(scrolled_window, label)

        # hide the tab if there's only one
        self.set_show_tabs(self.get_n_pages() > 1)

        self.show_all()
        self.set_current_page(new_tab_number)

    def create_tab_label (self, title, child):
        """creates a new tab label"""
        hbox = gtk.HBox()
        icon = gtk.image_new_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        label = gtk.Label(title)
        label.props.max_width_chars = 30
        label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)

        close_button = gtk.Button()
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.connect("clicked", self._close_tab, child)
        close_button.set_image(close_image)
        close_button.set_relief(gtk.RELIEF_NONE)
        hbox.pack_start(icon, False, False, padding=0)
        hbox.pack_start(label, False, False, padding=0)
        hbox.pack_end(close_button, False, False, padding=0)
        return hbox

    def _populate_page_popup_cb(self, view, menu):
        # misc
        if self._hovered_uri:
            open_in_new_tab = gtk.MenuItem(_("Open Link in New Tab"))
            open_in_new_tab.connect("activate", self._open_in_new_tab, view)
            menu.insert(open_in_new_tab, 0)
            menu.show_all()

    def _open_in_new_tab (self, menuitem, view):
        self.new_tab(self._hovered_uri)

    def _close_tab (self, button, child):
        page_num = self.page_num(child)
        if page_num != -1:
            self.remove_page(page_num)
            child.destroy()
        self.set_show_tabs(self.get_n_pages() > 1)

    def _switch_page (self, notebook, page, page_num):
        child = self.get_nth_page(page_num)
        view = child.get_child()
        frame = view.get_main_frame()
        self.emit("focus-view-load-committed", view, frame)

    def _hovering_over_link_cb (self, view, title, uri):
        self._hovered_uri = uri

    def _view_load_committed_cb (self, view, frame):
        self.emit("focus-view-load-committed", view, frame)

class WebToolbar(gtk.Toolbar):

    __gsignals__ = {
        "load-requested": (gobject.SIGNAL_RUN_FIRST,
                             gobject.TYPE_NONE,
                             (gobject.TYPE_STRING,))
        }

    def __init__(self):
        gtk.Toolbar.__init__(self)

        # location entry
        self._entry = gtk.Entry()
        self._entry.connect('activate', self._entry_activate_cb)
        entry_item = gtk.ToolItem()
        entry_item.set_expand(True)
        entry_item.add(self._entry)
        self._entry.show()

        self.insert(entry_item, -1)
        entry_item.show()

    def location_set_text (self, text):
        self._entry.set_text(text)

    def _entry_activate_cb(self, entry):
        self.emit("load-requested", entry.props.text)

class WebBrowser(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)

        toolbar = WebToolbar()
        content_tabs = ContentPane()
        content_tabs.connect("focus-view-load-committed", self._load_committed_cb, toolbar)
        toolbar.connect("load-requested", load_requested_cb, content_tabs)

#        statusbar = WebStatusBar()

#        content_tabs.connect("load-started", load_started_cb, toolbar)
#        content_tabs.connect('load-progress-changed', load_progress_cb, statusbar)
#        content_tabs.connect('load-finished', load_stop_cb)
#        content_tabs.connect('load-committed', load_committed_cb)
#        content_tabs.connect("title-changed", title_changed_cb, self)
#        content_tabs.connect("hovering-over-link", hover_link_cb, statusbar)
#        content_tabs.connect("status-bar-text-changed",statusbar_text_changed_cb, statusbar)

        vbox = gtk.VBox(spacing=1)
        vbox.pack_start(toolbar, expand=False, fill=False)
        vbox.pack_start(content_tabs)
#        vbox.pack_end(statusbar, expand=False, fill=False)

        self.add(vbox)
        self.set_default_size(800, 600)
        self.connect('destroy', destroy_cb)

        content_tabs.new_tab("http://www.google.com")

        self.show_all()

    def _load_committed_cb (self, tabbed_pane, view, frame, toolbar):
        title = frame.get_title()
        if not title:
           title = frame.get_uri()
        self.set_title(_("PyWebKitGtk - %s") % title)
        load_committed_cb(tabbed_pane, view, frame, toolbar)

# event handlers
def load_requested_cb (widget, text, content_pane):
    if not text:
        return
    content_pane.load(text)

def load_committed_cb (tabbed_pane, view, frame, toolbar):
    uri = frame.get_uri()
    if uri:
        toolbar.location_set_text(uri)

def destroy_cb(window):
    """destroy window resources"""
    window.destroy()
    gtk.main_quit()

# context menu item callbacks
def about_pywebkitgtk_cb(menu_item, web_view):
    web_view.open("http://live.gnome.org/PyWebKitGtk")

def zoom_in_cb(menu_item, web_view):
    """Zoom into the page"""
    web_view.zoom_in()

def zoom_out_cb(menu_item, web_view):
    """Zoom out of the page"""
    web_view.zoom_out()

def zoom_hundred_cb(menu_item, web_view):
    """Zoom 100%"""
    if not (web_view.get_zoom_level() == 1.0):
        web_view.set_zoom_level(1.0)

class WebStatusBar(gtk.Statusbar):

    def __init__(self):
        gtk.Statusbar.__init__(self)

    def display(self, text, context=None):
        cid = self.get_context_id("pywebkitgtk")
        self.push(cid, str(text))


if __name__ == "__main__":
    webbrowser = WebBrowser()
    gtk.main()
