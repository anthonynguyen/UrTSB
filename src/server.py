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

class Server(object):
    """
    Represents a UrT game server. 
    """
    password = ''
    
    def __init__(self, host, port):
        """
        Constructor
        
        @param host - hostadress of the game server
        @param port - port number of the game server
        """
        self.host = host
        self.port = port
        self.setDefaults()
       
    def setDefaults(self):
        """
        Sets values to defaults. 
        """
        self.name = '-'
        self.ping = 999
        self.max_players = 0
        self.clientcount = 0
        self.map = '-'
        self.gametype = '-'
        self.playerlist = []
        self.vars = []
        self.lastconnect = ''
        self.connections = 0
        self.needspw = None
        
        
    def reset(self):
        self.setDefaults()
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getAdress(self):
        return self.host+':'+str(self.port)
    
    def getPing(self):
        return self.ping
    
    def setPing(self, ping):
        self.ping = ping
        
    def getClientCount(self):
        return self.clientcount
    
    def setClientCount(self, clientcount):
        self.clientcount = clientcount
        
    def getMaxPlayers(self):
        return self.max_players
    
    def setMaxPlayers(self, maxplayers):
        self.max_players = maxplayers
    
    def getPlayerString(self):
        return str(self.clientcount)+'/'+str(self.max_players)
    
    def getMap(self):
        return self.map
    
    def setMap(self, map):
        self.map = map
        
    def getGameType(self):
        return self.gametype
    
    def setGameType(self, gametype):
        self.gametype = gametype
        
    def getGameTypeName(self):
        """
        Returns a string representation of the gametype number.
        This is UrT specific!
        """
        
        if self.gametype == '8':
            return "Bomb"
        elif self.gametype == '6':
            return 'Capture & Hold'
        elif self.gametype == '7': 
            return 'Capture the Flag'
        elif self.gametype == '0':
            return 'Free For All'
        elif self.gametype == '3':
            return 'Team Deathmatch'
        elif self.gametype == '4':
            return 'Team Survivor'
        elif self.gametype == '5':
            return 'Follow the Leader'
        else:
            return 'Unknown: '+ self.gametype
        
    def getPlayerList(self):
        return self.playerlist
    
    def getServerVars(self):
        return self.vars
    
    def setServerVars(self, vars):
        self.vars = vars
        
    def getLastConnect(self):
        return self.lastconnect
    
    def setLastConnect(self, date_of_last_connect):
        self.lastconnect = date_of_last_connect
        
    def getConnections(self):
        return self.connections
    
    def setConnections(self, connections):
        self.connections = connections
        
    def needsPassword(self):
        return self.needspw
    
    def setNeedsPassword(self, needspw):
        self.needspw = needspw
        
    def getPassword(self):
        return self.password
    
    def setPassword(self, password):
        self.password = password
        
    