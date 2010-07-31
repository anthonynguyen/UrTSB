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

from q3serverquery import Q3ServerQuery
import gobject
import thread
from filemanager import FileManager

class GuiController(object):
    """
    Backend for the UI to perform non UI logic.
    """
    
    __shared_state = {} # borg pattern
    
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
      
    def executeMasterServerQuery(self, serverlistfilter, tab):
        """
        Starts executing the search for game servers.
        
        @param serverlistfilter - query and filteroptions 
        @param tab - the tab on the ui that requests the serverlist
        """        
        print 'search...'
        
        tab.clearServerList()
        thread.start_new_thread(self.loadMasterServerList
                                ,(serverlistfilter.checkbox_showempty.get_active()
                                ,serverlistfilter.checkbox_showfull.get_active()
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
        This method is executed in a background thread which is triggered by 
        the executeFavoritesLoading method.
        
        @param tab - the tab requesting the favorite servers list
        """
        fm = FileManager()
        tab.clearServerList()
        serverlist = fm.getFavorites().values()
        self.addServerListToTab(serverlist, tab)
        
    def loadRecentServer(self, tab):
        """
        Loads the list of recent servers from a file using the FileManager
        and update the serverlist on the requesting tab.
        This methid is executed in a background thread which is triggered by
        the executeRecentServersLoading method
        
        @param tab - the tab requesting the recent server list
        """
        fm = FileManager()
        tab.clearServerList()
        serverlist = fm.getRecentServers().values()
        self.addServerListToTab(serverlist, tab)

    def loadMasterServerList(self, empty, full, tab):
        """
        Loads the Serverlist from the masterserver.
        This method is executed in a background thread which is triggered by 
        the executeMasterServerQuery method
        
        @param empty - empty parameter for the query
        @param full - full parameter for the query
        @tab - the tab requesting the serverlist
        """
        print 'load_serverlist'
        query = Q3ServerQuery()
        
        self.window.progressbar.pulse()
        self.window.progressbar.set_text('asking Masterserver for list of server IPs')
        
        #query the urban terror master server
        serverlist = query.getServerList('master.urbanterror.info'
                                         ,27950
                                         ,empty
                                         ,full)
        # alternate master server        
#        serverlist = query.getServerList('master.uaaportal.com'
#                                         ,27950
#                                         ,empty
#                                         ,full)
        
        # start updating the ui with the serverlist
        self.addServerListToTab(serverlist, tab)


    def addServerListToTab(self, serverlist, tab):
        """
        Gets the status of each server in the passed serverlist and 
        add it to the serverlist of the passed tab.
        
        
        @param serverlist - the list of servers 
        @param tab - the tab 
        """
        if serverlist: 
            #needed for updating the progressbar
            fraction4oneserver = 1./float(len(serverlist)) 
            
            self.window.progressbar.set_text("fetching serverinfos...")
            #if serverlist > 50 create 10 worker threads to speed up server query
            if len(serverlist) > 50 :
                index_low = 0
                index_high = int(len(serverlist)/10)
                for i in range(1, 11):
                    if i == 10:
                        partition = serverlist[index_low:len(serverlist)]
                    else:
                        partition = serverlist[index_low:index_high]
                    thread.start_new_thread(self.populateServerView, (partition, fraction4oneserver, tab))
                    index_low = index_high
                    index_high = index_high*i 
            else:
                thread.start_new_thread(self.populateServerView, (serverlist, fraction4oneserver, tab))
        else:
            self.window.progressbar.set_text("failed getting serverlist from masterserver")
            self.window.progressbar.set_fraction(0.0)

    def appendProgressFraction(self, fraction2add):
        """
        Appends the passed fractionvalue to the progressbar.
        
        @param fraction2add- the value that should be added to the current
                             fraction of the progressbar
        """
        cur = self.window.progressbar.get_fraction()
        new = cur+fraction2add
        if 1.0>new+fraction2add: 
            self.window.progressbar.set_fraction(cur+fraction2add)
        else:
            self.window.progressbar.set_fraction(0.0)
            self.window.progressbar.set_text('')
        
    def populateServerView(self, serverlist, fraction4oneserver, tab):   
        """
        Populates the serverlisttreeview of a tab with the servers of a passed
        serverlist. Also updates the status of each server.
        
        @param serverlist - the serverlist that should be displayed
        @param fraction4oneserver- for updating the progressbar
        @tab - the tab whichs serverlist should be updated
        """
        query = Q3ServerQuery()   
        lauf = 0
       
       
        for server in serverlist:
            lauf+=1
            # getStatus for a server is needed, because getStatus will not return
            # every needed information (e.g. if a server is passworded)
            server = query.getServerStatus(server)
            
            # update the UI
            gobject.idle_add(self.appendProgressFraction, fraction4oneserver)
            gobject.idle_add(tab.addServer, server)
    