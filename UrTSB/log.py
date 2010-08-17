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
from logging.handlers import RotatingFileHandler
import logging

class Log(object):
    """
    This class handles the initialization of an application logger.
    """

    log = None

    def __init__(self, level=logging.INFO):
        """
        Constructor
        
        @parameter the loggin level to use
        """
        log_file = Globals.config_dir + '/urtsb.log'
        Log.log = logging.getLogger('UrTSB')
        #initialize logging
        #rotating filehandler using a 2MB logfile and keep 5 backups
        filehandler = RotatingFileHandler( \
                                      log_file, maxBytes=2097152, backupCount=5)
        FORMAT='%(asctime)s\t%(levelname)s\t%(message)s'
        formatter = logging.Formatter(FORMAT)
        logging.basicConfig(format=FORMAT) 
        filehandler.setFormatter(formatter)
        Log.log.addHandler(filehandler)
        Log.log.setLevel(level)
        