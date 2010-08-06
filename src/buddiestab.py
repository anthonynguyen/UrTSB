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

from addbuddydialog import AddBuddyDialog
from buddiesfilter import BuddiesFilter
from guicontroller import GuiController
from passworddialog import PasswordDialog
from playerlist import PlayerList
from serverdetailbox import ServerDetailBox
from serverlist import ServerList
from statusbar import StatusBar
import gtk

class BuddiesTab(gtk.VBox):
    """
    This is the gui tab for the buddylist feature
    """


    def __init__(self):
        """
        Constructor
        """
        
        gtk.VBox.__init__(self)
        
        mainbox = gtk.HBox()
        
        self.pack_start(mainbox)
        
        
        buddieslistview = self.create_buddy_list_view()
        mainbox.pack_start(buddieslistview, False, False)
        
        
        serverlistbox = gtk.VBox()
        mainbox.pack_start(serverlistbox)
        
        self.filter = BuddiesFilter()
        self.filter.show()
        
        serverlistbox.pack_start(self.filter, False, False)
        
        # top pane area 
        paned = gtk.VPaned() 
        paned.show()
        serverlistbox.pack_start(paned)   
        
        
        # bottom add a statusbar
        self.statusbar = StatusBar()
        serverlistbox.pack_start(self.statusbar, False, False)
        
        # serverlist window
        self.serverlist = ServerList()
        paned.pack1(self.serverlist, True, False)
        #paned.add1(self.serverlist)
        
        
        # bottom panearea
        bottompane = gtk.HPaned()
        paned.pack2(bottompane, True, False)
        #paned.add2(bottompane)
        
        #left box
        self.playerlist = PlayerList()
        bottompane.pack1(self.playerlist, False, False)
        
        
        
        #right box
        self.detailsbox = ServerDetailBox()
        vbox = gtk.VBox()
        
        
        bottompane.pack2(vbox, True, False)
        
      
        buttonbox = gtk.HBox()
        #self.detailsbox.pack_start(buttonbox, False, False)
        vbox.pack_start(buttonbox, False, False)
        vbox.pack_start(self.detailsbox)
        
        
        refresh_button = gtk.Button('Refresh')
        refreshimage = gtk.Image()
        refreshimage.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_BUTTON)
        refresh_button.set_image(refreshimage)
        
        connect_button = gtk.Button('Connect')
        connectimage = gtk.Image()
        connectimage.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)
        connect_button.set_image(connectimage)
        
        removefav_button = gtk.Button('Remove from Favorites')
        removeimage = gtk.Image()
        removeimage.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_BUTTON)
        removefav_button.set_image(removeimage)
        
        
        buttonbox.pack_start(refresh_button, True, True)
        buttonbox.pack_start(connect_button, True, True)
        buttonbox.pack_start(removefav_button, False, False)
#       refresh_button.connect("clicked", self.onRefreshButtonClicked)
#       removefav_button.connect("clicked", self.onRemoveFavoriteClicked)
#       connect_button.connect("clicked", self.connect_button_clicked)
        
        self.show_all()
        
        
        
    def connect_button_clicked(self, widget):
        """
        Callback of the connect button
        """
        gui = GuiController()
        server = self.detailsbox.current_server
        if server:
            if server.needsPassword():
                passdialog = PasswordDialog(server)
                passdialog.run()
            else:
                gui.connectToServer(server)
       
    def onAddFavButtonClicked(self, widget):   
        """
        Callback to adding the selected server to the favorites
        """
        server = self.detailsbox.current_server
        gui = GuiController()
        gui.addFavorite(server)
       
    def onRefreshButtonClicked(self, widget):
        """
        Callback for refreshing the current selected server
        """
        
        selection = self.serverlist.serverlistview.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[7]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self)
            
    def create_buddy_list_view(self):
        """
        Builds the gui elements for the buddylist
        """
        
        buddybox = gtk.VBox()
                
        scrolled_window = gtk.ScrolledWindow()
        buddybox.pack_start(scrolled_window)
        self.buddyliststore = gtk.ListStore(str)
        

        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        
        buddylistview = gtk.TreeView(model=self.buddyliststore)
        buddylistview.show()
        buddylistview.set_headers_clickable(True)
        scrolled_window.add(buddylistview)
        
        column_buddyname = gtk.TreeViewColumn('Buddy')
        buddylistview.append_column(column_buddyname)
        
        column_buddyname.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        column_buddyname.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column_buddyname.set_expand(False)
        column_buddyname.set_fixed_width(100)
        
        
        player_cell0=gtk.CellRendererText()
        
        column_buddyname.pack_start(player_cell0, expand=True)
        
        column_buddyname.add_attribute(player_cell0, 'text', 0)
        
        
        buttonbox = gtk.HBox()
        buddybox.pack_start(buttonbox, False, False)
        add_button = gtk.Button('Add Buddy')
        add_button.connect("clicked", self.on_add_buddy_clicked)
        
        
        remove_button = gtk.Button('Remove Selected')
        
        buttonbox.pack_start(add_button, True, True)
        buttonbox.pack_start(remove_button, True, True)
        
        buddybox.show_all()
        
        return buddybox
    
    def on_add_buddy_clicked(self, button):
        """
        Callback for the add buddy button. Opens the dialog
        to add a buddy
        """
        add_dialog = AddBuddyDialog()
        add_dialog.run()