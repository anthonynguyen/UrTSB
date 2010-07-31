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

import glib
import gtk

class ServerDetailBox(gtk.HBox):
    """
    The ServerDetailBox is a UI element containing a treeview to display 
    server variables and a shortinfo table with some basic server informations.
    """

    current_server = None

    def __init__(self):
        """
        Constructor
        """
        gtk.HBox.__init__(self)
        
        self.varliststore = gtk.ListStore(str, str)
        var_scrolled_window = gtk.ScrolledWindow()
        var_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        var_scrolled_window.show_all()
        varlistview = gtk.TreeView(model=self.varliststore)
        varlistview.show()
        varlistview.set_headers_clickable(True)
        var_scrolled_window.add(varlistview)
        var_scrolled_window.show()
        self.pack_start(var_scrolled_window)
        
        
        column_variable = gtk.TreeViewColumn('Variable')
        column_value = gtk.TreeViewColumn('Value')
       
        column_variable.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_variable.set_expand(True)
        column_variable.set_fixed_width(75)
        
        column_value.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_value.set_expand(True)
        column_value.set_fixed_width(75)
        
        varlistview.append_column(column_variable)
        varlistview.append_column(column_value)
        
        var_cell0=gtk.CellRendererText()
        var_cell1=gtk.CellRendererText()
        
        
        column_variable.pack_start(var_cell0, expand=True)
        column_value.pack_start(var_cell1, expand=False)
        
        column_variable.add_attribute(var_cell0, 'text', 0)
        column_value.add_attribute(var_cell1, 'text', 1)  
        
        column_variable.set_reorderable(True)
        column_value.set_reorderable(True)  
    
        # add some basic infos of the currently selected server
        infobox = gtk.VBox()
        self.pack_start(infobox, True, True)
        self.namelabel = gtk.Label('')
        
        
        self.namelabel.set_line_wrap(True)
        self.namelabel.set_use_markup(True)
        
        
        infobox.pack_start(self.namelabel, True, False)
        
        #rows, cols
        table = gtk.Table(5,2)
        infobox.pack_start(table)
        
        adresslabel = gtk.Label('Adress:')
        adresslabel.set_alignment(xalign=0, yalign=0.5)
        
        playerslabel = gtk.Label('Players:')
        playerslabel.set_alignment(xalign=0, yalign=0.5)
        
        maplabel = gtk.Label('Current Map:')
        maplabel.set_alignment(xalign=0, yalign=0.5)
        
        gametypelabel = gtk.Label('Gametype:')
        gametypelabel.set_alignment(xalign=0, yalign=0.5)
        
        pinglabel = gtk.Label('Ping:')
        pinglabel.set_alignment(xalign=0, yalign=0.5)
        
        passlabel = gtk.Label('needs Password:')
        passlabel.set_alignment(xalign=0, yalign=0.5)
        
        self.adressvaluelabel = gtk.Label()
        self.adressvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.playersvaluelabel = gtk.Label()
        self.playersvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.mapvaluelabel = gtk.Label()
        self.mapvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.gametypevaluelabel = gtk.Label()
        self.gametypevaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.pingvaluelabel = gtk.Label()
        self.pingvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.passvaluelabel = gtk.Label()
        self.passvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        table.attach(adresslabel, 0,1,0,1 )
        table.attach(playerslabel, 0,1,1,2)
        table.attach(maplabel, 0,1,2,3)
        table.attach(gametypelabel, 0,1,3,4)
        table.attach(pinglabel, 0,1,4,5)
        table.attach(passlabel, 0,1,5,6)
        
        
        table.attach(self.adressvaluelabel, 1,2,0,1 )
        table.attach(self.playersvaluelabel, 1,3,1,2)
        table.attach(self.mapvaluelabel, 1,2,2,3)
        table.attach(self.gametypevaluelabel, 1,2,3,4)
        table.attach(self.pingvaluelabel, 1,2,4,5)
        table.attach(self.passvaluelabel, 1,2,5,6)
        
        self.show_all()
        
    def setServerDetails(self, server):
        """
        Set the details of a certain server.
        
        @param server - the server which data is used to fill
                        the details
        """
        #detailstable
        self.current_server = server
        self.namelabel.set_markup('<b>' + glib.markup_escape_text(server.getName()) + '</b>')
        self.adressvaluelabel.set_text(server.getAdress())
        self.mapvaluelabel.set_text(server.getMap())
        self.gametypevaluelabel.set_text(server.getGameTypeName())
        self.playersvaluelabel.set_text(server.getPlayerString())
        self.pingvaluelabel.set_text(str(server.getPing()))
        if(server.needsPassword()):
            self.passvaluelabel.set_text('Yes')
        else: 
            self.passvaluelabel.set_text('No')
        
        #server vars treeview           
        self.varliststore.clear()
        
        vars = server.getServerVars()
        if vars:
            for key in vars.iterkeys():
                self.varliststore.append([key, vars[key]]) 
        
