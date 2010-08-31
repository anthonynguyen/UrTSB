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



from passworddialog import PasswordDialog
from urtsb_src.filemanager import FileManager, cfgkey
from urtsb_src.guicontroller import GuiController
import gtk
from urtsb_src.ui.passworddialog import PassDialogType

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
                passdialog = PasswordDialog(server,\
                                                 PassDialogType.SERVER_PASSWORD)
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
        
    def abort_current_task(self):
        """
        Aborts a current proccessed task (query/search/refresh)
        """  
        if self.qm: 
            self.qm.abort_current_task()
        
    def set_querymanager(self, querymanager):
        """
        Sets the querymanager that currently executes a requested task for 
        a tab. Needed to abort this task. Also unlocks the abort button
        """
        self.qm = querymanager
        self.statusbar.unlock()
