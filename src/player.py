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

class Player(object):
    """
    Simple data "container" class holding information about a player on a game
    server - name, kills and ping.
    """
    
    def __init__(self, name, kills, ping):
        self.name = name
        self.kills = int(kills)
        self.ping = int(ping)
        
    def getName(self):
        return self.name
    
    def getKills(self):
        return self.kills
    
    def getPing(self):
        return self.ping