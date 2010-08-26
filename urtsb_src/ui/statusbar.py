#
# Copyright (C) 2010  Sorcerer
#
# This file is part of UrTSB.
#
# UrTSB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UrTSB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UrTSB.  If not, see <http://www.gnu.org/licenses/>.
#


import gtk

class StatusBar(gtk.Statusbar):
    """
    Statusbar GUI element containing a progressbar.
    """


    def __init__(self, parenttab):
        """
        Constructor
        """
        gtk.Statusbar.__init__(self)
        
        self.parenttab = parenttab
        
        self.set_border_width(2)
        
        self.progressbar = gtk.ProgressBar()
        
        hbox = gtk.HBox()
        
        self.add(hbox)
        
        hbox.pack_start(self.progressbar, True, True)
        
        self.abort_button = gtk.Button()
        abortimage = gtk.Image()
        abortimage.set_from_stock(gtk.STOCK_CANCEL, gtk.ICON_SIZE_BUTTON)
        self.abort_button.set_image(abortimage)
        hbox.pack_start(self.abort_button, False, False)
        self.abort_button.set_border_width(0)
        self.abort_button.connect('clicked', self.on_abort_button_clicked)
        
        self.lock()
        
    def lock(self):
        """
        Locks the abort button
        """
        self.abort_button.set_sensitive(False)
        
    def unlock(self):
        """
        unlocks the abort button
        """
        self.abort_button.set_sensitive(True)
        
    def on_abort_button_clicked(self, button):
        """
        Callback of the abort button
        """
        self.parenttab.abort_current_task()