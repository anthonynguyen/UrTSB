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
from globals import Globals
from log import Log
from pygeoip import GeoIP
from q3serverquery import Q3ServerQuery
from threading import Thread
import gobject
import pygeoip
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
        self.geo_lock = None
        
        coord = Thread(target=self.coordinator)
        coord.daemon = True
        coord.start()
        
        dbname = Globals.geoip_dir+ '/GeoIP.dat'
        self.pygeoip = GeoIP(dbname, pygeoip.const.MMAP_CACHE)
        
        self.abort = False
        
    def start_serverlist_refresh(self, liststore, tab):
        """
        Refreshes the Serverlist of a tab
        
        @param liststore - the liststore which contains the servers to be 
                           refreshed
        @param tab - the tab requesting the refresh
        """    
        self.tab = tab
        self.filter = None
        
        iter = liststore.iter_children(None)
        while iter:
            server = liststore.get_value(iter, 8)
            self.serverqueue.put(server)
            iter = liststore.iter_next(iter)
        
        self.servercount = self.serverqueue.qsize()
        
        gobject.idle_add(tab.clearServerList)
        self.messageque.put('serverlist_loaded')
        
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
     
    def lookup_server(self, server, tab):
        """
        Starts the lookup of a certain server. 
        
        @param server - the server to be looked up
        @param tab - the requesting tab
        """
        self.tab = tab
        self.filter = None
        
        self.serverqueue.put(server)
        self.servercount = 1
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
                    Log.log.info('Thread:Coordinator - start_master_server_' \
                                 +'query signal received')
                    # spawn the pulse progressbar thread
                    pt = Thread(target=self.pulse_progressbar_thread)
                    pt.setDaemon(True)
                    pt.start()
                    #spawns the master server query thread
                    pt = Thread(target=self.master_server_query_thread)
                    pt.setDaemon(True)
                    pt.start()
                elif message == 'serverlist_loaded':
                    Log.log.info('Thread:Coordinator - received serverlist' \
                                  +'_loaded signal. Queuesize is ' \
                                  + str(self.serverqueue.qsize()))
                    
                    #stop the pulsing of the progressbar
                    self.pulsemessageque.put('stop_pulse')    
                    #start 10 worker threads retreiving the status of 
                    #the servers in the serverqueue
                    for i in range(10):
                        name = 'Worker_' + str(i+1)
                        t = Thread(target=self.get_server_status_thread, name=name)
                        t.setDaemon(True)
                        t.start()
                elif message == 'finished':
                    #finish tasks :)
                    Log.log.info('Thread:Coordinator - received the ' \
                                  + 'finished signal')
                    self.gui_lock = threading.RLock()
                    with self.gui_lock:
                        gobject.idle_add(self.tab.serverlist_loading_finished)
                    break
                elif message == 'all_aborted':
                    #all_aborted tasks :)
                    Log.log.info('Thread:Coordinator - received the ' \
                                  + 'all_aborted signal')
                    self.gui_lock = threading.RLock()
                    with self.gui_lock:
                        gobject.idle_add(self.set_progressbar_aborted)
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
        
        
        empty = self.filter.show_empty   
        full = self.filter.show_full
        
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
            Log.log.debug('Thread:' + threading.current_thread().name + \
                         ' started') 
              
         
        # main thread loop
        while True:
            try:
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    if self.abort:
                        self.threadcount -= 1
                        Log.log.info('Thread:' + threading.current_thread().name + \
                         ' exiting due to abort signal')
                        if self.threadcount == 0: #last thread reached
                            Log.log.info('Thread:' + threading.current_thread().name + \
                            '   notifying the coordinator thread that all threads ' \
                            + 'was aborted')
                            self.messageque.put('all_aborted')
                        break
                
                server = self.serverqueue.get(False)    
                
                
                #perform the statusrequest
                query = Q3ServerQuery()   
                server = query.getServerStatus(server)
                
                #add the server to the gui 
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    
                    self.set_location(server)
                    
                    self.processedserver+=1
                    gobject.idle_add(self.set_progressbar_fraction)
                    if None == self.filter or \
                                   self.filter.does_filter_match_server(server):
                        gobject.idle_add(self.tab.addServer, server)
                    else:
                        self.filterdcount+=1  # server is not added but filterd
                        
            except Empty:
                #no more threads in the queue break thread execution
                self.gui_lock = threading.RLock()
                with self.gui_lock:
                    self.threadcount -= 1
                    Log.log.debug('Thread:' + threading.current_thread().name + \
                         ' finishes working and exiting')
                    if self.threadcount == 0: #last thread reached
                        Log.log.info('Thread:' + threading.current_thread().name + \
                         ' notifying the coordinator thread that the queue ' \
                         + 'processing is finished')
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
        if not self.abort:
            fraction = float(self.processedserver) / float(self.servercount)
            
            
            bartext = None
            if 1.0 == fraction:
                bartext = 'finished getting server status - displaying ' \
                         + str((self.servercount-self.filterdcount)) + \
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
       
    def set_progressbar_aborted(self):
        """
        Sets the text of the progressbar to the aborted message and resets fraction
        """    
        self.tab.statusbar.progressbar.set_text('task aborted')
        self.tab.statusbar.progressbar.set_fraction(0.0)
    
    def abort_current_task(self):
        """
        Stops the processing of the queue by setting a abort flag.
        """    
        self.gui_lock = threading.RLock()
        with self.gui_lock:
            self.abort = True
        
    def set_location(self, server):
        """
        Determine location of a server based on the ip adress of the server 
        and set it at the server object
        
        Extra threading lock used because there was some strange effects 
        without it.
        
        @param - the server object
        """
        self.geo_lock = threading.RLock()
        with self.geo_lock:
            #location = country(server.getHost())
            location = self.pygeoip.country_code_by_addr(server.getHost())
            locname = self.pygeoip.country_name_by_addr(server.getHost())
            server.set_location(location)
            server.set_location_name(locname)
