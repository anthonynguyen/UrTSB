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
import gtk
from guicontroller import GuiController

class RconWindow(gtk.Window):
    """
    A Rcon Console window 
    """


    def __init__(self, server):
        """
        Constructor
        """
        gtk.Window.__init__(self)
        self.server = server
        self.connect('destroy', self.on_closebutton_clicked)
        self.set_default_size(480, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title('RCON for - ' +self.server.getaddress())
        
        
        vbox = gtk.VBox()
        self.add(vbox)
        vbox.set_border_width(5)
        
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.messages = gtk.TextView()
        self.buffer = gtk.TextBuffer()
        self.messages.set_buffer(self.buffer)
        scrolled_window.add(self.messages)
        
        vbox.pack_start(scrolled_window, True, True)
        
        rconbox = gtk.HBox()
        vbox.pack_start(rconbox, False, False)
        
        self.input = gtk.Entry()
        rconbox.pack_start(self.input, True, True)
        sendbutton = gtk.Button('Send')
        statusbutton = gtk.Button('Status')
        clearbutton = gtk.Button('Clear')
        
        sendbutton.set_border_width(5)
        statusbutton.set_border_width(5)
        clearbutton.set_border_width(5)
        
        rconbox.pack_start(sendbutton, False, False)
        rconbox.pack_start(statusbutton, False, False)
        rconbox.pack_start(clearbutton, False, False)
        
        
        endbox = gtk.HBox()
        vbox.pack_start(endbox, False, False)
        closebutton = gtk.Button('Close')
        closebutton.set_border_width(5)
        
        closebutton.connect('clicked', self.on_closebutton_clicked)
        clearbutton.connect('clicked', self.on_clearbutton_clicked)
        sendbutton.connect('clicked', self.on_send_requested)
        self.input.connect('activate', self.on_send_requested)
        statusbutton.connect('clicked', self.on_status_button_clicked)
        
        endbox.pack_end(closebutton, False, False)
        
        self.show_all()
        
        
    def add_server_response(self, response): 
        """
        Adds the response of the server to the textview
        """   
        #enditer = self.buffer.get_end_iter()
        #self.buffer.insert(enditer, response)
        self.buffer.insert_at_cursor(response)
        #self.messages.scroll_to_iter(self.buffer.get_end_iter(), 0.0, False, 0.0, 0.0)
        self.messages.scroll_to_mark(self.buffer.get_insert(), 0)
        
    def on_status_button_clicked(self, button):    
        """
        Callback of the status button
        Performs the 'rcon status' command
        """
        rcon_command = 'status'
        self.buffer.insert_at_cursor('rcon > status\n')
        gc = GuiController()
        gc.send_rcon_command(self.server, rcon_command, self)
        
    def on_send_requested(self, widget):
        """
        Callback of the send button
        """    
        rcon_command = self.input.get_text()
        gc = GuiController()
        
        self.buffer.insert_at_cursor('rcon > ' + rcon_command + '\n')
        self.input.set_text('')
        
        gc.send_rcon_command(self.server, rcon_command, self)
        
        
    def on_clearbutton_clicked(self, button):
        """
        Callback of the clear button.
        Clears the textview
        """    
        self.buffer.set_text('')
        
    def on_closebutton_clicked(self, button):
        """
        Callback of the close button.
        Closes the window
        """
        self.destroy()
        