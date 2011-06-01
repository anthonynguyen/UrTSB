#
# Copyright (C) 2011  Sorcerer
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

from filemanager import FileManager, cfgkey
from log import Log
import gtk
import os.path
import shlex
import subprocess

class ConnectionManager(object):
    """
    Handling Urban Terror connections - launches and monitors
    Urban Terror Game instances (currently only one instance launched by 
    UrTSB is allowed, if someone can tell me a usecase where more than one 
    instance is needed, maybe I will implement support for more instances ;) )
    When a new server connection is requested the status of the server
    is updated and checked if there are empty slots available. If not
    display a message dialog (supports private slots).
    """
    
    __shared_state = {} # borg pattern
    
    instance = None
    
    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__shared_state # borg pattern
            
        if not self.instance:
            self.instance = True
            
            #initialize process varible to None
            #will store the process of the launched Urban Terror instance
            self.urt_process = None

    def connectToServer(self, server):
        """
        Launches Urban Terror and connect to the passed server
        
        @param server - the server to connect to 
        """
        Log.log.debug('[GuiController] connectToServer called...')
        
        #check if there is already a running process
        #if so display a dialog and inform the user
        #but do not launch a second instance
        if self.__isUrTrunning():
            self.__displayUrTRunningDialog()
            return

        #perform the connection
        self.__connect(server)
        
        
    def __isUrTrunning(self):
        """
        checks if there is already a UrT instance running (launched by UrTSB)
        Returns False if no instance is running, otherwise True.
        """
        if not None == self.urt_process:
            self.urt_process.poll()
            returncode = self.urt_process.returncode
            if None == returncode:
                return True
            return False
        
        
    def __displayUrTRunningDialog(self):
        """
        Displays the message dialog to inform the user that UrT is already
        running.
        """
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK,
        message_format = "Urban Terror is already running! Please exit" \
                       + " it before launching a new instance")
        dialog.set_title('Urban Terror is already running')
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.run()
        
    def __connect(self, server):
        """
        launch Urban Terror and connect to the passed server
        """
        fm = FileManager()
        
        
        #build the connect parameters
        #format of the commandline command:
        #urbanterror + connect <address> + password <pw>
        
        #get the executablename, the path and the additional commands
        #from the configuration
        config = fm.getConfiguration()
        executable = config[cfgkey.URT_EXE]
        path = config[cfgkey.URT_EXE_PATH]
        additionalcommands = config[cfgkey.URT_EXE_PARAMS]
                
        if not os.path.exists(os.path.join(path, executable)):
            Log.log.warning('path to Urban Terror unreachable : ' + os.path.join(path, executable))
        params = ' +connect ' + server.getaddress()
        if server.needsPassword():
            params = params + ' +password ' + server.getPassword()
            if server.getRememberPassword():
                if server.isFavorite():
                    fm.saveFavorites()
            else:
                server.setPassword('')
        
        #add additional params    
        params = params + ' ' + additionalcommands
                
        #add server to recent servers list
        fm.addRecent(server)
                
        Log.log.info('launching UrT with cmd = ' + os.path.join(path,\
                                                     executable) + ' ' + params)
        #use shlex.split to turn the command string into a sequence
        #that works with subprocess.popen
        args = shlex.split(executable + ' ' + params)
        
        #finally execute the command 
        self.urt_process = subprocess.Popen(args, executable=os.path.join(path,\
                                        executable), cwd=os.path.normpath(path))
        