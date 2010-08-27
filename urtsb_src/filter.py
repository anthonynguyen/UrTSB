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
from urtsb_src.filemanager import FileManager, filterkey, cfgvalues
from urtsb_src.log import Log

class FilterType(object):
    """
    Defines the possible filtertypes
    """    
    BASIC_FILTER = 0
    ADVANCED_FILTER = 1
    BUDDY_FILTER = 2
    EMPTY= 3


class Filter(object):
    """
    Handles filtering of servers. Stores the filter settings and performs
    the comparison of server values and filter options.
    """

    DISABLED = 0
    INCLUDE = 1
    EXCLUDE = 2

    def __init__(self, type, tab=None):
        """
        Constructor
        
        @param the type of the filter @see FilterType
        """
        self.type = type
        
        self.tab = tab
        #filter values initialization
        
        #query params
        self.show_empty = False
        if FilterType.BUDDY_FILTER == type:
            self.show_full = True
        else:
            self.show_full = False
        
        #filters
        self.hide_passworded = True
        self.hide_non_responsive = True
        
        self.min_players = 0
        self.max_players = 99
        
        self.map_name = None
        self.server_name = None
        
        #gametypes
        self.gametype_bomb = True #bomb
        self.gametype_ts = True #team survivor
        self.gametype_ctf= True #capture the flag
        self.gametype_tdm = True #team deathmatch
        self.gametype_cah = True #capture and hold
        self.gametype_ftl = True #follow the leader
        self.gametype_ffa = True #free for all
        
        #gear settingsfilter
        self.gear_filter_type = self.DISABLED
        self.gear_value_list = []
        
        #servervars 
        self.server_var_list = []
        
        #buddy / playersearch list
        self.playerlist = []
        
    def initialize_from_stored_filter_settings(self):
        """
        Uses the stored filter settings provided by the FileManager to 
        initialize the values of the filter
        """
        fm = FileManager()
        sf = fm.get_remembered_filter_parameters()
        
        self.show_empty = fm.value_as_boolean(sf[filterkey.QRY_SHOW_EMPTY])
        self.show_full = fm.value_as_boolean(sf[filterkey.QRY_SHOW_FULL])
        
        self.hide_non_responsive = fm.value_as_boolean(sf[filterkey.\
                                                             FLT_HIDE_NON_RESP])
        self.hide_passworded = fm.value_as_boolean(sf[filterkey.\
                                                           FLT_HIDE_PASSWORDED])
        
        self.min_players = int(sf[filterkey.FLT_MIN_PLAYERS])
        self.max_players = int(sf[filterkey.FLT_MAX_PLAYERS])
        
        self.gametype_bomb = fm.value_as_boolean(sf[filterkey.GT_BOMB])
        self.gametype_ts = fm.value_as_boolean(sf[filterkey.GT_TS])
        self.gametype_ctf= fm.value_as_boolean(sf[filterkey.GT_CTF])
        self.gametype_tdm = fm.value_as_boolean(sf[filterkey.GT_TDM])
        self.gametype_cah = fm.value_as_boolean(sf[filterkey.GT_CAH])
        self.gametype_ftl = fm.value_as_boolean(sf[filterkey.GT_FTL])
        self.gametype_ffa = fm.value_as_boolean(sf[filterkey.GT_FFA])
        
        if filterkey.FLT_MAP_NAME in sf:
            self.map_name = sf[filterkey.FLT_MAP_NAME]
        
        if filterkey.FLT_SERVER_NAME in sf:
            self.server_name = sf[filterkey.FLT_SERVER_NAME]
            
        if filterkey.FLT_GEAR in sf:
            self.gear_filter_type = sf[filterkey.FLT_GEAR]
        
        if filterkey.FLT_GEAR_LIST in sf:
            self.gear_value_list = sf[filterkey.FLT_GEAR_LIST]
            
        if filterkey.FLT_VAR_LIST in sf:
            self.server_var_list = sf[filterkey.FLT_VAR_LIST]
        
    def is_urt_server(self, server):
        """
        this method contains all filter checks to make sure its a UrT server.
        currently this is only checked by looking for the gamename variable
        
        @param- the server to be checked
        
        @return True if server is a UrT server, otherwise False is returned
        """
        vars = server.getServerVars()
        if 'gamename' in vars and vars['gamename'] == 'q3ut4':
            return True
        else:
            return False
        
        
    def _does_basic_filter_match_server(self, server):
        """
        The checks used for the basic filter panel
        
        @returns true if the server matches the filter and should not be hidden
        """    
        # hide non responsove servers 
        if (server.getPing() == 999) \
                           and self.hide_non_responsive:
            Log.log.debug('[Filter] server filtered: ping > 999 - '\
                                                           + server.to_string())
            return False
        # hide passworded servers
        if server.needsPassword() \
                               and self.hide_passworded:
            Log.log.debug('[Filter] server filtered: passworded - '\
                                                           + server.to_string())
            return False
        
        
        gametype = server.getGameType()
        if gametype == '8' and not self.gametype_bomb:
            Log.log.debug('[Filter] server filtered: gametype is Bomb - '\
                                                           + server.to_string())
            return False
        elif gametype == '6' and not self.gametype_cah:
            Log.log.debug('[Filter] server filtered: gametype is CAH - '\
                                                           + server.to_string())
            return False
        elif gametype == '7' and not self.gametype_ctf: 
            Log.log.debug('[Filter] server filtered: gametype is CTF - '\
                                                           + server.to_string())
            return False
        elif gametype == '0' and not self.gametype_ffa:
            Log.log.debug('[Filter] server filtered: gametype is FFA - '\
                                                           + server.to_string())
            return False
        elif gametype == '3' and not self.gametype_tdm:
            Log.log.debug('[Filter] server filtered: gametype is TDM - '\
                                                           + server.to_string())
            return False
        elif gametype == '4' and not self.gametype_ts:
            Log.log.debug('[Filter] server filtered: gametype is TS - '\
                                                           + server.to_string())
            return False
        elif gametype == '5' and not self.gametype_ftl:
            Log.log.debug('[Filter] server filtered: gametype is FLT - '\
                                                           + server.to_string())
            return False
        
        if self.min_players > server.getClientCount():
            Log.log.debug('[Filter] server filtered: less than minimum players'\
                                                    +' - ' + server.to_string())
            return False
        
        if self.max_players < server.getClientCount():
            Log.log.debug('[Filter] server filtered: more than maximum players'\
                                                   + ' - ' + server.to_string())
            return False
   
        #no filtermatch so far, return True which results in displaying the server
        Log.log.debug('[Filter] server passed basic filter - '\
                                                           + server.to_string())
        return True
        
    def _does_adv_filter_match_server(self, server):
        """
        The checks used for the advanced filter panel
        
        @returns true if the server matches the filter and should not be hidden
        """    
        basic_result = self._does_basic_filter_match_server(server)
        server_vars = server.getServerVars()
        if not basic_result:
            # the server is not matching the basic filters so the advanced 
            # doesn't need to be processed and False can be returned
            return False   
        
        if not None == self.map_name and not len(self.map_name) == 0:
            if server.getMap().find(self.map_name) == -1: 
                #mapname does not match the filter for mapname
                #so return False
                Log.log.debug('[Filter] server filtered: mapname does not '\
                                             + 'match  - ' + server.to_string())
                return False
        
        if not None == self.server_name and not len(self.server_name) == 0:
            if server.getName().find(self.server_name) == -1: 
                #servername does not match the filter for servername
                #so return False
                Log.log.debug('[Filter] server filtered: servername does not '\
                                             + 'match  - ' + server.to_string())
                return False   
         
        #gear include filter   
        if not None == self.gear_filter_type and self.gear_filter_type \
                                                           == cfgvalues.INCLUDE:
            server_g_gear = server_vars['g_gear']
            result = False
            for value in self.gear_value_list:
                if server_g_gear == value:
                    result = True
                    break
                
            if not result: #g_gear not in include list!
                Log.log.debug('[Filter] server filtered: g_gear value does not'\
                                             + ' match  - ' + server.to_string())
                return False #do not display
            
            
        #gear exclude filter   
        if not None == self.gear_filter_type and self.gear_filter_type \
                                                           == cfgvalues.EXCLUDE:
            server_g_gear = server_vars['g_gear']
            for value in self.gear_value_list:
                if server_g_gear == value:
                    Log.log.debug('[Filter] server filtered: g_gear on exclude'\
                                             + ' list  - ' + server.to_string())
                    return False # do not display
                
           
        #custom var filter
        if not None == self.server_var_list:
            for value in self.server_var_list:
                varname = value[0]
                varvalue = value[1]
                filtertype = value[2]
                if cfgvalues.INCLUDE == filtertype: #Inlcude path
                    if not varname in server_vars:
                        Log.log.debug('[Filter] server filtered: var '\
                                + varname + ' not set  - ' + server.to_string())
                        return False #include - var must be set 
                    else: 
                        if not varvalue == server_vars[varname]:
                            Log.log.debug('[Filter] server filtered: var '\
                                              + varname + ' does not match  - '\
                                                           + server.to_string())
                            return False # value is not the same  
                elif cfgvalues.EXCLUDE == filtertype: #Exclude path
                    if varname in server_vars:
                        if varvalue == server_vars[varname]:
                            Log.log.debug('[Filter] server filtered: var '\
                                              + varname + ' on excludelist  - '\
                                                           + server.to_string())
                            return False # var is the same
        
        Log.log.debug('[Filter] server passed advanced filter - '\
                                                           + server.to_string())
        return True
        
    def _does_buddy_filter_match_server(self, server):
        """
        Checks if a player that is on the buddylist is playing on the passed
        server
        
        @param server - server to check
        
        @returns True if a buddy is playing on the server
        """
       
        Log.log.debug('[Filter] checking server' + server.to_string() \
                      + ' for playing buddies')
        playerlist = server.getPlayerList()
        
        #if there are no players on the server return true to hide the server
        if len(playerlist) == 0:
            return False
        
        retval = False
        for player in playerlist:
            for name in self.playerlist:
                status = False
                #we want also partial matches e.g. when searching for a clantag
                count = player.getName().find(name)
                if not count == -1:
                    #a match! set status to True, so that the server 
                    #will be displayed on the serverlist
                    status = True
                    retval  = True
                if not None == self.tab and status == True:
                    Log.log.debug('[Filter] - Buddy - ' + name + ' is online')
                    self.tab.update_buddy_status(name, True)
                status = False
                        
        #if the iteration returns no match, return False so that the server
        #will be hidden
        
        return retval
        
    def does_filter_match_server(self, server):
        """
        Checks if the filter applies a certain server
        
        @param the server to be checked
        
        @returns True if the server matches the filter (means should be
        displayed in a serverlist) - otherwise False
        """
        #check if the server is a UrT server, other servers are not interessting
        if not self.is_urt_server(server):
            Log.log.debug('[Filter] server filtered: not a q3ut4 server - '\
                                                           + server.to_string())
            return False
        
        if FilterType.BASIC_FILTER == self.type:
            return self._does_basic_filter_match_server(server)
        elif FilterType.ADVANCED_FILTER == self.type:
            return self._does_adv_filter_match_server(server)
        elif FilterType.BUDDY_FILTER == self.type:
            return self._does_buddy_filter_match_server(server)
        else:
            Log.log.warn('Unknown Filter passed ! Returning True!')
            return True