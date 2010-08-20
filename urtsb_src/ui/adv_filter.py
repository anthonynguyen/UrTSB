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
from urtsb_src.guicontroller import GuiController
from urtsb_src.log import Log
from urtsb_src.servermanager import ServerManager
import gtk

class AdvancedFilter(gtk.HBox):
    """
    This is a filter panel for the server list tab. 
    As the basic filter panel (serverlistfilter.py) needs enough space and there
    is no good place to add more filter options this filter panel provides a
    button to open filter settings in a popup window. Additionaly a text entry
    is provided to lookup a server directly by ip:port without the need of 
    performing a master server query.
    """


    def __init__(self, parent):
        """
        Constructor
        """
        gtk.HBox.__init__(self)    
        
        self.parenttab = parent
        
        lookupbox = gtk.HBox()
        self.pack_start(lookupbox, False, False)
        
        desc_lookup_label = gtk.Label('direct server lookup:')
        self.lookupentry = gtk.Entry()
        self.lookupentry.set_width_chars(40)
        self.lookupbutton = gtk.Button('Lookup')
        lookupbox.pack_start(desc_lookup_label, False, False)
        lookupbox.pack_start(self.lookupentry, False, False)
        lookupbox.pack_start(self.lookupbutton, False, False)
        self.lookupbutton.connect("clicked", self.on_lookup_clicked)
        self.lookupbutton.set_border_width(5)
        
        
        
        
        self.search_button = gtk.Button('Search')
        self.pack_end(self.search_button, False, False)
        self.search_button.connect("clicked", self.on_search_clicked)
        self.search_button.set_border_width(5)
        
        self.configfilter_button = gtk.Button('Configure Filter')
        self.pack_end(self.configfilter_button, False, False)
        self.configfilter_button.connect("clicked", self.\
                                                    on_configure_filter_clicked)
        self.configfilter_button.set_border_width(5)
    
        self.show_all()
  
    def on_lookup_clicked(self, button):
        """
        Callback of the lookup button
        """
        self.lock()
        
        srvman = ServerManager() 
        enteredserver = self.lookupentry.get_text()
        guicontroller = GuiController()
        try:
            host, port = enteredserver.split(':', 1)
            port = int(port)
            host = guicontroller.get_host_by_name(host)
            server = srvman.getServer(host, port)
        except:
            self.parent.statusbar.progressbar.set_text('Failed to lookup server!')
            return
        #TODO: perform the lookup
        guicontroller.lookup_server(server, self.parenttab)
        
    def on_search_clicked(self, button):
        """
        Callback of the search button
        """
        Log.log.info('not yet implemented!')
        
    def on_configure_filter_clicked(self, button):
        """
        Callback of the configure filter button
        """
        Log.log.info('not yet implemented!')
        
    def lock(self):
        """
        Locks the UI-Elements for Lookup and Search so no two concurrent 
        requests can be executed!
        """
        self.search_button.set_sensitive(False)
        self.lookupbutton.set_sensitive(False)
        
    def unlock(self):
        """
        Unlocks the UI Elements for lookup and search after the request
        has finished.
        """
        self.search_button.set_sensitive(True)
        self.lookupbutton.set_sensitive(True)