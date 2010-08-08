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

from filemanager import FileManager
from log import Log
from q3serverquery import Q3ServerQuery
from querymanager import QueryManager
from threading import Thread
import gobject
import os
import thread




class GuiController(object):
    """
    Backend for the UI to perform non UI logic.
    """
    
    __shared_state = {} # borg pattern
    
    appname = 'UrTSB'
    appver = '0.2'
    appdesc = 'a Urban Terror Server Browser'
    
    def __init__(self):
        self.__dict__ = self.__shared_state # borg pattern
        
        
    def addFavorite(self, server):
        """
        Adds a favorite server.
        
        The favorites are persisted in a CSV file.
        """
        fm = FileManager()
        fm.addFavorite(server)
        
    def removeFavorite(self, server):
        """
        Removes a server from the favorites list.
        """
        fm = FileManager()
        fm.removeFavorite(server)
     
    def remove_buddy(self, name):
        """
        Removes a name from the buddylist
        
        @param name - the name to be removed from the buddylist
        """ 
        fm = FileManager()
        thread.start_new_thread(fm.remove_buddy ,(name,)) 
        
    def removeRecent(self, server):
        """
        Removes a server from the list of recent servers
        
        @param server - server to be removed
        """
        fm = FileManager()
        fm.removeRecentServer(server)
      
    def clearRecentServers(self, tab):
        """
        clears the recent server list.
        
        @param tab - tab requesting the action
        """
        fm = FileManager()
        fm.clearRecentServerList()
        tab.clearServerList()
      
    def executeMasterServerQuery(self, serverlistfilter, tab):
        """
        Starts executing the search for game servers.
        
        @param serverlistfilter - query and filteroptions 
        @param tab - the tab on the ui that requests the serverlist
        """        
        Log.log.debug('[GuiController] executeMasterServerQuery called...')
        
        tab.clearServerList()
        thread.start_new_thread(self.loadMasterServerList
                                ,(serverlistfilter
                                ,tab)) 
        
        
    def execute_buddies_loading(self, tab):
        """
        Starts executing the loading of the buddies
        
        @tab the tab requesting the buddylist        
        """
        tab.clear_buddy_list()
        thread.start_new_thread(self.load_buddies, (tab,))
        
        
    def executeFavoritesLoading(self, tab):
        """
        Starts executing the loading of favorites.
        
        @tab - the tab requesting the favorites
        """
        Log.log.debug('[GuiController] executeFavoritesLoading called...')
        
        tab.clearServerList()
        thread.start_new_thread(self.loadFavorites, (tab,))
        
    def executeRecentServersLoading(self, tab):
        """
        Starts executing the loading of recent servers.
        
        @tab - the tab requesting the recent servers list.
        """
        Log.log.debug('[GuiController] executeRecentServersLoading called...')
        tab.clearServerList()
        thread.start_new_thread(self.loadRecentServer, (tab,))
    
                  
    def setDetailServer(self, server, tab):
        """
        Sets serverdetails on a UI tab.
        
        @param server - the server
        @param tab - the tab where the details should be set
        """                                    
        thread.start_new_thread(self.updateServerDetails, (server, tab))
        
    def updateServerDetails(self, server, tab):
        """
        Requests updated status data of a certain sever
        
        @param server - the server that should be updated
        @param tab - the tab requesting the updated server data
        """
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
        fm = FileManager()
        buddylist = fm.get_buddies()
        for name in buddylist:
            gobject.idle_add(tab.append_buddy_to_list, name)

    
    def add_name_to_buddylist(self, name, tab):
        """
        Adds a new name to the buddylist
        
        @param name = name to add to the buddylist
        """
        fm = FileManager()
        buddylist = fm.get_buddies()
        buddylist.append(name)
        t = Thread(target=fm.save_buddies)
        t.setDaemon(True)
        t.start()
        tab.append_buddy_to_list(name)
        

    def loadFavorites(self, tab):
        """
        Loads the favorite server list from a file using the FileManager and
        update the serverlist on the requesting tab.
        All of this is done
        on background threads using the QueryManager
        
        @param tab - the tab requesting the favorite servers list
        """

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
        fm = FileManager()
        
        
        #build the connect parameters
        #format of the commandline command:
        #urbanterror + connect <address> + password <pw>
        
        #get the executablename, the path and the additional commands
        #from the configuration
        config = fm.getConfiguration()
        executable = config['urt_executable']
        path = config['path_to_executable']
        additionalcommands = config['additional_commands']
                
        cmd = path + executable + ' + connect ' + server.getaddress()
        if server.needsPassword():
            cmd = cmd + ' + password ' + server.getPassword()
            if server.getRememberPassword():
                if server.isFavorite():
                    fm.saveFavorites()
            else:
                server.setPassword('')
        
        fm.addRecent(server)
            
        cmd = cmd + ' ' + additionalcommands
        #finally execute the command
        
        Log.log.info('launching UrT with cmd = ' + cmd)
        os.popen(cmd) 
        
    