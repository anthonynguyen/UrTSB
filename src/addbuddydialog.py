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

class AddBuddyDialog(gtk.Dialog):
    """
    A dialog for adding a buddy to the buddylist
    """


    def __init__(self, parenttab):
        """
        Construct the dialog
        
        @param parenttab - the tab which started this dialog
        """
        gtk.Dialog.__init__(self, 'Add Buddy', None,\
                              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.parenttab = parenttab
    
        #buttons
        okbutton = gtk.Button('OK')
        cancelbutton = gtk.Button('Cancel')
        
        okbutton.connect("clicked", self.on_ok_clicked)
        cancelbutton.connect("clicked", self.on_cancel_clicked)
        
        
        self.action_area.pack_start(cancelbutton, False, False)
        self.action_area.pack_start(okbutton, False, False)
        
        #content area
        desc_label = gtk.Label('Enter the name or part of the name for the ' \
                               + 'buddy/player you like to add:')
        
        self.nameentry = gtk.Entry()
        self.nameentry.set_text('')
        
        
        self.vbox.pack_start(desc_label, False, False)
        
        self.vbox.pack_start(self.nameentry, False, False)
       
        
       
        self.show_all()
        
        
    def on_ok_clicked(self, widget):
            """
            Callback of the OK button
            """
            #get the entered name
            enteredname = self.nameentry.get_text()
            
            gc = GuiController()
            gc.add_name_to_buddylist(enteredname, self.parenttab)
            
            #afterwards close the dialog
            self.destroy()
            
    def on_cancel_clicked(self, widger):
            """
            Callback of the Cancel button
            """
            #do nothing just close the dialog
            self.destroy()
        