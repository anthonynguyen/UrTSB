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
from server import Server

class ServerManager(object):
    """
    Manages creation and application internal memory storage of 
    Server class instances.
    """

    __shared_state = {} # borg pattern
    
    # dict of all servers (as key the address (ip:port) will be used)
    servers = {}

    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__shared_state # borg pattern
        
        
    def getServer(self, host, port):
        """
        Get a Server specified by host and port. If there is already
        a Server instance in the dict return this instance, otherwise create
        a new instance and put it in the dict and then return this instance.
        
        @param host - the hostaddress/ip of the server (str)
        @param port - the port of the server (int)
        
        @return instance of Server class
        """
        #concatenate host and port to addressstring that is used as the dict key
        address = host+':'+str(port)        
        if address in self.servers:
            return self.servers[address]
        server = Server(host, port)
        self.servers[address] = server
        return server
        
        