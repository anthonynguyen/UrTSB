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

from log import Log
from player import Player
from servermanager import ServerManager
import re
import socket
import time

try:
    from socket import inet_ntop as inet_ntop
except ImportError:
    ## on Windows socket.inet_ntop is not available (at least not
    ## in python2.6. http://www.dnspython.org provides a alternative
    from dns.inet import inet_ntop as inet_ntop

class Q3ServerQuery(object):
    """
    Implements the network communication with the UrT master server and
    the UrT Game server. Since UrT is based on ioQuake3 the open source 
    implementation of Quake3Arena this class should also work with other
    Q3 based games. (the Server class must be replaced, there is some UrT 
    specific code) 
    
    Supported features atm:
    - query a master server to retreive a list of gane server
    - send getinfo command to a game server and handle the response
    - send getstatus command to a game server and handle the response
       
    """
    
    # all packets begins with 0xFFFFFFFF indicating a q3 OOB command
    packet_prefix = '\xff' * 4
    
    
    def get_host_by_name(self, name):
        """
        Converts the passed hostname to a ipv4 ip adress.
        If the name already is a ipv4 ip it is returned unchanged
        
        @param name - the name for which an ip is requested
        """
        return socket.gethostbyname(name)
   
    def parseInfoResponse(self, response, server):
        """
        Parse the infoResponse message from an Q3/UrT game server.
                
        @param response - the infoResponse message 
        @param server - the server object where the retreived informations
                        should be stored in
        
        @return: the filled server object (the same that was passed as parameter) 
        """
        # the infoResponse contains of two lines 
        # first line is the header OOB-command bytes + infoResponse string
        # second line contains the info data as / seperated values
        # so cut of the first line to only have the real data for further 
        # processing
        headerlength = response.find('\n')
        infoline = response[headerlength+1:]
        # handling the data line is outsourced into the fillServerInfo method
        self.fillServerInfo(server, infoline)
        return server
    
    def parseStatusResponse(self, response, server):
        """
        Parse the statusResponse message of an Q3/UrT game server.
        
        @param response- the statusResponse message
        @param server - the server object where the retreived informations
                        should be stored in  
        """
        
        # format of the statusResponse:
        # first line is the "header" OOB-command bytes + statusResponse string
        # second line contains the servervars as / seperated key values
        # every further line represents a player with name, ping and kills
                
        # cut of headerline
        index1 = response.find('\n')
        infoline = response[index1+1:]
        #find second \n to get the server vars line
        index2  = infoline.find('\n')
        infoline = infoline[:index2]
        # further lines (aka playerlines)
        playerlines = response[index1+index2+1:]
        
        # handling of the server vars and playerlines   
        self.fillServerStatus(server, infoline)
        self.fillPlayerInfo(server, playerlines)
                
        #map some vars to variables of the server class
        vars = server.getServerVars()
        # the name of the server
        if 'sv_hostname' in vars:
            hostname = self.stripQ3ColorcodesFromString(vars['sv_hostname'])
            server.setName(hostname)
        # the gametype. its a number. Mapping to string representation
        # like 'TDM' is done in the Server class
        if 'g_gametype' in vars:
            server.setGameType(server.getServerVars()['g_gametype'])
        # current map
        if 'mapname' in vars:
            server.setMap(server.getServerVars()['mapname'])
        
        # does the server needs a password? 0 = no, 1 = yes
        if 'g_needpass' in vars:
            needpass = vars['g_needpass']
            if '0' == needpass:
                server.setNeedsPassword(False)
            elif '1' == needpass:
                server.setNeedsPassword(True)
                
        # there are some alternative keys for max players
        if 'g_maxGameClients' in vars:
            server.setMaxPlayers(vars['g_maxGameClients'])
        if 'sv_maxclients' in vars:
            server.setMaxPlayers(vars['sv_maxclients'])
        if 'sv_maxClients' in vars:
            server.setMaxPlayers(vars['sv_maxClients'])
        
        # there is no explicit value for count of currently connected clients 
        # like the infoResponse provides so use the length of the player list
        playerlist = server.getPlayerList()
        server.setClientCount(len(playerlist))
        
        return server
   
    def fillPlayerInfo(self, server, playerlines):
        """
        Fill the information of currently connected players (name, kills, 
        ping) of a server into the passed Server instance  by parsing the 
        playerlines extracted from the last part of a statusResponse message.
        
        @param server- the server instance the data should be stored into
        @param playerlines - the last part of the statusResponse message
                             containing the playerinformations
        """
        # each line contains information about one player so split by linebreak
        toks = playerlines.split('\n')
        # regular expression for extracting the information of a line
        # format of playerinformation is "kills  ping playername" 
        regexp = re.compile(r'^(-?\d+) (\d+) "(.*)"')
        #this can also be an update, so clear the playerlist of the server first
        playerlist = server.getPlayerList()
        del playerlist[:] 
        # finally iterate over the lines and apply the regexp on it
        for tok in toks:
            if tok:
                match = regexp.match(tok)
                if match:
                    kills, ping, name = match.groups()
                    name = self.stripQ3ColorcodesFromString(name)
                    player = Player(name, kills, ping)
                    server.getPlayerList().append(player)
                   
   
    def fillServerStatus(self, server, statusline):
        """
        Extract the server vars out of the passed server vars line of a
        statusResponse message and apply it on the passed server instance
        
        @param server - the server instance the data should be stored into
        @param statusline - second line of a statusResponse message containing
                            the server vars
        """
        
        # format is key/value/key/value/...etc. 
        split = statusline[1:].split('\\')
        vars = dict(zip(split[::2], split[1::2])) 
        server.setServerVars(vars) 
       
    def stripQ3ColorcodesFromString(self, value):
        """
        Utility method Removing the Q3 color codes from the passed string 
        and return it as a new string. 
        """
        
        #remove q3 color codes (e.g. ^2 or ^3) from hostname using a regexp
        retval = re.sub('\^[0-9]', '', value)
        return retval  
        
    def fillServerInfo(self, server, infoline):
        """
        Extract the server infos hostname, mapname, clientcount, maxclients
        and gametype from the second line of a infoResponse message.
        
        @param server - the server instance the data should be stored into
        @param infoline - second line of an infoResponse message  
        """
        
        # format is key/value/key/value/...etc. 
        split = infoline[1:].split('\\')
        vars = dict(zip(split[::2], split[1::2]))     
        
        #use the keys to get the values and set them at the passed server instance
        hostname = vars['hostname']
        hostname = self.stripQ3ColorcodesFromString(hostname)
        server.setName(hostname)
                
        server.setClientCount(int(vars['clients']))
        server.setMap(vars['mapname'])
        server.setMaxPlayers(vars['sv_maxclients'])
        server.setGameType(vars['gametype'])
    
    def parseResponse(self, response, server):
        """
        parse the response a game server returned after sending an 'getinfo' or
        'getstatus' command.
        
        @param response - the response of the game server
        @param server - the server which sends the response 
        
        @return - the server object with updated data based on the response
        """
        
        # check if its a info or status response and delegate to the 
        # appropriate method 
        if response.find('infoResponse') != -1:
            return self.parseInfoResponse(response, server)
        if response.find('statusResponse') != -1:
            return self.parseStatusResponse(response, server)
        # if two above returns not happened it must be a malformed response.
        # reset the server object. this will look like a timeout at the gui
        server.reset()
        return server
      
    def send_rcon_command(self, command, server):
        """
        Sends a rcon command to a gameserver
        
        @param command - the command to send to the game server
        @param server - the server
        """      
        try:
            # open an socket to the game server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((server.getHost(), server.getPort()))
            # set timeout to 1s 
            s.settimeout(2)
            # all packets send to an q3 server must beging with the OOB command bytes
            cmd = self.packet_prefix+command 
            s.send(cmd)
        except:
            Log.log.error('Something went wrong opening socket to ' + server.getaddress())
            server.reset()
            return server
        response = None
        
        
        for retries in range(3):
        
            time_start = time.time() # start time measurement (pinging)       
            try:
                response = s.recv(2048) # a bit more buffer than needed
                break 
            except:
                if retries == 2:
                    # handle failure case - usually this is a timeout
                    Log.log.info('[Q3ServerQuery] '+server.getaddress() \
                                 +' is not responding - timeout')
                    return 'no response ...'
        time_end = time.time() # end time measurement (pinging)
        ping = int((time_end-time_start)*1000) # calculate ping
        s.close() #close the socket
        if response: # yeah got a response :-)
            server.setPing(ping) # update the ping of the server
            
            if response.find('print') != -1:
                response = response[9:]
                return response
            else:
                Log.log.error('Malformed package received: ' + response)           
                return 'Malformed response received from server'
        else:
            return 'no timeout, but also no response?!...'
            
        
   
    def sendCommand(self, command, server):
        """
        Sends an UDP Packet containing a Q3 server command to a game server
        specified by a passed server object.
        The server response is delegated to the parseResponse method
        
        @param command - the command to send to the game server
        @param server - the server  
        """
        
        try:
            # open an socket to the game server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((server.getHost(), server.getPort()))
            # set timeout to 1s 
            s.settimeout(1)
            # all packets send to an q3 server must beging with the OOB command bytes
            cmd = self.packet_prefix+command 
            s.send(cmd)
        except:
            Log.log.error('Something went wrong opening socket to ' + server.getaddress())
            server.reset()
            return server
        response = None
        
        
        for retries in range(3):
        
            time_start = time.time() # start time measurement (pinging)       
            try:
                response = s.recv(2048) # a bit more buffer than needed
                break 
            except:
                if retries == 2:
                    # handle failure case - usually this is a timeout
                    Log.log.info('[Q3ServerQuery] '+server.getaddress() \
                                 +' is not responding - timeout')
                    server.reset() # reset server object
        time_end = time.time() # end time measurement (pinging)
        ping = int((time_end-time_start)*1000) # calculate ping
        
        s.close() # close the socket
        
        if response: # yeah got a response :-)
            server.setPing(ping) # update the ping of the server
            return self.parseResponse(response, server) # parse the response and
                                                        # update server data/info
        else: # reset if no response
            server.reset()
            return server
        
   
    def getServerStatus(self, server):
        """
        Sends a 'getstatus' command to a gamesever.
        """
        return self.sendCommand('getstatus\n', server)
        
      
    def getServerInfo(self, server):
        """
        Sends a 'getinfo' command to a gamesever.
        """
        return self.sendCommand('getinfo\n', server)
        
    def getServerList(self, host, port, empty, full):
        """
        Query a master server to retreive a list of registered game servers.
        
        @param host - host of the master server
        @param port - port of the master server
        @param empty - boolean parameter - false = empty servers will not be returned
                       by the master server - true = get also empty servers
        @param full - boolean parameter - false = full sercers will no be returned 
                      by the master server - true = get also full servers
                      
        @return list of server objects
        """
        Log.log.info('[Q3ServerQuery] - start master server query')
        
        #server manager
        srvman = ServerManager()
        self.serverlist = []
        
        #open socket to the master server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host, port))
        s.settimeout(2) 
        # build command string based on the provided parameters empty and full
        # format 'OOBgetservers protocol [empty] [full] [demo]'
        cmd = self.packet_prefix+'getservers  68 '
        if empty and full:
            cmd+='empty full'
        else:
            if empty:
                cmd+='empty'
            if full:
                cmd+='full'
        cmd+=' demo'
        # send !
        s.send(cmd)
        
        # the master server can send multiple reponse packets based on the count
        # of servers - collect all of these response packtes in a list
        self.response = []
        while True:
            try:
                # a full responsepacket has 1394 bytes so use 1395 as 
                # receive buffer
                response = s.recv(1395)
                   
            except:
                break
            
            if not response :
                break
            else:
                self.response.append(response)
       
        Log.log.debug('[Q3ServerQuery] received ' \
                    + str(len(self.response)) + ' response packets ' \
                    + 'from master server')
       
        # parse the response 
        # packet format: all packets starts with the OOB bytes and a
        # 'getserversResponse' string. after this start the server list starts
        # which are each 7 bytes. Start with the char / (first byte), the next
        # four bytes are the ip and the last two bytes is the port number
        # transmission of servers ends with '/EOF' at the end of the last packet
        for packet in self.response:
            index = 22 # OOB bytes + getserversResponse = 22 bytes
            # iterate over the 7 byte fields in the packet 
            while True:
                # /EOF or malformed packet
                if index+7>=len(packet):
                    break
                # ip              
                ip = inet_ntop(socket.AF_INET, packet[index+1:index+5])
                #port
                port = 256*ord(packet[index+5]) + ord(packet[index+6])
                index+=7
                # create server object and add it to the serverlist that will
                # be returned
                server = srvman.getServer(ip, int(port))
                self.serverlist.append(server)
         
        s.close()
        
        Log.log.info('[Q3ServerQuery] - finished master server query. ' \
                     + 'returning list with ' + str(len(self.serverlist)) \
                     + ' servers')
        return self.serverlist
        
   
        