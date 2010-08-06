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
from q3serverquery import Q3ServerQuery
import gobject
import os
import thread
from querymanager import QueryManager




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
        print 'search...'
        
        tab.clearServerList()
        thread.start_new_thread(self.loadMasterServerList
                                ,(serverlistfilter
                                ,tab)) 
        
    def executeFavoritesLoading(self, tab):
        """
        Starts executing the loading of favorites.
        
        @tab - the tab requesting the favorites
        """
        print 'load favs...'
        tab.clearServerList()
        thread.start_new_thread(self.loadFavorites, (tab,))
        
    def executeRecentServersLoading(self, tab):
        """
        Starts executing the loading of recent servers.
        
        @tab - the tab requesting the recent servers list.
        """
        print 'load recent servers list...'
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
        print 'load_serverlist'
        
        #clear the current serverlist
        tab.clearServerList()
        
        #perform the master server query
        qm = QueryManager()
        qm.startMasterServerQueryThread(serverlistfilter, tab)


    def addServerListToTab(self, serverlist, tab, serverlistfilter):
        """
        Gets the status of each server in the passed serverlist and 
        add it to the serverlist of the passed tab.
        
        
        @param serverlist - the list of servers 
        @param tab - the tab 
        param serverlistfilter - filters that should be applied
        """
        if serverlist: 
            #needed for updating the progressbar
            fraction4oneserver = 1./float(len(serverlist)) 
            
            tab.statusbar.progressbar.set_text("fetching serverinfos...")
            #if serverlist > 50 create 10 worker threads to speed up server query
            if len(serverlist) > 50 :
                index_low = 0
                index_high = int(len(serverlist)/10)
                for i in range(1, 11):
                    if i == 10:
                        partition = serverlist[index_low:len(serverlist)]
                    else:
                        partition = serverlist[index_low:index_high]
                    thread.start_new_thread(self.populateServerView, \
                         (partition, fraction4oneserver, tab, serverlistfilter))
                    index_low = index_high
                    index_high = index_high*i 
            else:
                thread.start_new_thread(self.populateServerView, \
                        (serverlist, fraction4oneserver, tab, serverlistfilter))
        else:
            tab.statusbar.progressbar.set_text("failed getting serverlist from masterserver")
            tab.statusbar.progressbar.set_fraction(0.0)


    def appendProgressFraction(self, fraction2add, tab):
        """
        Appends the passed fractionvalue to the progressbar.
        
        @param fraction2add- the value that should be added to the current
                             fraction of the progressbar
        @param tab - the tab on which the progressbar to be updated is located
        """
        cur = tab.statusbar.progressbar.get_fraction()
        new = cur+fraction2add
        if 1.0>new+fraction2add: 
            tab.statusbar.progressbar.set_fraction(cur+fraction2add)
        else:
            tab.statusbar.progressbar.set_fraction(0.0)
            tab.statusbar.progressbar.set_text('')
        
    def populateServerView(self, serverlist, fraction4oneserver, tab, serverlistfilter):   
        """
        Populates the serverlisttreeview of a tab with the servers of a passed
        serverlist. Also updates the status of each server.
        
        @param serverlist - the serverlist that should be displayed
        @param fraction4oneserver- for updating the progressbar
        @param serverlistfiler - filters that should be applied
        @tab - the tab whichs serverlist should be updated
        """
        query = Q3ServerQuery()   
        lauf = 0
       
       
        for server in serverlist:
            lauf+=1
            # getStatus for a server is needed, because getStatus will not return
            # every needed information (e.g. if a server is passworded)
            server = query.getServerStatus(server)
            if not self.does_filter_match_server(server, serverlistfilter):    
                # update the UI
                gobject.idle_add(tab.addServer, server)
            gobject.idle_add(self.appendProgressFraction, fraction4oneserver, tab)
    

    
    def connectToServer(self, server):
        """
        Launches Urban Terror and connect to the passed server
        
        @param server - the server to connect to 
        """
        fm = FileManager()
        
        
        #build the connect parameters
        #format of the commandline command:
        #urbanterror + connect <adress> + password <pw>
        
        #get the executablename, the path and the additional commands
        #from the configuration
        config = fm.getConfiguration()
        executable = config['urt_executable']
        path = config['path_to_executable']
        additionalcommands = config['additional_commands']
                
        cmd = path + executable + ' + connect ' + server.getAdress()
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
        print 'launching UrT with cmd = ' + cmd
        os.popen(cmd) 
        
    def does_filter_match_server(self, server, filter):
        """
        Checks if the passed filter matches the passed server.
        If filter matches the server return True, which means the server
        is filtered and should not be displayed. 
        Otherwise return False
        
        @param server - the server to check
        @param filter - the filter to be applied
        """
        
        #basic filtering on UrT Servers.
        #also UrTSB uses the UrT Masterserver sometimes a Q3 server appears 
        #in the list
        vars = server.getServerVars()
        if 'gamename' in vars:
            if not vars['gamename'] == 'q3ut4':
                return True
        
        if not filter: # no filter passed
            return False
        
        # hide non responsove servers 
        if (server.getPing() == 999) \
                           and filter.checkbox_hide_non_responsive.get_active():
            return True
        # hide passworded servers
        if server.needsPassword() \
                               and filter.checkbox_hide_passworded.get_active():
            return True
        
        
        gametype = server.getGameType()
        if gametype == '8' and not filter.checkbox_show_gametype_bomb.get_active():
            return True
        elif gametype == '6' and not filter.checkbox_show_gametype_cah.get_active():
            return True
        elif gametype == '7' and not filter.checkbox_show_gametype_ctf.get_active(): 
            return True
        elif gametype == '0' and not filter.checkbox_show_gametype_ffa.get_active():
            return True
        elif gametype == '3' and not filter.checkbox_show_gametype_tdm.get_active():
            return True
        elif gametype == '4' and not filter.checkbox_show_gametype_survivor.get_active():
            return True
        elif gametype == '5' and not filter.checkbox_show_gametype_ftl.get_active():
            return True
        
        filter_min_player = filter.minplayerentry.get_value_as_int()
        filter_max_player = filter.maxplayerentry.get_value_as_int()
        
        
        if filter_min_player > server.getClientCount():
            return True
        
        if filter_max_player < server.getClientCount():
            return True
   
        #no filtermatch so far, return false which results in displaying the server
        return False       