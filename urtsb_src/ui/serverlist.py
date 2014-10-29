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




from urtsb_src.flagmanager import FlagManager
from urtsb_src.globals import Globals
from urtsb_src.guicontroller import GuiController
from urtsb_src.ui.passworddialog import PasswordDialog, PassDialogType
from urtsb_src.ui.rconpassdialog import RconPassDialog
import gtk



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
        lock_image.set_from_file(Globals.icon_dir+'/lock.png')
        self.lock_pixbuf = lock_image.get_pixbuf()
        
        not_locked = gtk.Image()
        self.not_locked_pixbuf = not_locked.get_pixbuf()
        
        self.parenttab = parenttab
        
        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str, str,\
                                                str, int, str, str, str, object)
        
       
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.serverlistview = gtk.TreeView(model=self.liststore)
        self.serverlistview.show()
        self.serverlistview.set_headers_clickable(True)
        self.add(self.serverlistview)
        self.show()
        
        
        
        self.column_pw = gtk.TreeViewColumn('pw')
        self.column_flag = gtk.TreeViewColumn('')
        self.column_name = gtk.TreeViewColumn('Servername')
        self.column_version = gtk.TreeViewColumn('Version')
        self.column_address = gtk.TreeViewColumn('Address')
        self.column_ping = gtk.TreeViewColumn('Ping')
        self.column_player = gtk.TreeViewColumn('Players')
        self.column_map = gtk.TreeViewColumn('Map')
        self.column_gametype = gtk.TreeViewColumn('Gametype')
        
        #sizing
        self.column_pw.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_pw.set_expand(False)
        self.column_pw.set_fixed_width(30)
        
        #self.column_flag.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_flag.set_expand(False)
        #self.column_flag.set_fixed_width(30)
        
        self.column_name.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_name.set_expand(True)
        self.column_name.set_fixed_width(235)

        self.column_version.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column_version.set_expand(True)
        self.column_version.set_fixed_width(15)
        
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
        
        self.serverlistview.append_column(self.column_pw)
        self.serverlistview.append_column(self.column_flag)
        self.serverlistview.append_column(self.column_name)
        self.serverlistview.append_column(self.column_version)
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
        cell8=gtk.CellRendererText()
        
        self.column_pw.pack_start(cell0, expand=False)
        self.column_flag.pack_start(cell1, expand=False)
        self.column_name.pack_start(cell2, expand=True)
        self.column_version.pack_start(cell3, expand=True)
        self.column_address.pack_start(cell4, expand=False)
        self.column_ping.pack_start(cell5, expand=False)
        self.column_player.pack_start(cell6, expand=False)
        self.column_map.pack_start(cell7, expand=False)
        self.column_gametype.pack_start(cell8, expand=False)
        
        self.column_pw.add_attribute(cell0, 'pixbuf', 0)
        self.column_flag.add_attribute(cell1, 'pixbuf', 1)
        self.column_name.add_attribute(cell2, 'text', 2)
        self.column_version.add_attribute(cell3, 'text', 3)
        self.column_address.add_attribute(cell4, 'text', 4)
        self.column_ping.add_attribute(cell5, 'text', 5)
        self.column_player.add_attribute(cell6, 'text', 6)
        self.column_map.add_attribute(cell7, 'text', 7)
        self.column_gametype.add_attribute(cell8, 'text', 8)
        
        self.column_pw.set_clickable(True)
        self.column_name.set_clickable(True)
        self.column_version.set_clickable(True)
        self.column_address.set_clickable(True)
        self.column_ping.set_clickable(True)
        self.column_player.set_clickable(True)
        self.column_map.set_clickable(True)
        self.column_gametype.set_clickable(True)
        
        self.column_pw.connect('clicked', self.on_table_column_clicked, 0)
        self.column_name.connect('clicked', self.on_table_column_clicked, 2)  
        self.column_version.connect('clicked', self.on_table_column_clicked, 3)
        self.column_address.connect('clicked', self.on_table_column_clicked, 4)
        self.column_ping.connect('clicked', self.on_table_column_clicked, 5)
        self.column_player.connect('clicked', self.on_table_column_clicked, 6)
        self.column_map.connect('clicked', self.on_table_column_clicked, 7)
        self.column_gametype.connect('clicked', self.on_table_column_clicked, 8)
        
     
        
        self.column_pw.set_reorderable(True)
        self.column_flag.set_reorderable(True)
        self.column_name.set_reorderable(True)
        self.column_version.set_reorderable(True)
        self.column_address.set_reorderable(True)
        self.column_ping.set_reorderable(True)
        self.column_player.set_reorderable(True)
        self.column_map.set_reorderable(True)
        self.column_gametype.set_reorderable(True)
        
        # set intial values for sorting order and column
        self.sortorder = gtk.SORT_ASCENDING
        self.sortcolumn = 5
        # and apply sorting
        self.liststore.set_sort_column_id(self.sortcolumn, self.sortorder)
        self.column_ping.set_sort_order(self.sortorder)
        self.column_ping.set_sort_indicator(True)
        
        selection = self.serverlistview.get_selection()
        selection.connect('changed', self.onSelectionChanged)
        
        self.serverlistview.connect('row-activated', self.on_row_double_clickdef)
        self.serverlistview.connect('button-press-event', \
                                            self.on_treeview_button_press_event)
        
        self.initialize_context_menu()
    
    def reset_sort_indicators(self):
        """
        Reset all sort indicators of the table headers
        """
        self.column_pw.set_sort_indicator(False)
        self.column_name.set_sort_indicator(False)
        self.column_version.set_sort_indicator(False)
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
        
        if colnum == 0:
            self.liststore.set_sort_func(self.sortcolumn, self.pw_sorter, colnum)
        elif colnum == 6:
            self.liststore.set_sort_func(self.sortcolumn, self.player_sorter, colnum)

        self.liststore.set_sort_column_id(self.sortcolumn, self.sortorder)
    
    def pw_sorter(self, liststr, iter1, iter2, user_data):
        """
        Sorts servers based on their passworded status
        """
        colnum = 0
        val1 = (1 if liststr.get_value(iter1, colnum) == self.lock_pixbuf else 0)
        val2 = (1 if liststr.get_value(iter2, colnum) == self.lock_pixbuf else 0)
        return cmp(val1, val2)

    def player_sorter(self, liststr, iter1, iter2, user_data):
        """
        Sorting players by its integer value not by string
        Contributed by Phoenix
        """
        #5th row (for now) is the player numbers (what we want to sort on)
        colnum = 6
        if user_data != None:
            colnum = int(user_data)
        #Get the value of the 'colnum' column in the first row
        val1 = liststr.get_value(iter1, colnum)
        val2 = liststr.get_value(iter2, colnum)
        if(type(val1) == str):
        #Check if the type is a string, if so, sort on the first part until the slash ('/'), casted to int
            val1 = int(val1[:val1.find('/')])
        if(type(val2) == str):
            val2 = int(val2[:val2.find('/')])
        #return the comparison of the first and the second
        return cmp(val1,val2)
        
    def on_row_double_clickdef(self, treeview, path, view_column):
        """
        Callback for the row-activate signal (double-click, enter...)
        """    
        row =  self.liststore[path]
        server = row[9]
        gui = GuiController()
        
        if server:
            if server.needsPassword():
                passdialog = PasswordDialog(server, PassDialogType\
                                                               .SERVER_PASSWORD)
                passdialog.run()
            else:
                gui.connectToServer(server)
        
    def onSelectionChanged(self, selection):
        """
        Callback handling the selection of a row in the serverlist.
        Triggers updating the serverdetails area of the parent tab.
        """
        
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[9]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self.parenttab)
           
        
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
        
        self.liststore.append([needpw, flag, server.getName(), server.getVersionString()
                            , server.getaddress()
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
        
    def initialize_context_menu(self):
        """
        Creates a contextmenu
        """
        self.context_menu = gtk.Menu()
        
        
        connect_menu_item = gtk.MenuItem('connect')
        self.context_menu.add(connect_menu_item)
        connect_menu_item.connect('activate', self.on_connect_menu_item_clicked)
        
        separator = gtk.SeparatorMenuItem()
        self.context_menu.add(separator)
        
        #differ between remove and add favorite menuitem.
        #on the favorites tab the menuitem will be remove
        #all other tabs the add menuitem should be displayed
        if self.parenttab.__class__.__name__ == 'FavoritesTab':
            rem_fav_menu_item = gtk.MenuItem('remove from favorites')
            self.context_menu.add(rem_fav_menu_item)
            rem_fav_menu_item.connect('activate', \
                                           self.on_remove_fav_menu_item_clicked)
        else:
            add_fav_menu_item = gtk.MenuItem('add to favorites')
            self.context_menu.add(add_fav_menu_item)
            add_fav_menu_item.connect('activate', \
                                              self.on_add_fav_menu_item_clicked)
        
        separator = gtk.SeparatorMenuItem()
        self.context_menu.add(separator)
        
        rcon_menu_item = gtk.MenuItem('open RCON console')
        self.context_menu.add(rcon_menu_item)
        rcon_menu_item.connect('activate', self.on_context_rcon_pressed)
        
        separator = gtk.SeparatorMenuItem()
        self.context_menu.add(separator)
        
        #copy to clipboard functions
        copy_address_menu_item = gtk.MenuItem('copy address to clipboard')
        self.context_menu.add(copy_address_menu_item)
        copy_address_menu_item.connect('activate',\
                                      self.on_copy_address_to_clipboard_clicked)
        
        copy_name_and_address_menu_item = gtk.MenuItem('copy name and address '\
                                                               + 'to clipboard')
        self.context_menu.add(copy_name_and_address_menu_item)
        copy_name_and_address_menu_item.connect('activate',\
                             self.on_copy_name_and_address_to_clipboard_clicked)
        
        
        self.context_menu.show_all()
 
    def on_connect_menu_item_clicked(self, menuitem):
        """
        Callback of the 'connect' menuitem
        """
        server = self.get_selected_server()
        gc = GuiController()
        gc.connectToServer(server)
 
    def on_remove_fav_menu_item_clicked(self, menuitem):
        """
        Callback of the 'remove from favorites' menu item
        """
        #get the selected row of the serverlist
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            server = self.liststore.get_value(iter, 9)
            gc = GuiController()
            gc.removeFavorite(server)
            self.liststore.remove(iter)
 
 
    def on_copy_address_to_clipboard_clicked(self, menuitem):
        """
        Callback method of the "copy address to clipboard" menuitem
        """
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            server = self.liststore.get_value(iter, 9)
            clipboard = gtk.clipboard_get()
            clipboard.set_text(server.getaddress())
            clipboard.store()
    
    def on_copy_name_and_address_to_clipboard_clicked(self, menuitem):
        """
        Callback method of the "copy name and address to clipboard" menuitem
        """
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            server = self.liststore.get_value(iter, 9)
            clipboard = gtk.clipboard_get()
            copytext = server.getaddress() + ' - ' + server.getName() 
            clipboard.set_text(copytext)
            clipboard.store()
 
    def on_add_fav_menu_item_clicked(self, menuitem):
        """
        Callback for the 'add to favorites' context menu item
        """    
        server = self.get_selected_server()
        if server:
            gc = GuiController()
            gc.addFavorite(server)
 
    def on_context_rcon_pressed(self, menuitem):
        """
        Callback for the context menu item 'open RCON console'
        """
        server = self.get_selected_server()
        if server:
            RconPassDialog(server)
             
    def get_selected_server(self):
        """
        Returns the server object for the selcted row of the serverlist
        
        @return the serverobject of the selected row
        """        
        #get the selected row of the serverlist
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            server = self.liststore.get_value(iter, 9)
            return server
        return None
                
    def update_selected_row(self, server):
        selection = self.serverlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            self.liststore.set_value(iter, 4, server.getVersionString())
            self.liststore.set_value(iter, 5, server.getPing())
            self.liststore.set_value(iter, 6, server.getPlayerString())
            self.liststore.set_value(iter, 7, server.getMap())
            self.liststore.set_value(iter, 8, server.getGameTypeName())
            
    def on_treeview_button_press_event(self, treeview, event):
        """
        Callback for mouse-clicks to create a context menu on right mouse 
        button pressed
        """
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.context_menu.popup( None, None, None, event.button, time)
                
            return True
