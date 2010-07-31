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
       
        
        
        column_playername = gtk.TreeViewColumn('Player')
        column_playerkills = gtk.TreeViewColumn('Kills')
        column_playerping = gtk.TreeViewColumn('Ping')
        
        column_playername.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_playername.set_expand(True)
        column_playername.set_fixed_width(150)
        
        column_playerkills.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_playerkills.set_expand(False)
        column_playerkills.set_fixed_width(50)
        
        column_playerping.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_playerping.set_expand(False)
        column_playerping.set_fixed_width(50)
        
        
        playerlistview.append_column(column_playername)
        playerlistview.append_column(column_playerkills)
        playerlistview.append_column(column_playerping)
        
        
        player_cell0=gtk.CellRendererText()
        player_cell1=gtk.CellRendererText()
        player_cell2=gtk.CellRendererText()
        
        
        column_playername.pack_start(player_cell0, expand=True)
        column_playerkills.pack_start(player_cell1, expand=False)
        column_playerping.pack_start(player_cell2, expand=False)
        
        
        column_playername.add_attribute(player_cell0, 'text', 0)
        column_playerkills.add_attribute(player_cell1, 'text', 1)  
        column_playerping.add_attribute(player_cell2, 'text', 2)
           
        column_playername.set_reorderable(True)
        column_playerkills.set_reorderable(True)  
        column_playerping.set_reorderable(True)
        
    def clear(self):
        print 'playerlist clear called'
        self.playerliststore.clear()
        
    def addPlayer(self, player):
        playername = player.getName()
        playerkills = player.getKills()
        playerping = player.getPing()
        self.playerliststore.append([playername,playerkills,playerping])