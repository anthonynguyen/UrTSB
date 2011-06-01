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
from urtsb_src.filter import Filter, FilterType
from urtsb_src.globals import Globals
import gobject
import gtk
import os
import shlex
import subprocess
import thread
from connectionmanager import ConnectionManager


class GuiController(object):
    """
    Backend for the UI to perform non UI logic.
    """
    
    __shared_state = {} # borg pattern
    
    appname = Globals.app_name
    appver = Globals.app_ver
    appdesc = Globals.app_desc
    
    instance = None
    
    def __init__(self):
        self.__dict__ = self.__shared_state # borg pattern
        if not self.instance:
            self.instance = True
            
            self.urt_process = None

    def get_host_by_name(self, name):
        """
        Converts the passed hostname to a ipv4 ip adress.
        If the name already is a ipv4 ip it is returned unchanged
        
        @param name - the name for which an ip is requested
        """
        query = Q3ServerQuery()
        return query.get_host_by_name(name)

    def lookup_server(self, server, tab):
        """
        This method performs a lookup of a certain server. Its like a search
        with the adress as paremeter so it clears the serverlist on the 
        requesting tab and only adds the server object with the looked up 
        data to the list afterwards.
        
        @param server - the server to be looked up
        @param tab - the requesting tab
        """
        #clear the serverlist on the tab
        tab.serverlist.clear()
        
        #start the lookup in an extra thread using the querymanager
        qm = QueryManager()
        qm.lookup_server(server, tab)
        
        
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
        if tab:
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
        
        
    def execute_buddies_loading(self, tab, execute=False):
        """
        Starts executing the loading of the buddies
        
        @tab the tab requesting the buddylist   
        @execute - boolean value. If True immediately start a buddy search after
                   loading the buddylist   
        """
        Log.log.info('[GuiController] execute_buddies_loading called...')
        tab.clear_buddy_list()
        thread.start_new_thread(self.load_buddies, (tab,execute))
        
        
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
    
    def execute_serverlist_refresh(self, liststore, tab):
        """
        Starts the execution of the refreshe of a serverlist 
                
        @param liststore - the liststore which contains the servers to be 
                           refreshed
        @param tab - the tab requesting the refresh
        """
        Log.log.info('[GuiController] execute_serverlist_refresh called...')
        thread.start_new_thread(self.refresh_server_list, (liststore,tab))
    
                  
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

    def load_buddies(self, tab, execute):
        """
        Loads the buddylist and append the values to the treeview on the 
        passed tab 
        
        @param tab - the tab requesting the buddylist
        @execute - boolean value. If True immediately start a buddy search after
                   loading the buddylist
        """
        Log.log.debug('[GuiController] load_buddies called...')
        fm = FileManager()
        buddylist = fm.get_buddies()
        for name in buddylist:
            gobject.idle_add(tab.append_buddy_to_list, name)

        
        if execute:
            tab.filter.lock()
        
            #create a filter object
            filter = Filter(FilterType.BUDDY_FILTER, tab)
            filter.playerlist = fm.get_buddies()
            tab.set_all_buddies_to_offline()
            self.executeMasterServerQuery(filter, tab)
    
    def refresh_server_list(self, liststore, tab):
        """
        Refreshes the Serverlist of a tab
        
        @param liststore - the liststore which contains the servers to be 
                           refreshed
        @param tab - the tab requesting the refresh
        """
        Log.log.debug('[GuiController] refresh_server_list called...')
        qm = QueryManager()
        tab.set_querymanager(qm)
        qm.start_serverlist_refresh(liststore, tab)

    def loadFavorites(self, tab):
        """
        Loads the favorite server list from a file using the FileManager and
        update the serverlist on the requesting tab.
        All of this is done
        on background threads using the QueryManager
        
        @param tab - the tab requesting the favorite servers list
        """
        Log.log.debug('[GuiController] loadFavorites called...')
        gobject.idle_add(tab.clearServerList)
        qm = QueryManager()
        tab.set_querymanager(qm)
        qm.startFavoritesLoadingThread(tab)
        
    def loadRecentServer(self, tab):
        """
        Loads the list of recent servers from a file using the FileManager
        and update the serverlist on the requesting tab. All of this is done
        on background threads using the QueryManager

        
        @param tab - the tab requesting the recent server list
        """
        Log.log.debug('[GuiController] loadRecentServer called...')
        gobject.idle_add(tab.clearServerList)
        qm = QueryManager()
        tab.set_querymanager(qm)
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
        gobject.idle_add(tab.clearServerList)
        
        #perform the master server query
        qm = QueryManager()
        tab.set_querymanager(qm)
        qm.startMasterServerQueryThread(serverlistfilter, tab)



    
    def connectToServer(self, server):
        """
        Launches Urban Terror and connect to the passed server
        
        @param server - the server to connect to 
        """
        Log.log.debug('[GuiController] connectToServer called...')
        
        cm = ConnectionManager()
        cm.connectToServer(server)
        

    def send_rcon_command(self, server, command, console):
        """
        Initiates the sending of a rcon command to a server
        Launches a thread that does the rcon command sending
        
        @param server - the server the command should be send to
        @param command - the command to send
        @param console - the rcon window 
        """
        thread.start_new_thread(self.perform_rcon_command_sending, \
                                                     (server, command, console))
        
    def perform_rcon_command_sending(self, server, command, console):
        """
        This is the method that runs in a backgroundthread and sends
        a rcon command to a server
        """
        #construct the full command
        #format : 'rcon "password" command'
        rcon_cmd = 'rcon "'+server.rconpass+'" ' + command
        Log.log.debug('rcon command to send: ' + rcon_cmd)
        
        query = Q3ServerQuery()
        response = query.send_rcon_command(rcon_cmd, server)
        
        gobject.idle_add(console.add_server_response, response)
        
        