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

class PlayerList(gtk.ScrolledWindow):
    """
    A UI-Element for displaying players on a game server using a GTK Treeview.
    Displayed data is the playername, the kills and the ping of the player.
    """


    def __init__(self):
        """
        Constructor
        """
        
        
        gtk.ScrolledWindow.__init__(self)
        self.playerliststore = gtk.ListStore(str, int, int)

        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.show_all()
        playerlistview = gtk.TreeView(model=self.playerliststore)
        playerlistview.show()
        playerlistview.set_headers_clickable(True)
        self.add(playerlistview)
        self.show()
       
        
        
        self.column_playername = gtk.TreeViewColumn('Player')
        self.column_playerkills = gtk.TreeViewColumn('Kills')
        self.column_playerping = gtk.TreeViewColumn('Ping')
        
        
        
        self.column_playername.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_playername.set_expand(True)
        self.column_playername.set_fixed_width(150)
        
        self.column_playerkills.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_playerkills.set_expand(False)
        self.column_playerkills.set_fixed_width(50)
        
        self.column_playerping.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_playerping.set_expand(False)
        self.column_playerping.set_fixed_width(50)
        
        
        playerlistview.append_column(self.column_playername)
        playerlistview.append_column(self.column_playerkills)
        playerlistview.append_column(self.column_playerping)
        
        
        player_cell0=gtk.CellRendererText()
        player_cell1=gtk.CellRendererText()
        player_cell2=gtk.CellRendererText()
        
        
        self.column_playername.pack_start(player_cell0, expand=True)
        self.column_playerkills.pack_start(player_cell1, expand=False)
        self.column_playerping.pack_start(player_cell2, expand=False)
        
        
        self.column_playername.add_attribute(player_cell0, 'text', 0)
        self.column_playerkills.add_attribute(player_cell1, 'text', 1)  
        self.column_playerping.add_attribute(player_cell2, 'text', 2)
           
        self.column_playername.set_reorderable(True)
        self.column_playerkills.set_reorderable(True)  
        self.column_playerping.set_reorderable(True)
        
        #sortingoptions
        self.sortorder = gtk.SORT_DESCENDING
        self.sortcolumn = 0
        
        
        self.column_playername.set_clickable(True)
        self.column_playerkills.set_clickable(True)
        self.column_playerping.set_clickable(True)
        
        self.column_playername.connect('clicked', self.on_column_header_clicked, 0)  
        self.column_playerkills.connect('clicked', self.on_column_header_clicked, 1)
        self.column_playerping.connect('clicked', self.on_column_header_clicked, 2)
     
     
    def reset_sort_indicators(self):
        """
        Reset all sort indicators of the table headers
        """
        self.column_playername.set_sort_indicator(False)  
        self.column_playerkills.set_sort_indicator(False)
        self.column_playerping.set_sort_indicator(False)
        
        
    def on_column_header_clicked(self, treecolumn, colnum):
        """
        Callback for the table header buttons.
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
        
        self.playerliststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        
    def clear(self):
        self.playerliststore.clear()
        
    def addPlayer(self, player):
        playername = player.getName()
        playerkills = player.getKills()
        playerping = player.getPing()
        self.playerliststore.append([playername,playerkills,playerping])