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


class GametypesFilter(gtk.Frame):
    """
    A reusable ui element for choosing UrT Gametypes using checkboxes
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.Frame.__init__(self, 'Gametypes to show')
        
        gametypetable = gtk.Table(2,4)
        gametypetable.set_border_width(5)
        self.add(gametypetable)
        
        self.checkbox_show_gametype_all = gtk.CheckButton('all')
        self.checkbox_show_gametype_bomb = gtk.CheckButton('Bomb')
        self.checkbox_show_gametype_survivor = gtk.CheckButton('Team Survivor')
        self.checkbox_show_gametype_ctf = gtk.CheckButton('Capture the Flag')
        self.checkbox_show_gametype_tdm = gtk.CheckButton('Team Deathmatch')
        self.checkbox_show_gametype_cah = gtk.CheckButton('Capture and Hold')
        self.checkbox_show_gametype_ftl = gtk.CheckButton('Follow the Leader')
        self.checkbox_show_gametype_ffa = gtk.CheckButton('Free for all')
        
        gametypetable.attach(self.checkbox_show_gametype_all, 0,1,0,1 )
        gametypetable.attach(self.checkbox_show_gametype_bomb, 1,2,0,1 )
        gametypetable.attach(self.checkbox_show_gametype_survivor, 2,3,0,1 )
        gametypetable.attach(self.checkbox_show_gametype_ctf, 3,4,0,1 )
        gametypetable.attach(self.checkbox_show_gametype_tdm, 0,1,1,2 )
        gametypetable.attach(self.checkbox_show_gametype_cah, 1,2,1,2 )
        gametypetable.attach(self.checkbox_show_gametype_ftl, 2,3,1,2 )
        gametypetable.attach(self.checkbox_show_gametype_ffa, 3,4,1,2 )
        
        
        #callback connections
        self.gametype_all_handler = self.checkbox_show_gametype_all. \
                               connect('toggled', self.on_all_gametypes_toggled) 
        self.checkbox_show_gametype_bomb.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_survivor.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_ctf.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_tdm.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_cah.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_ftl.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        self.checkbox_show_gametype_ffa.connect('toggled', \
                                               self.on_gametype_checkbox_toggle) 
        
    def on_gametype_checkbox_toggle(self, togglebutton):
        """
        Callback for all gametype checkboxes except the 'all' (has its own
        callback).
        When an checbox is deactivated and the 'all' is active, then deactivate
        the all checkbox. 
        """    
        if not togglebutton.get_active():
            # deactivate callback for the all checkbutton
            # don't wan't to deacticate all other checkbutton!
            self.checkbox_show_gametype_all.disconnect(self.gametype_all_handler)
            
            # deactivate the all checkbutton 
            self.checkbox_show_gametype_all.set_active(False)
            
            # reactivate callback for the  all checkbutton
            self.gametype_all_handler = self.checkbox_show_gametype_all. \
                               connect('toggled', self.on_all_gametypes_toggled)
            
            
             
    def on_all_gametypes_toggled(self, togglebutton):
        """
        Callback for the 'all' gametypes checkbox on 'toggled' signal.
        Activates/Deactivates all other gametype checkboxes.
        """
        state =  togglebutton.get_active() 
        
        #set all other gametype checkboxes to the same state as the all checkbox
        self.checkbox_show_gametype_bomb.set_active(state)
        self.checkbox_show_gametype_survivor.set_active(state)
        self.checkbox_show_gametype_ctf.set_active(state)
        self.checkbox_show_gametype_tdm.set_active(state)
        self.checkbox_show_gametype_cah.set_active(state)
        self.checkbox_show_gametype_ftl.set_active(state)
        self.checkbox_show_gametype_ffa.set_active(state)
        
                