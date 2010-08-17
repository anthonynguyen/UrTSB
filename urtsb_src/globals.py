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
    
    app_name = 'UrTSB'
    app_ver = '0.4'
    app_desc = 'a Urban Terror Server Browser'
    
    app_root = None
    package_dir= None
    resource_dir = None
    configfolder = None
    
    icon_dir = None
    geoip_dir = None
    flag_dir = None
    
    
    @staticmethod
    def initialize(packagepath):
        """
        static init method to initialize static variables
        """
        Globals.package_dir = packagepath
        Globals.app_root = os.path.normpath(os.path.join(Globals.package_dir,\
                                                                         '../'))
        Globals.resource_dir = os.path.join(Globals.package_dir, 'resource')
        Globals.config_dir = Globals.__determine_config_dir()
        
        # resource dirs 
        Globals.icon_dir = os.path.join(Globals.resource_dir, 'icons')
        Globals.geoip_dir = os.path.join(Globals.resource_dir, 'geoip')
        Globals.flag_dir = os.path.join(Globals.resource_dir, 'flags')
        
        print Globals.package_dir + '   - (package_dir)'
        print Globals.app_root + '   - (app_root)'
        print Globals.resource_dir + '   - (resource_dir)'
        print Globals.config_dir + '    - (config_dir)'
    
    @staticmethod
    def __determine_config_dir():
        config_dir = os.path.expanduser('~/.urtsb/')
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except OSError:
                #fallback to app root
                config_dir = os.path.join(Globals.package_dir,'../')
                pass
        return config_dir
    
