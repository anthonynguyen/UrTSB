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
import gtk



class FavoritesFilter(gtk.HBox):
    """
    Filter/Control element of the favorites tab.
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.HBox.__init__(self)    
        
        refresh_button = gtk.Button('Refresh List')
        self.pack_end(refresh_button, False, False)
        refresh_button.connect("clicked", self.on_refresh_clicked)
    
        
    def on_refresh_clicked(self, widget):
        """
        Callback for the refresh button
        """
        guicontroller = GuiController()
        guicontroller.executeFavoritesLoading(self.parent)    
        
   
