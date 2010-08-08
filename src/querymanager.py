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
from Queue import Queue, Empty
from filemanager import FileManager
from log import Log
from q3serverquery import Q3ServerQuery
from threading import Thread
import gobject
import threading



class QueryManager(object):
    """
    Implements handling multiple threads used to speed up serverqueries
    
    
    """

    def __init__(self):
        """
        Constructor -
        It starts with some basic initialisations and spawns a coordinator
        thread which creates more threads to perform the master server query 
        and also the status updates for the servers.
        """
        self.serverqueue = Queue()
        self.messageque = Queue()
        self.pulsemessageque = Queue() 
        
        self.threadcount = 0
        self.servercount = 0
        self.processedserver = 0
        self.filterdcount = 0
        
        self.gui_lock = None
        
        coord = Thread(target=self.coordinator)
        coord.daemon = True
        coord.start()
        
    def startMasterServerQueryThread(self, filter, tab):
        """
        Starts the masterserver query.
        
        @param filter - filter to apply
        @param tab - tab requesting the serverlist
        
        """
        
        self.tab = tab
        self.filter = filter
        tab.clearServerList()
        
        
        #this message will cause the coordinator to start querying the master
        #server
        self.messageque.put('start_master_server_query')
        
    def startRecentServersLoadingThread(self, tab):
        """
        Starts loading the recent servers list
        
        @param tab - tab rquesting the recent servers
        """
        fm = FileManager()
        self.tab = tab
        self.filter = None
        
        serverdict = fm.getRecentServers()
        for key in serverdict:
            self.serverqueue.put(serverdict[key])
        
        self.servercount = len(serverdict)
        
        #notify the coordinator thread, that the serverlist is loaded
        self.messageque.put('serverlist_loaded')
        
        
    def startFavoritesLoadingThread(self, tab):
        """
        Starts loading the favorites
        
        @param tab - the tab requesting the favoriteslist
        """
        fm = FileManager()
        self.tab = tab
        self.filter = None
        
        serverlist = fm.getFavorites().values()
        for server in serverlist:
            self.serverqueue.put(server)
            
        self.servercount = len(serverlist)
        
        #notify the coordinator thread, that the serverlist is loaded
        self.messageque.put('serverlist_loaded')
        
    def coordinator(self):
        """
        Method that runs as coordinator thread.
        Spawning additional threads based on string messages in the messagueue
        
        Messages accepted: 
        start_master_server_query - is the start signal. will cause the coordinator
                                    to spawn two new threads. The first is to pulse
                                    the progressbar on self.tab every 0.1 seconds.
                                    The second thread performs the master server
                                    query, when this thread finishes puts the
                                    message serverlist_loaded into the 
                                    messagequeue indicating that the query
                                    was succesfull and the serverqueue is 
                                    filled with servers
        serverlist_loaded - spawns 10 worker threads that will perform the 
                            get_status request of the servers in the 
                            serverqueue
        finished - if the status of all servers has been retreived the last 
                   thread puts this message in the messagueue. calls the
                   serverlist_loading_finished method on self.tab and terminates
                   the coordinator thread
        
        
        """
        # main thread loop
        Log.log.debug('Thread:Coordinator started...')
        while True:
            try:
                
                message = self.messageque.get()    
                if message == 'start_master_server_query':
                    # spawn the pulse progressbar thread
                    pt = Thread(target=self.pulse_progressbar_thread)
                    pt.setDaemon(True)
                    pt.start()
                    #spawns the master server query thread
                    pt = Thread(target=self.master_server_query_thread)
                    pt.setDaemon(True)
                    pt.start()
                elif message == 'serverlist_loaded':
                    Log.log.debug('Thread:Coordinator - received serverlist' \
                                  +'_loaded signal. Queuesize is ' \
                                  + str(self.serverqueue.qsize()))
                    
                    #stop the pulsing of the progressbar
                    self.pulsemessageque.put('stop_pulse')    
                    #start 10 worker threads retreiving the status of 
                    #the servers in the serverqueue
                    for i in range(10):
                        t = Thread(target=self.get_server_status_thread)
                        t.setDaemon(True)
                        t.start()
                elif message == 'finished':
                    #finish tasks :)
                    Log.log.debug('Thread:Coordinator - received the ' \
                                  + 'finished signal')
                    self.gui_lock = threading.RLock()
                    with self.gui_lock:
                        gobject.idle_add(self.tab.serverlist_loading_finished)
                    break
            except Empty:
                True
    
    
    def master_server_query_thread(self):
        """
        This method is running as a thread to retreive a list of servers
        from the master server.
        """
        query = Q3ServerQuery()
        
        
        empty = self.filter.checkbox_showempty.get_active()    
        full = self.filter.checkbox_showfull.get_active()
        
        #query the urban terror master server
        serverlist = query.getServerList('master.urbanterror.info'
                                         ,27950
                                         ,empty
                                         ,full)
        #put all servers in the serverqueue
        for server in serverlist:
            self.serverqueue.put(server)
        self.servercount = len(serverlist)
        
        #notify the coordinator thread, that the serverlist is loaded
        self.messageque.put('serverlist_loaded')
      
      
    def get_server_status_thread(self):
        """
        This method will run as worker thread to retreive the status of
        the servers in the serverqueue
        """
        
        #increment thread count.
        #the counter will be decreased on exit and compared to 0
        #so the last thread can notify the coordinator that all threads finished
        #their work        
        self.gui_lock = threading.RLock()
        with self.gui_lock:
            self.threadcount+=1
            
        # main thread loop
        while True:
            try:
                server = self.serverqueue.get(False)    
                
                #perform the statusrequest
                query = Q3ServerQuery()   
                server = query.getServerStatus(server)
                
                #add the server to the gui 
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    self.processedserver+=1
                    gobject.idle_add(self.set_progressbar_fraction)
                    if not self.does_filter_match_server(server, self.filter):
                        gobject.idle_add(self.tab.addServer, server)
                    else:
                        self.filterdcount+=1  # server is not added but filterd
                        
            except Empty:
                #no more threads in the queue break thread execution
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    self.threadcount -= 1
                    if self.threadcount == 0: #last thread reached
                        self.messageque.put('finished')
                break
    
    def pulse_progressbar_thread(self):
        """
        This method runs as a background thread that pulse the progressbar
        of self.tab every 0.1 seconds
        """
        while True:
            try:
                message = self.pulsemessageque.get(True, 0.1)    
                if message == 'stop_pulse':
                    break
            except Empty:
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    gobject.idle_add(self.pulse_progressbar)
                    
                    
    def set_progressbar_fraction(self):
        """
        Sets the progressbar fraction. Uses the total servercount and the
        processed servercount values to calculate the fraction
        """
        fraction = float(self.processedserver) / float(self.servercount)
        
        
        bartext = None
        if 1.0 == fraction:
            bartext = 'finished getting server status - displaying ' \
                     + str((self.processedserver-self.filterdcount)) + \
                     ' servers (' + str(self.filterdcount) + ' filtered)'
            self.tab.statusbar.progressbar.set_fraction(0.0)
            
        else:
            bartext = 'fetching server status (' + str(self.processedserver) + \
                      ' / ' + str(self.servercount) + ') - ' + \
                      str(self.filterdcount) + ' servers filtered'
            self.tab.statusbar.progressbar.set_fraction(fraction)     
        self.tab.statusbar.progressbar.set_text(bartext)
                    
    def pulse_progressbar(self):
        """
        Pulse the progressbar, called by the thread using  gobject.idle_add
        """
        self.tab.statusbar.progressbar.set_text('fetching serverlist from master server')
        self.tab.statusbar.progressbar.pulse() 
        
    
    
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
        elif filter.get_filter_name() == 'serverlistfilter':
            return self.apply_serverlist_filter(server, filter)
        elif filter.get_filter_name() == 'buddiesfilter':
            return self.apply_buddies_filter(server, filter)
        else:
            return True #unknown filter don't filter the server
        
    def apply_buddies_filter(self, server, filter):
        """
        Checks if the players of the found server matches one of the names in 
        the searchlist
        
        @param server - the server to apply the filter
        @param filter - the buddy search filter to apply
        
        @return false - if this server should not be displayed (means no player
                        on this server matches the buddylist), otherwise 
                        returnvalue is true 
        """
        
        namefilters = filter.searchname_list
        playerlist = server.getPlayerList()
        
        #if there are no players on the server return true to hide the server
        if len(playerlist) == 0:
            return True
        
        for player in playerlist:
            for name in namefilters:
                #we want also partial matches e.g. when searching for a clantag
                count = player.getName().find(name)
                if not count == -1:
                    #a match! return False, so that the server will be displayed
                    #on the serverlist
                    return False
        #if the iteration returns no match, return True so that the server
        #will be hidden
        return True
        
       
        
    def apply_serverlist_filter(self, server, filter):
        """
        This methods checks if the filters specified by the passed 
        serverlistfilter object matches the passed server.
        
        @param server - server object to be checked against the filter
        @param filter - filter to be applied
        
        @param true if server should be hided, otherwise false
        """
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
    
        