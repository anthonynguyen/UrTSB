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



from rconwindow import RconWindow
from urtsb_src.filemanager import FileManager
import gtk


class RconPassDialog(gtk.Dialog):
    """
    A dialog for entering the RCON password for a game server
    """


    def __init__(self, server):
        """
        Constructor
        
        @param server - the server which needs a password
        """
        gtk.Dialog.__init__(self, 'RCON Password needed!', None,\
                              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        
        self.server = server
        #buttons
        okbutton = gtk.Button('OK')
        cancelbutton = gtk.Button('Cancel')
        
        okbutton.connect("clicked", self.on_ok_clicked)
        cancelbutton.connect("clicked", self.on_cancel_clicked)
        
        
        self.action_area.pack_start(cancelbutton, False, False)
        self.action_area.pack_start(okbutton, False, False)
        
        #content area
        desc_label = gtk.Label('Please enter the RCON password for:')
        namelabel = gtk.Label('Servername: ' + server.getName())
        addresslabel = gtk.Label('Serveraddress: ' + server.getaddress())
        self.passentry = gtk.Entry()
        self.passentry.set_visibility(False)
        self.passentry.set_text('')
        self.remembercheckbutton = gtk.CheckButton('remember password')
        self.remembercheckbutton.set_active(False)
                
        self.vbox.pack_start(desc_label, False, False)
        self.vbox.pack_start(namelabel, False, False)
        self.vbox.pack_start(addresslabel, False, False)
        self.vbox.pack_start(self.passentry, False, False)
        self.vbox.pack_start(self.remembercheckbutton, False, False)
        
        
        #check if there is a stored rcon pw for the server
        fm = FileManager()
        rconpws = fm.get_rcon_passwords()
        if server.getaddress() in rconpws:
            pw = rconpws[server.getaddress()]
            
            self.passentry.set_text(pw)
            self.remembercheckbutton.set_active(True)
        
        self.show_all()
        
        
    def on_ok_clicked(self, widget):
            """
            Callback of the OK button
            """
            #get the entered password
            self.server.rconpass = self.passentry.get_text()
            
            #store the password if checkbox is active
            if self.remembercheckbutton.get_active():
                fm = FileManager()
                rconpws = fm.get_rcon_passwords()
                rconpws[self.server.getaddress()] = self.server.rconpass
                fm.save_rcon_passwords() 
            
            #display the rcon window
            rconwin= RconWindow(self.server)
            rconwin.show_now()
            self.destroy()
            
            
    def on_cancel_clicked(self, widger):
            """
            Callback of the Cancel button
            """
            #do nothing just close the dialog
            
            self.destroy()
        
        