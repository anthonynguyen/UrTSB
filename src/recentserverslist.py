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

from serverlist import ServerList
import gtk

class RecentServersList(ServerList):
    """
    This is a extension to the default ServerList class of UrTSB for use
    in the Recent Server tab. It has two extra columns: number of connections
    and date of last connection.
    """


    def __init__(self):
        """
        Constructor
        """
        ServerList.__init__(self)
        
        self.liststore = gtk.ListStore(str, str, str, int, str, str, str, object, int, str)
        
        self.serverlistview.set_model(self.liststore)
        
        column_connections = gtk.TreeViewColumn('Connections')
        column_lastconnection = gtk.TreeViewColumn('Last Connection')
        
        column_connections.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_connections.set_expand(True)
        column_connections.set_fixed_width(30)
        
        column_lastconnection.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_lastconnection.set_expand(True)
        column_lastconnection.set_fixed_width(75)
        
        self.serverlistview.append_column(column_connections)
        self.serverlistview.append_column(column_lastconnection)
        
        cell8=gtk.CellRendererText()
        cell9=gtk.CellRendererText()
        
        column_connections.pack_start(cell8, expand=False)
        column_lastconnection.pack_start(cell9, expand=False)
        
        column_connections.add_attribute(cell8, 'text', 8)
        column_lastconnection.add_attribute(cell9, 'text',9)
        
        column_connections.set_reorderable(True)
        column_lastconnection.set_reorderable(True)  
        
        self.show_all()

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
                            , server, server.getConnections(), server.getLastConnect()]) 
        
        # default hardcoded sorting by last connection descending
        self.liststore.set_sort_column_id(9, gtk.SORT_DESCENDING)
        
                
        