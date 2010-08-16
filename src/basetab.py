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
from filemanager import FileManager, cfgkey
from guicontroller import GuiController
from passworddialog import PasswordDialog
import gtk

class BaseTab(gtk.VBox):
    """
    This class implements general features common to all UrTSB tabs with 
    server lists (serverlist, favorites, buddies) 
    
    
    """


    def __init__(self):
        """
        Constructor
        """
        
    def addServer(self, server):
        """
        Adds a server to the embedded serverlist
        
        @param server - the server to add
        """
        self.serverlist.addServer(server)
    
    def clearServerList(self):
        """
        Clears the embedded serverlist
        """
        self.serverlist.clear()        
        
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
        
    def setServerdetails(self, server):
        """
        Set/Update the serverdetails in the embedded serverdetails area
        """
        
        # clear and afterwards set the playerlist
        self.playerlist.clear()
        for player in server.getPlayerList():
            self.playerlist.addPlayer(player)
        
        # set the other serverdetail            
        self.detailsbox.setServerDetails(server) 
        # update row in list
        # but only if the corresponding option is True
        fm = FileManager()
        config = fm.getConfiguration()
        if 'True' == config[cfgkey.OPT_UPDATE_SL_ROW]: 
            self.serverlist.update_selected_row(server)    

    def onRefreshButtonClicked(self, widget):
        """
        Callback for refreshing the current selected server
        """
        
        selection = self.serverlist.serverlistview.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[8]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, self)

    def onAddFavButtonClicked(self, widget):   
        """
        Callback to handle adding a favorite
        """
        server = self.detailsbox.current_server
        gui = GuiController()
        gui.addFavorite(server)
