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
from guicontroller import GuiController

class ServerList(gtk.ScrolledWindow):
    """
    A generic serverlist UI element. Its a treeview 
    to display the columns
    - needs pw
    - servername
    - adress
    - ping 
    - cur/max players
    - current map
    - gametype
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.ScrolledWindow.__init__(self)
        
        self.liststore = gtk.ListStore(str, str, str, int, str, str, str, object)
        
       
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.serverlistview = gtk.TreeView(model=self.liststore)
        self.serverlistview.show()
        self.serverlistview.set_headers_clickable(True)
        self.add(self.serverlistview)
        self.show()
        
        
        
        column_number = gtk.TreeViewColumn('needs PW')
        column_name = gtk.TreeViewColumn('Servername')
        column_adress = gtk.TreeViewColumn('Adress')
        column_ping = gtk.TreeViewColumn('Ping')
        column_player = gtk.TreeViewColumn('Players')
        column_map = gtk.TreeViewColumn('Map')
        column_gametype = gtk.TreeViewColumn('Gametype')
        
        #sizing
        column_number.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_number.set_expand(True)
        column_number.set_fixed_width(15)
        
        column_name.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_name.set_expand(True)
        column_name.set_fixed_width(250)
        
        column_adress.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_adress.set_expand(True)
        column_adress.set_fixed_width(75)
                
        column_ping.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_ping.set_expand(True)
        column_ping.set_fixed_width(15)
        
        column_player.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_player.set_expand(True)
        column_player.set_fixed_width(15)
        
        column_map.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_map.set_expand(True)
        column_map.set_fixed_width(75)
        
        column_gametype.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_gametype.set_expand(True)
        column_gametype.set_fixed_width(50)
        
        self.serverlistview.append_column(column_number)
        self.serverlistview.append_column(column_name)
        self.serverlistview.append_column(column_adress)
        self.serverlistview.append_column(column_ping)
        self.serverlistview.append_column(column_player)
        self.serverlistview.append_column(column_map)
        self.serverlistview.append_column(column_gametype)
        
        cell0=gtk.CellRendererText()
        cell1=gtk.CellRendererText()
        cell2=gtk.CellRendererText()
        cell3=gtk.CellRendererText()
        cell4=gtk.CellRendererText()
        cell5=gtk.CellRendererText()
        cell6=gtk.CellRendererText()
        
        column_number.pack_start(cell0, expand=False)
        column_name.pack_start(cell1, expand=True)
        column_adress.pack_start(cell2, expand=False)
        column_ping.pack_start(cell3, expand=False)
        column_player.pack_start(cell4, expand=False)
        column_map.pack_start(cell5, expand=False)
        column_gametype.pack_start(cell6, expand=False)
        
        column_number.add_attribute(cell0, 'text', 0)
        column_name.add_attribute(cell1, 'text', 1)  
        column_adress.add_attribute(cell2, 'text', 2)
        column_ping.add_attribute(cell3, 'text', 3)
        column_player.add_attribute(cell4, 'text', 4)
        column_map.add_attribute(cell5, 'text', 5)
        column_gametype.add_attribute(cell6, 'text',6)
        
     
        
        column_number.set_reorderable(True)
        column_name.set_reorderable(True)  
        column_adress.set_reorderable(True)
        column_ping.set_reorderable(True)
        column_player.set_reorderable(True)
        column_map.set_reorderable(True)
        column_gametype.set_reorderable(True)
        
        self.liststore.set_sort_column_id(3, gtk.SORT_ASCENDING)
        
        selection = self.serverlistview.get_selection()
        selection.connect('changed', self.onSelectionChanged)
        
    def onSelectionChanged(self, selection):
        """
        Callback handling the selection of a row in the serverlist.
        Triggers updating the serverdetails area of the parent tab.
        """
        
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[7]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self.parent.parent)
            #thread.start_new_thread(self.updateServerStatus, (server,))
        
    def addServer(self, server):
        """
        Adds a server to the serverlist.
        
        @param server - the server to add
        """
        
        # map needsPassword boolean to a String
        needpw = '-' # default for don't know 
        if server.needsPassword() != None:
            if server.needsPassword():
                needpw = 'yes'
            else:
                needpw = '' # just leave the cell blank if no pw required
        self.liststore.append([needpw, server.getName(), server.getAdress()
                            , server.getPing(), server.getPlayerString()
                            , server.getMap(), server.getGameTypeName()
                            , server]) 
        
        # default hardcoded sorting by ping ascending
        self.liststore.set_sort_column_id(3, gtk.SORT_ASCENDING)
        
    def clear(self):
        """
        Completely clears the serverlist.
        """
        self.liststore.clear()
