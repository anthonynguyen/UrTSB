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

from globals import Globals
from servermanager import ServerManager
import time



class FileManager(object):
    """
    This class handles all file accesses of UrTSB.
    
    1. read/write of configuration
    2. access file for loading/storing favorites list
    3. access file for loading/storing recent servers
    
    """
    __shared_state = {} # borg pattern
    
    instance = None

    favorites = None
    recentservers = None
    configuration = None
    buddies = None
    
    #filenames
    conf_file = 'urtsb.cfg'
    fav_file = 'favorites.srv'
    rec_file = 'recent.srv'
    buddies_file = 'buddies.cfg'
    log_file = 'urtsb.log'
    
    

    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__shared_state # borg pattern
        
        if not self.instance:
            self.instance = True
            
            
            
            # extend filenames with path to the configurationfolder
            self.log_file = Globals.configfolder+FileManager.log_file
            self.fav_file = Globals.configfolder+FileManager.fav_file
            self.rec_file = Globals.configfolder+FileManager.rec_file
            self.conf_file = Globals.configfolder+FileManager.conf_file
            self.buddies_file = Globals.configfolder+FileManager.buddies_file
            
            #initialise ServerManager
            self.srvman = ServerManager()
    
    def get_buddies(self):
        """
        Get the list of buddies (names or part of names). If already loaded 
        from file the instance from memory is returned, otherwise it is fresh 
        loaded from the file.
        
        @return list of server names
        """
        if self.buddies:
            return self.buddies
        
        self.buddies = []
        
        fobj = None
        try:
            fobj = open(self.buddies_file, "r") 
        except IOError:
            #the file does not exist! just return the empty list created earlier
            return self.buddies
        
        for line in fobj: 
            line = line.strip('\n')
            self.buddies.append(line)
        fobj.close()
        return self.buddies
        
    def save_buddies(self):
        """
        Writes the list of buddies to the buddies file.
        """
        fobj = open(self.buddies_file, "w") 
        for name in self.buddies:
            
            #format: one name on every line
            fobj.write(name + '\n')
        fobj.close()
        
    
    def getFavorites(self):
        """
        Get the Favorites. If already loaded from file, return the instance from
        memory, otherwise load from file. 
        
        @return dict of server objects (key = address)
        """
        if self.favorites:
            return self.favorites
        
        self.favorites = {}
        fobj = None
        try:
            fobj = open(self.fav_file, "r") 
        except IOError:
            #the file does not exist! just return the empty dict created earlier
            return self.favorites
        
        for line in fobj: 
            line = line.strip() 
            serverinfo = line.split(',') # file is a csv
            #format: ip,port,password,servername
            server = self.srvman.getServer(serverinfo[0], int(serverinfo[1]))
            server.setPassword(serverinfo[2])
            server.setName(serverinfo[3])
            server.setIsFavorite(True)
            #use the address (ip:port) as key to avoid duplicate entries
            self.favorites[server.getaddress()] = server
        fobj.close()
        
        return self.favorites
    
    def addFavorite(self, server):
        """
        Adds a new favorite server to the list of favorites.
        Note: Immediately writes the current state of the list 
        into the favorites file. 
        
        @param server - the server object to add
        """
        favs = self.getFavorites() # this makes sure it is initialized 
        if server.getaddress() not in favs:
            self.favorites[server.getaddress()] = server
            #immdediately save to file in order to avoid a loss of data (crash etc.)
            self.saveFavorites()
            server.setIsFavorite(True)
    
    def removeFavorite(self, server):
        """
        Removes a existing favorite server from the favorites list.
        Note: Immediately updates the favorties file.
        
        @param server - the server object to be removed
        """
        favs = self.getFavorites() # this makes sure it is initialized  
        if server.getaddress() in favs:
            del self.favorites[server.getaddress()]
            self.saveFavorites()
            
    def remove_buddy(self, name):
        """
        Removes a name from the buddylist and immediately persists this change
        to the list into the buddylist file.
        
        @param name - the name to be removed
        """
        for i in range(len(self.buddies)):
            if name == self.buddies[i]:
                del self.buddies[i]
                break # already found the name to delete, so we can stop the loop
        self.save_buddies()
            
    def removeRecentServer(self, server):
        """
        Removes a existing recent server entry from the list.
        Note: Immediately updates the recent servers file.
        
        @param server - the server object to be removed
        """
        recents = self.getRecentServers() # this makes sure it is initialized  
        if server.getaddress() in recents.keys():
            del self.recentservers[server.getaddress()]
            self.saveRecentServers()
            
            
    def clearRecentServerList(self):
        """
        Clears the list of recent servers.
        """
        self.recentservers = {}
        self.saveRecentServers()
    
    def addRecent(self, server):
        """
        Adds a new server to the list of recent connected servers.
        Note: Immediately writes the current state of the list 
        into the recent servers file.
        Or if server exists, updates the existing entry 
        
        @param server - the server object to add
        """
        recent_servers = self.getRecentServers()
        if server.getaddress() not in self.recentservers:
            server.setConnections(1)
            self.recentservers[server.getaddress()] = server
        else:
            
            existing_entry = recent_servers[server.getaddress()] 
            conns = existing_entry.getConnections()
            conns += 1
            existing_entry.setConnections(conns)
            server = existing_entry
            
        server.setLastConnect(time.strftime("%Y.%m.%d - %H:%M"))
        #immdediately save to file in order to avoid a loss of data (crash etc.)
        self.saveRecentServers()
            
            
    def saveFavorites(self):
        """
        Performs the writing to the favorites file.
        """
        fobj = open(self.fav_file, "w") 
        for key in self.favorites:
            server = self.favorites[key]
            #format: ip,port,password,servername
            fobj.write(server.getHost() + ',' + str(server.getPort()) 
                       + ',' + server.getPassword() + ',' + server.getName() + '\n')
        fobj.close()
        
    def saveRecentServers(self):
        """
        Performs the writing to the recent servers file
        """
        fobj = open(self.rec_file, "w")
         
        for key in self.recentservers:
            server = self.recentservers[key]
            #format: ip,port,password, connectioncount,dateoflastconnection,name
            fobj.write(server.getHost() + ',' + str(server.getPort()) 
                     + ',' + server.getPassword() + ',' + str(server.getConnections()) + ','
                     + server.getLastConnect() + ',' + server.getName() + '\n')
        fobj.close()
    
    def getRecentServers(self):
        """
        Get the Recent Servers. If already loaded from file, return the instance from
        memory, otherwise load from file. 
        
        @return dict of server objects (key = address)
        """
        if self.recentservers:
            return self.recentservers
        
        self.recentservers = {}
        fobj = None
        try:
            fobj = open(self.rec_file, "r") 
        except IOError:
            #the file does not exist! just return the empty dict created earlier
            return self.recentservers
        
        for line in fobj: 
            line = line.strip() 
            serverinfo = line.split(',') # file is a csv
            #format: ip,port,password, connectioncount,dateoflastconnection,name
            server = self.srvman.getServer(serverinfo[0], int(serverinfo[1]))
            server.setPassword(serverinfo[2])
            server.setConnections(int(serverinfo[3]))
            server.setLastConnect(serverinfo[4])
            server.setName(serverinfo[5])
            self.recentservers[server.getaddress()] = server
        fobj.close()
        
        return self.recentservers        
    
    def getConfiguration(self):
        """
        Returns the configuration dict.
        If not already loaded from fail, else returned from memory.
        """
        if self.configuration:
            return self.configuration
        
        self.configuration = self.init_configuration()
        
        fobj = None
        try:
            fobj = open(self.conf_file, "r") 
        except IOError:
            #the file does not exist! just return the default dict created earlier
            return self.configuration
        
        for line in fobj: 
            #format of the configuration file is a key value pair on each 
            #line separated by a '='
            
            key, value = line.split('=', 1)
            self.configuration[key] = value.strip('\n') #strip linebreak
        return self.configuration
    
    def saveConfiguration(self):
        """
        Writes the current configuration dict into the configuration file.
        """
        fobj = open(self.conf_file, "w")
         
        for key in self.configuration:
            value = self.configuration[key]
            #format of each line:  key=value
            fobj.write(key+'='+str(value)+'\n')
        fobj.close()
        
    def init_configuration(self):
        """
        Performs initialisation of the configuration dict
        by setting all available options to default values
        """
        configuration = {}
        
        configuration['urt_executable'] = 'urbanterror'
        configuration['path_to_executable'] = ''
        configuration['additional_commands'] = ''
        configuration['save_passwords'] = True
        configuration['default_tab'] = 0

        return configuration