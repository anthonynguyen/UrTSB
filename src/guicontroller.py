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
from log import Log
from q3serverquery import Q3ServerQuery
from querymanager import QueryManager
from threading import Thread
import gobject
import gtk
import shlex
import subprocess
import thread






class GuiController(object):
    """
    Backend for the UI to perform non UI logic.
    """
    
    __shared_state = {} # borg pattern
    
    appname = 'UrTSB'
    appver = '0.3'
    appdesc = 'a Urban Terror Server Browser'
    
    instance = None
    
    def __init__(self):
        self.__dict__ = self.__shared_state # borg pattern
        if not self.instance:
            self.instance = True
            
            self.urt_process = None
        
    def addFavorite(self, server):
        """
        Adds a favorite server.
        
        The favorites are persisted in a CSV file.
        """
        Log.log.debug('[GuiController] addFavorite called for server with ' \
                      + 'adress ' + server.getaddress())
        fm = FileManager()
        fm.addFavorite(server)
        
    def removeFavorite(self, server):
        """
        Removes a server from the favorites list.
        """
        Log.log.debug('[GuiController] remove Favorite called for server with ' \
                      + 'adress ' + server.getaddress())
        fm = FileManager()
        fm.removeFavorite(server)

    def add_name_to_buddylist(self, name, tab):
        """
        Adds a new name to the buddylist
        
        @param name = name to add to the buddylist
        """
        Log.log.debug('[GuiController] add_name_to_buddylist called for buddy ' \
                      + 'with name ' + name)
        
        fm = FileManager()
        buddylist = fm.get_buddies()
        buddylist.append(name)
        t = Thread(target=fm.save_buddies)
        t.setDaemon(True)
        t.start()
        tab.append_buddy_to_list(name)
          
    def remove_buddy(self, name):
        """
        Removes a name from the buddylist
        
        @param name - the name to be removed from the buddylist
        """ 
        Log.log.debug('[GuiController] remove_buddy called for buddy with ' \
                      + 'name ' + name)
        
        fm = FileManager()
        thread.start_new_thread(fm.remove_buddy ,(name,)) 
        
    def removeRecent(self, server):
        """
        Removes a server from the list of recent servers
        
        @param server - server to be removed
        """
        Log.log.debug('[GuiController] removeRecent called for server with ' \
                      + 'adress ' + server.getaddress())
        
        fm = FileManager()
        fm.removeRecentServer(server)
      
    def clearRecentServers(self, tab):
        """
        clears the recent server list.
        
        @param tab - tab requesting the action
        """
        Log.log.debug('[GuiController] clearRecentServers called ')
        
        fm = FileManager()
        fm.clearRecentServerList()
        tab.clearServerList()
      
    def executeMasterServerQuery(self, serverlistfilter, tab):
        """
        Starts executing the search for game servers.
        
        @param serverlistfilter - query and filteroptions 
        @param tab - the tab on the ui that requests the serverlist
        """        
        Log.log.info('[GuiController] executeMasterServerQuery called...')
        
        tab.clearServerList()
        thread.start_new_thread(self.loadMasterServerList
                                ,(serverlistfilter
                                ,tab)) 
        
        
    def execute_buddies_loading(self, tab):
        """
        Starts executing the loading of the buddies
        
        @tab the tab requesting the buddylist        
        """
        Log.log.info('[GuiController] execute_buddies_loading called...')
        tab.clear_buddy_list()
        thread.start_new_thread(self.load_buddies, (tab,))
        
        
    def executeFavoritesLoading(self, tab):
        """
        Starts executing the loading of favorites.
        
        @tab - the tab requesting the favorites
        """
        Log.log.info('[GuiController] executeFavoritesLoading called...')
        
        tab.clearServerList()
        thread.start_new_thread(self.loadFavorites, (tab,))
        
    def executeRecentServersLoading(self, tab):
        """
        Starts executing the loading of recent servers.
        
        @tab - the tab requesting the recent servers list.
        """
        Log.log.info('[GuiController] executeRecentServersLoading called...')
        tab.clearServerList()
        thread.start_new_thread(self.loadRecentServer, (tab,))
    
                  
    def setDetailServer(self, server, tab):
        """
        Sets serverdetails on a UI tab.
        
        @param server - the server
        @param tab - the tab where the details should be set
        """     
        Log.log.debug('[GuiController] setDetailServer called...')
                                       
        thread.start_new_thread(self.updateServerDetails, (server, tab))
        
    def updateServerDetails(self, server, tab):
        """
        Requests updated status data of a certain sever
        
        @param server - the server that should be updated
        @param tab - the tab requesting the updated server data
        """
        Log.log.debug('[GuiController] updateServerDetails called...')
        query = Q3ServerQuery()
        server = query.getServerStatus(server)
        gobject.idle_add(tab.setServerdetails, server)
        
    def setWindow(self, window):
        """
        Let the gui controller know with which window it works together
        """
        self.window = window     

    def load_buddies(self, tab):
        """
        Loads the buddylist and append the values to the treeview on the 
        passed tab 
        
        @param tab - the tab requesting the buddylist
        """
        Log.log.debug('[GuiController] load_buddies called...')
        fm = FileManager()
        buddylist = fm.get_buddies()
        for name in buddylist:
            gobject.idle_add(tab.append_buddy_to_list, name)

    


    def loadFavorites(self, tab):
        """
        Loads the favorite server list from a file using the FileManager and
        update the serverlist on the requesting tab.
        All of this is done
        on background threads using the QueryManager
        
        @param tab - the tab requesting the favorite servers list
        """
        Log.log.debug('[GuiController] loadFavorites called...')
        tab.clearServerList()
        qm = QueryManager()
        qm.startFavoritesLoadingThread(tab)
        
    def loadRecentServer(self, tab):
        """
        Loads the list of recent servers from a file using the FileManager
        and update the serverlist on the requesting tab. All of this is done
        on background threads using the QueryManager

        
        @param tab - the tab requesting the recent server list
        """
        Log.log.debug('[GuiController] loadRecentServer called...')
        tab.clearServerList()
        qm = QueryManager()
        qm.startRecentServersLoadingThread(tab)

    def loadMasterServerList(self, serverlistfilter, tab):
        """
        Loads the Serverlist from the masterserver.
        This method is executed in a background thread which is triggered by 
        the executeMasterServerQuery method
        
        @param serverlistfilter - instance of the serverlistfilter profiding
                                  query and filter paramters
        @tab - the tab requesting the serverlist
        """
        Log.log.debug('[GuiController] loadMasterServerList called...')
        #clear the current serverlist
        tab.clearServerList()
        
        #perform the master server query
        qm = QueryManager()
        qm.startMasterServerQueryThread(serverlistfilter, tab)



    
    def connectToServer(self, server):
        """
        Launches Urban Terror and connect to the passed server
        
        @param server - the server to connect to 
        """
        Log.log.debug('[GuiController] connectToServer called...')
        
        #check if there is already a running process
        #if so display a dialog and inform the user
        #but do not launch a second instance
        if not None == self.urt_process:
            self.urt_process.poll()
            returncode = self.urt_process.returncode
            if None == returncode:
                
                dialog = gtk.MessageDialog(
                parent         = None,
                flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                type           = gtk.MESSAGE_INFO,
                buttons        = gtk.BUTTONS_OK,
                message_format = "Urban Terror is already running! Please exit" \
                                 + " it before launching a new instance")
                dialog.set_title('Urban Terror is already running')
                dialog.connect('response', lambda dialog, response: dialog.destroy())
                dialog.run()
                return

        
        fm = FileManager()
        
        
        #build the connect parameters
        #format of the commandline command:
        #urbanterror + connect <address> + password <pw>
        
        #get the executablename, the path and the additional commands
        #from the configuration
        config = fm.getConfiguration()
        executable = config[cfgkey.URT_EXE]
        path = config[cfgkey.URT_EXE_PATH]
        additionalcommands = config[cfgkey.URT_EXE_PARAMS]
                
        cmd = path + executable + ' + connect ' + server.getaddress()
        if server.needsPassword():
            cmd = cmd + ' + password ' + server.getPassword()
            if server.getRememberPassword():
                if server.isFavorite():
                    fm.saveFavorites()
            else:
                server.setPassword('')
        
        #add additional params    
        cmd = cmd + ' ' + additionalcommands
        
        
        #add server to recent servers list
        fm.addRecent(server)
        
        
        Log.log.info('launching UrT with cmd = ' + cmd)
        #use shlex.split to turn the command string into a sequence
        #that works with subprocess.popen
        args = shlex.split(cmd)       
        
        #finally execute the command 
        self.urt_process = subprocess.Popen(args)
        
    