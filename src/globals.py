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
import os
import sys


class Globals(object):
    """
    Defines some global variables.
    
    This are the path to the configfolder and the location the py scripts are
    located.
    """
    
    configfolder = None
    scriptdir = None
    
    def __init__(self):
        """
        Constructor
        """
        #set up configfolder
        # linux specific! if someday UrTSB should run on another OS
        # this definitely needs to be extended
        
        Globals.scriptdir = sys.path[0]
        Globals.configfolder = os.path.expanduser('~/.urtsb/')
        if not os.path.exists(Globals.configfolder):
            try:
                os.makedirs(self.configfolder)
            except OSError:
                #fallback to scriptdir
                Globals.configfolder = Globals.scriptdir + '/'
                pass