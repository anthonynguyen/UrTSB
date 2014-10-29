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
    connections = 0
    
    
    def __init__(self, host, port):
        """
        Constructor
        
        @param host - hostaddress of the game server
        @param port - port number of the game server
        """
        self.host = host
        self.port = port
        self.setDefaults()
        self.favorite = False
        self.lastconnect = ''
        self.connections = 0
        self.name = '-'
        self.favorite = False
        self.rememberpass = False
        self.location = ''
        self.locationame = ''
        self.rconpass = ''
        self.priv_slots = 0
       
    def setDefaults(self):
        """
        Sets values to defaults. 
        """
        #self.name = '-'
        self.ping = 999
        self.max_players = 0
        self.clientcount = 0
        self.map = '-'
        self.gametype = '-'
        self.playerlist = []
        self.vars = []
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
    
    def getaddress(self):
        return self.host+':'+str(self.port)
    
    def getPing(self):
        return self.ping
    
    def setPing(self, ping):
        self.ping = ping
        
    def getClientCount(self):
        return self.clientcount
    
    def setClientCount(self, clientcount):
        self.clientcount = int(clientcount)
        
    def getMaxPlayers(self):
        return self.max_players
    
    def setMaxPlayers(self, maxplayers):
        self.max_players = int(maxplayers)
        
    def set_private_slots(self, priv_slots):
        try:
            self.priv_slots = int(priv_slots)
        except:
            #fallback
            #there is one server which has the value 'ate123' as 
            #sv_privateclients value...
            self.priv_slots = 0
        
    def get_private_slots(self):
        return self.priv_slots
    
    def getPlayerString(self):
        players = str(self.clientcount)+'/'
        if not self.priv_slots == 0:
            players += str(self.max_players - self.priv_slots)
            players += ' (+' + str(self.priv_slots) +')'
        else:
            players += str(self.max_players) 
        return str(self.clientcount)+'/'+str(self.max_players)+ ' (' +str(self.priv_slots) + ')'
    
    def getVersionString(self):
        try:
            return self.vars["g_modversion"]
        except:
            return "Unknown"

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

        _GAMETYPES = [
            "Free For All",
            "Last Man Standing",
            "Unknown: 2",
            "Team Deathmatch",
            "Team Survivor",
            "Follow the Leader",
            "Capture and Hold",
            "Capture the Flag",
            "Bomb Mode",
            "Jump",
            "Freeze Tag"
        ]
        
        try:
            return _GAMETYPES[int(self.gametype)]
        except:
            return "Unknown: " + self.gametype
        
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
        
    def isFavorite(self):
        return self.favorite
    
    def setIsFavorite(self, isfavorite):
        self.favorite = isfavorite
        
    def getRememberPassword(self):
        return self.rememberpass
    
    def setRememberPassword(self, rememberpassword):
        self.rememberpass = rememberpassword
        
    def set_location(self, location):
        self.location = location
    
    def get_location(self):
        return self.location
    
    def set_location_name(self, locationname):
        self.locationame = locationname
    
    def get_location_name(self):
        return self.locationame
    
    def to_string(self):
        return self.getaddress() + ' - ' + self.name