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



from urtsb_src.filemanager import FileManager, cfgkey
from urtsb_src.guicontroller import GuiController
import gtk

class PassDialogType():
    """
    Class as enum like value definition of possible passworddialog types
    """
    SERVER_PASSWORD = 0
    PRIV_SLOT_PASSWORD = 1

class PasswordDialog(gtk.Dialog):
    """
    A dialog for entering the password for a passworded game server
    """


    def __init__(self, server, type):
        """
        Constructor
        
        @param server - the server which needs a password
        @param type - value of PassDialogType to specify the type of the dialog
                      two possible values:
                         - SERVER_PASSWOR - enter password for private password
                         - PRIV_SLOT_PASSWORD - enter password for private slots
        """
        gtk.Dialog.__init__(self, 'Server needs a password to connect!', None,\
                              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        
        self.server = server
        self.diag_type = type
        #buttons
        okbutton = gtk.Button('OK')
        cancelbutton = gtk.Button('Cancel')
        
        okbutton.connect("clicked", self.on_ok_clicked)
        cancelbutton.connect("clicked", self.on_cancel_clicked)
        
        
        self.action_area.pack_start(cancelbutton, False, False)
        self.action_area.pack_start(okbutton, False, False)
        
        #content area
        desc_label = gtk.Label('Enter Password')
        if PassDialogType.SERVER_PASSWORD == self.diag_type:
            desc_label.set_text('The server you are trying to connect needs a '\
                                +'password')
        elif PassDialogType.PRIV_SLOT_PASSWORD == self.diag_type:
            desc_label.set_text('The server is full. In order to use a private'\
                            + 'slot please enter the private slot password')
        namelabel = gtk.Label('Servername: ' + server.getName())
        addresslabel = gtk.Label('Serveraddress: ' + server.getaddress())
        self.passentry = gtk.Entry()
        self.passentry.set_visibility(False)
        self.passentry.set_text(server.getPassword())
        self.remembercheckbutton = gtk.CheckButton('remember password')
        
        self.vbox.pack_start(desc_label, False, False)
        self.vbox.pack_start(namelabel, False, False)
        self.vbox.pack_start(addresslabel, False, False)
        self.vbox.pack_start(self.passentry, False, False)
        self.vbox.pack_start(self.remembercheckbutton, False, False)
        
        fm = FileManager()
        config = fm.getConfiguration()
        save_password = config[cfgkey.OPT_SAVE_PW]
        if 'True' == save_password:
            self.remembercheckbutton.set_active(True)
        else:
            self.remembercheckbutton.set_active(False)
        
        self.show_all()
        
        
    def on_ok_clicked(self, widget):
            """
            Callback of the OK button
            """
            #get the entered password
            password = self.passentry.get_text()
            #set the password at the server object
            self.server.setPassword(password)
            
            #set rememberpassword option
            self.server.setRememberPassword(self.remembercheckbutton.get_active())
            
            #and connect...
            gui = GuiController()
            gui.connectToServer(self.server)
            #afterwards close the dialog
            self.destroy()
            
    def on_cancel_clicked(self, widger):
            """
            Callback of the Cancel button
            """
            #do nothing just close the dialog
            self.destroy()
        
        