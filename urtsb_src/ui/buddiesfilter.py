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



from urtsb_src.filemanager import FileManager
from urtsb_src.filter import Filter, FilterType
from urtsb_src.guicontroller import GuiController
import gtk


class BuddiesFilter(gtk.HBox):
    """
    Filter/Control element of the buddies tab.
    """


    def __init__(self, parenttab):
        """
        Constructor
        """
        gtk.HBox.__init__(self) 
        
        self.parenttab = parenttab 
        
        # not for displayreason, but for not to differ filtertypes when 
        # passing the filter to the querymethod
        self.checkbox_showfull = gtk.CheckButton('show full')
        self.checkbox_showfull.set_active(True)
        self.checkbox_showempty = gtk.CheckButton('show empty')
        self.checkbox_showempty.set_active(False)
        
          
        
        addbox = gtk.HBox()
        self.pack_start(addbox, True, True)
        
        add_desc_label = gtk.Label('Enter a playername and press search: ')
        self.playersearch_entry = gtk.Entry()
        self.playersearch_entry.set_width_chars(15)
        self.playersearchbutton = gtk.Button('Search for Player')
        addbox.pack_start(add_desc_label, False, False)
        addbox.pack_start(self.playersearch_entry, True, True)
        addbox.pack_start(self.playersearchbutton, False, False)
        self.playersearchbutton.connect("clicked", self.on_search_player_clicked)
        self.playersearchbutton.set_border_width(5)
        
        self.search_button = gtk.Button('Search for Buddies')
        self.search_button.set_border_width(5)
        self.pack_end(self.search_button, False, False)
        self.search_button.connect("clicked", self.on_search_buddies_clicked)
    
        self.show_all()
        
    def on_search_player_clicked(self, widget):
        """
        Callback of the player search button
        """
        self.search_button.set_sensitive(False)
        self.playersearchbutton.set_sensitive(False)
        
        name2search = self.playersearch_entry.get_text()
        searchname_list = []
        searchname_list.append(name2search)
        
        #create the filter object
        filter = Filter(FilterType.BUDDY_FILTER)
        filter.playerlist = searchname_list
        self.parenttab.set_all_buddies_to_offline()
        gc = GuiController()
        gc.executeMasterServerQuery(filter, self.parenttab) 
      
    def on_search_buddies_clicked(self, widget):
        """
        Callback of the search buddies button
        """
        self.search_button.set_sensitive(False)
        self.playersearchbutton.set_sensitive(False)
        
        fm = FileManager()
        fm.get_buddies()
        
        #create a filter object
        filter = Filter(FilterType.BUDDY_FILTER, self.parenttab)
        filter.playerlist = fm.get_buddies()
        self.parenttab.set_all_buddies_to_offline()
        gc = GuiController()
        gc.executeMasterServerQuery(filter, self.parenttab) 
        
    def get_filter_name(self):
        """
        Returns a string to identify this filter
        
        @return identificationstring of this filter
        """
        return 'buddiesfilter' 
   
    def lock(self):
        """
        Locks the UI-Elements for search so no two concurrent 
        requests can be executed!
        """
        self.search_button.set_sensitive(False)
        
    def unlock(self):
        """
        Unlocks the UI Elements for search after the request
        has finished.
        """
        self.search_button.set_sensitive(True)