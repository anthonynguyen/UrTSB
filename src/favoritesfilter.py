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

from guicontroller import GuiController
from server import Server
import gtk
from servermanager import ServerManager



class FavoritesFilter(gtk.HBox):
    """
    Filter/Control element of the favorites tab.
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.HBox.__init__(self)    
        
        addbox = gtk.HBox()
        self.pack_start(addbox, False, False)
        
        add_fav_label = gtk.Label('enter IP:Port and press "Add" to manually add a server')
        self.addentry = gtk.Entry()
        self.addentry.set_width_chars(40)
        addbutton = gtk.Button('Add')
        addbox.pack_start(add_fav_label, False, False)
        addbox.pack_start(self.addentry, False, False)
        addbox.pack_start(addbutton, False, False)
        addbutton.connect("clicked", self.on_add_clicked)
        
        
        refresh_button = gtk.Button('Refresh List')
        self.pack_end(refresh_button, False, False)
        refresh_button.connect("clicked", self.on_refresh_clicked)
    
        self.show_all()
        
    def on_add_clicked(self, widget):   
        srvman = ServerManager() 
        enteredserver = self.addentry.get_text()
        guicontroller = GuiController()
        try:
            host, port = enteredserver.split(':', 1)
            port = int(port)
            server = srvman.getServer(host, port)
        except:
            self.parent.statusbar.progressbar.set_text('Failed to add server!')
            return
        guicontroller.addFavorite(server)
        guicontroller.executeFavoritesLoading(self.parent) 
        if server.isFavorite():
            self.parent.statusbar.progressbar.set_text('Server successfully added')
            self.addentry.set_text('')
        else:
            self.parent.statusbar.progressbar.set_text('Failed to add server!')
            
    def on_refresh_clicked(self, widget):
        """
        Callback for the refresh button
        """
        guicontroller = GuiController()
        guicontroller.executeFavoritesLoading(self.parent)    
        
   
