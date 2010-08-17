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


from UrTSB.guicontroller import GuiController
import gtk



class RecentSeversFilter(gtk.HBox):
    """
    Filter/Control element of the favorites tab.
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.HBox.__init__(self)    
        
        clear_button = gtk.Button('Clear List')
        self.pack_start(clear_button, False, False)
        clear_button.connect("clicked", self.on_clear_button_clicked)
        
        self.refresh_button = gtk.Button('Refresh List')
        self.pack_end(self.refresh_button, False, False)
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
    
    def on_clear_button_clicked(self, widget):
        """
        Callback for the clear list button
        """
        guicontroller = GuiController()
        guicontroller.clearRecentServers(self.parent)
        
    def on_refresh_clicked(self, widget):
        """
        Callback for the refresh button
        """
        self.refresh_button.set_sensitive(False)
        
        guicontroller = GuiController()
        guicontroller.executeRecentServersLoading(self.parent)    
        
   
