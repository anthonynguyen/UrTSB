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
import sys
from flagmanager import FlagManager

class ServerList(gtk.ScrolledWindow):
    """
    A generic serverlist UI element. Its a treeview 
    to display the columns
    - needs pw
    - servername
    - address
    - ping 
    - cur/max players
    - current map
    - gametype
    """


    def __init__(self, parenttab):
        """
        Constructor
        """
        gtk.ScrolledWindow.__init__(self)
        lock_image = gtk.Image()
        lock_image.set_from_file(sys.path[0] + '/lock.png')
        self.lock_pixbuf = lock_image.get_pixbuf()
        
        not_locked = gtk.Image()
        self.not_locked_pixbuf = not_locked.get_pixbuf()
        
        self.parenttab = parenttab
        
        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str, \
                                                str, int, str, str, str, object)
        
       
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.serverlistview = gtk.TreeView(model=self.liststore)
        self.serverlistview.show()
        self.serverlistview.set_headers_clickable(True)
        self.add(self.serverlistview)
        self.show()
        
        
        
        self.column_number = gtk.TreeViewColumn('PW')
        self.column_flag = gtk.TreeViewColumn('')
        self.column_name = gtk.TreeViewColumn('Servername')
        self.column_address = gtk.TreeViewColumn('Address')
        self.column_ping = gtk.TreeViewColumn('Ping')
        self.column_player = gtk.TreeViewColumn('Players')
        self.column_map = gtk.TreeViewColumn('Map')
        self.column_gametype = gtk.TreeViewColumn('Gametype')
        
        #sizing
        self.column_number.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_number.set_expand(False)
        self.column_number.set_fixed_width(30)
        
        #self.column_flag.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_flag.set_expand(False)
        #self.column_flag.set_fixed_width(30)
        
        self.column_name.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_name.set_expand(True)
        self.column_name.set_fixed_width(250)
        
        self.column_address.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_address.set_expand(True)
        self.column_address.set_fixed_width(75)
                
        self.column_ping.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_ping.set_expand(True)
        self.column_ping.set_fixed_width(15)
        
        self.column_player.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_player.set_expand(True)
        self.column_player.set_fixed_width(15)
        
        self.column_map.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_map.set_expand(True)
        self.column_map.set_fixed_width(75)
        
        self.column_gametype.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_gametype.set_expand(True)
        self.column_gametype.set_fixed_width(50)
        
        self.serverlistview.append_column(self.column_number)
        self.serverlistview.append_column(self.column_flag)
        self.serverlistview.append_column(self.column_name)
        self.serverlistview.append_column(self.column_address)
        self.serverlistview.append_column(self.column_ping)
        self.serverlistview.append_column(self.column_player)
        self.serverlistview.append_column(self.column_map)
        self.serverlistview.append_column(self.column_gametype)
        
        cell0=gtk.CellRendererPixbuf()
        cell1=gtk.CellRendererPixbuf()
        cell2=gtk.CellRendererText()
        cell3=gtk.CellRendererText()
        cell4=gtk.CellRendererText()
        cell5=gtk.CellRendererText()
        cell6=gtk.CellRendererText()
        cell7=gtk.CellRendererText()
        
        self.column_number.pack_start(cell0, expand=False)
        self.column_flag.pack_start(cell1, expand=False)
        self.column_name.pack_start(cell2, expand=True)
        self.column_address.pack_start(cell3, expand=False)
        self.column_ping.pack_start(cell4, expand=False)
        self.column_player.pack_start(cell5, expand=False)
        self.column_map.pack_start(cell6, expand=False)
        self.column_gametype.pack_start(cell7, expand=False)
        
        self.column_number.add_attribute(cell0, 'pixbuf', 0)
        self.column_flag.add_attribute(cell1, 'pixbuf', 1)
        self.column_name.add_attribute(cell2, 'text', 2)  
        self.column_address.add_attribute(cell3, 'text', 3)
        self.column_ping.add_attribute(cell4, 'text', 4)
        self.column_player.add_attribute(cell5, 'text', 5)
        self.column_map.add_attribute(cell6, 'text', 6)
        self.column_gametype.add_attribute(cell7, 'text',7)
        
        self.column_name.set_clickable(True)
        self.column_address.set_clickable(True)
        self.column_ping.set_clickable(True)
        self.column_player.set_clickable(True)
        self.column_map.set_clickable(True)
        self.column_gametype.set_clickable(True)
        
        
        self.column_name.connect('clicked', self.on_table_column_clicked, 2)  
        self.column_address.connect('clicked', self.on_table_column_clicked, 3)
        self.column_ping.connect('clicked', self.on_table_column_clicked, 4)
        self.column_player.connect('clicked', self.on_table_column_clicked, 5)
        self.column_map.connect('clicked', self.on_table_column_clicked, 6)
        self.column_gametype.connect('clicked', self.on_table_column_clicked,7)
        
     
        
        self.column_number.set_reorderable(True)
        self.column_flag.set_reorderable(True)
        self.column_name.set_reorderable(True)  
        self.column_address.set_reorderable(True)
        self.column_ping.set_reorderable(True)
        self.column_player.set_reorderable(True)
        self.column_map.set_reorderable(True)
        self.column_gametype.set_reorderable(True)
        
        # set intial values for sorting order and column
        self.sortorder = gtk.SORT_ASCENDING
        self.sortcolumn = 4
        # and apply sorting
        self.liststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        self.column_ping.set_sort_order(self.sortorder)
        self.column_ping.set_sort_indicator(True)
        
        selection = self.serverlistview.get_selection()
        selection.connect('changed', self.onSelectionChanged)
    
    def reset_sort_indicators(self):
        """
        Reset all sort indicators of the table headers
        """
        self.column_name.set_sort_indicator(False)  
        self.column_address.set_sort_indicator(False)
        self.column_ping.set_sort_indicator(False)
        self.column_player.set_sort_indicator(False)
        self.column_map.set_sort_indicator(False)
        self.column_gametype.set_sort_indicator(False)
        
    def on_table_column_clicked(self, treecolumn, colnum):    
        """
        Callback for the headers of sortable columns.
        Performs sorting.
        """
    
        #reset all indicators before sorting new
        self.reset_sort_indicators()
    
        #check sort order to apply
        #if the the clicked treecolumn is the current sorted column
        #the sort order needs to be changed:
        if self.sortcolumn == colnum:
            if treecolumn.get_sort_order() == gtk.SORT_ASCENDING:
                treecolumn.set_sort_order(gtk.SORT_DESCENDING)
            else:
                treecolumn.set_sort_order(gtk.SORT_ASCENDING)
        else:
            treecolumn.set_sort_order(gtk.SORT_ASCENDING)
        
        treecolumn.set_sort_indicator(True)
        self.sortorder = treecolumn.get_sort_order()
        self.sortcolumn = colnum
        
        self.liststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        
    def onSelectionChanged(self, selection):
        """
        Callback handling the selection of a row in the serverlist.
        Triggers updating the serverdetails area of the parent tab.
        """
        
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[8]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self.parenttab)
            #thread.start_new_thread(self.updateServerStatus, (server,))
        
    def addServer(self, server):
        """
        Adds a server to the serverlist.
        
        @param server - the server to add
        """
        
        # map needsPassword boolean to a image
        needpw = self.not_locked_pixbuf  # default for don't know 
        if server.needsPassword() != None:
            if server.needsPassword():
                needpw = self.lock_pixbuf
            else:
                needpw = self.not_locked_pixbuf # just leave the cell blank if no pw required
               
        flagmanager = FlagManager() 
        flag = flagmanager.get_flag(server.get_location())
        
        self.liststore.append([needpw, flag, server.getName(), server.getaddress()
                            , server.getPing(), server.getPlayerString()
                            , server.getMap(), server.getGameTypeName()
                            , server]) 
        
        # default hardcoded sorting by ping ascending
        self.liststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        
    def clear(self):
        """
        Completely clears the serverlist.
        """
        self.liststore.clear()
        
        
    def update_selected_row(self, server):
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            self.liststore.set_value(iter, 4, server.getPing())
            self.liststore.set_value(iter, 5, server.getPlayerString())
            self.liststore.set_value(iter, 6, server.getMap())
            self.liststore.set_value(iter, 7, server.getGameTypeName())
