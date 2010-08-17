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

from UrTSB.flagmanager import FlagManager
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
        
        
        self.column_variable = gtk.TreeViewColumn('Variable')
        self.column_value = gtk.TreeViewColumn('Value')
       
        self.column_variable.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_variable.set_expand(True)
        self.column_variable.set_fixed_width(75)
        
        self.column_value.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_value.set_expand(True)
        self.column_value.set_fixed_width(75)
        
        varlistview.append_column(self.column_variable)
        varlistview.append_column(self.column_value)
        
        var_cell0=gtk.CellRendererText()
        var_cell1=gtk.CellRendererText()
        
        
        self.column_variable.pack_start(var_cell0, expand=True)
        self.column_value.pack_start(var_cell1, expand=False)
        
        self.column_variable.add_attribute(var_cell0, 'text', 0)
        self.column_value.add_attribute(var_cell1, 'text', 1)  
        
        self.column_variable.set_reorderable(True)
        self.column_value.set_reorderable(True)  
    
    
        # set intial values for sorting order and column
        self.sortorder = gtk.SORT_ASCENDING
        self.sortcolumn = 0
        
        self.column_variable.set_clickable(True)
        self.column_value.set_clickable(True)

        
        self.column_variable.connect('clicked', self.on_column_header_clicked, 0)  
        self.column_value.connect('clicked', self.on_column_header_clicked, 1)
    
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
        
        addresslabel = gtk.Label('Address:')
        addresslabel.set_alignment(xalign=0, yalign=0.5)
        
        playerslabel = gtk.Label('Players:')
        playerslabel.set_alignment(xalign=0, yalign=0.5)
        
        maplabel = gtk.Label('Current Map:')
        maplabel.set_alignment(xalign=0, yalign=0.5)
        
        gametypelabel = gtk.Label('Gametype:')
        gametypelabel.set_alignment(xalign=0, yalign=0.5)
        
        locationlabel = gtk.Label('Location')
        locationlabel.set_alignment(xalign=0, yalign=0.5)
        
        pinglabel = gtk.Label('Ping:')
        pinglabel.set_alignment(xalign=0, yalign=0.5)
        
        passlabel = gtk.Label('needs Password:')
        passlabel.set_alignment(xalign=0, yalign=0.5)
        
        self.addressvaluelabel = gtk.Label()
        self.addressvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.playersvaluelabel = gtk.Label()
        self.playersvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.mapvaluelabel = gtk.Label()
        self.mapvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.gametypevaluelabel = gtk.Label()
        self.gametypevaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        locationbox = gtk.HBox()
        self.locationvaluelabel = gtk.Label()
        self.locationvaluelabel.set_alignment(xalign=0, yalign=0.5)
        self.flag = gtk.Image()
        locationbox.pack_start(self.flag, False, False)
        locationbox.pack_start(self.locationvaluelabel)
        
        self.pingvaluelabel = gtk.Label()
        self.pingvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        self.passvaluelabel = gtk.Label()
        self.passvaluelabel.set_alignment(xalign=0, yalign=0.5)
        
        table.attach(addresslabel, 0,1,0,1 )
        table.attach(playerslabel, 0,1,1,2)
        table.attach(maplabel, 0,1,2,3)
        table.attach(gametypelabel, 0,1,3,4)
        table.attach(locationlabel, 0,1,4,5)
        table.attach(pinglabel, 0,1,5,6)
        table.attach(passlabel, 0,1,6,7)
        
        
        table.attach(self.addressvaluelabel, 1,2,0,1 )
        table.attach(self.playersvaluelabel, 1,3,1,2)
        table.attach(self.mapvaluelabel, 1,2,2,3)
        table.attach(self.gametypevaluelabel, 1,2,3,4)
        table.attach(locationbox, 1,2,4,5)
        table.attach(self.pingvaluelabel, 1,2,5,6)
        table.attach(self.passvaluelabel, 1,2,6,7)
        
        self.show_all()

    def reset_sort_indicators(self):
        """
        Reset all sort indicators of the table headers
        """
        self.column_variable.set_sort_indicator(False)  
        self.column_value.set_sort_indicator(False)
        
        
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
        
        self.varliststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        
        
    def setServerDetails(self, server):
        """
        Set the details of a certain server.
        
        @param server - the server which data is used to fill
                        the details
        """
        #detailstable
        self.current_server = server
        self.namelabel.set_markup('<b>' + glib.markup_escape_text(server.getName()) + '</b>')
        self.addressvaluelabel.set_text(server.getaddress())
        self.mapvaluelabel.set_text(server.getMap())
        self.gametypevaluelabel.set_text(server.getGameTypeName())
        self.playersvaluelabel.set_text(server.getPlayerString())
        
        self.locationvaluelabel.set_text('  (' + server.get_location() + ') '+\
                                         server.get_location_name())
        flagmanager = FlagManager()
        self.flag.set_from_pixbuf(flagmanager.get_flag(server.get_location()))
        
        
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
        
