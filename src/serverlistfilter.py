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

from guicontroller import GuiController
import gtk
#from guicontroller import GuiController


class ServerListFilter(gtk.HBox):
    """
    UI Element containing the Filter setting (and also query) for the
    serverlist.
    """


    def __init__(self, parent):
        gtk.HBox.__init__(self)    
        
        
        queryframe = gtk.Frame('Query Parameters')
        queryframe.set_border_width(2)
        
        filterframe = gtk.Frame('Filter')
        filterframe.set_border_width(2)
        
        gametypesframe = gtk.Frame('Gametypes')
        gametypesframe.set_border_width(2)
        
        self.pack_start(queryframe, False, False)
        self.pack_start(filterframe, True, True)
        self.pack_start(gametypesframe, False, False)
        
        #query parameters, empty and full
        querybox = gtk.VBox()
        querybox.set_border_width(5)
                
        self.checkbox_showfull = gtk.CheckButton('show full')
        self.checkbox_showfull.show()
        self.checkbox_showempty = gtk.CheckButton('show empty')
        self.checkbox_showempty.show()
        # checkbox_showpassworded = gtk.CheckButton('show passworded')
        # checkbox_showpassworded.show()
        
        
        
        #filterframe content
        
        filtertable = gtk.Table(2,3)
        filtertable.set_border_width(5)
        
        filterframe.add(filtertable)
        
        self.checkbox_hide_non_responsive = gtk.CheckButton('hide non responsive')
        self.checkbox_hide_passworded = gtk.CheckButton('hide passworded')
        minplayerlabel = gtk.Label('min. players:')
        maxplayerlabel = gtk.Label('max. players:')
        self.minplayerentry = gtk.Entry()
        self.maxplayerentry = gtk.Entry()
        
        self.minplayerentry.set_width_chars(5)
        self.maxplayerentry.set_width_chars(5)
        
        
        filtertable.attach(self.checkbox_hide_non_responsive, 0,1,0,1 )
        filtertable.attach(self.checkbox_hide_passworded, 0,1,1,2 )
        filtertable.attach(minplayerlabel, 1,2,0,1 )
        filtertable.attach(maxplayerlabel, 1,2,1,2 )
        filtertable.attach(self.minplayerentry, 2,3,0,1 )
        filtertable.attach(self.maxplayerentry, 2,3,1,2 )
        
        
        querybox.pack_start(self.checkbox_showfull)
        querybox.pack_start(self.checkbox_showempty)
        queryframe.add(querybox)
        
        # gametype framecontent
        gametypetable = gtk.Table(2,4)
        gametypetable.set_border_width(5)
        gametypesframe.add(gametypetable)
        
        self.checkbox_show_gametype_all = gtk.CheckButton('all')
        self.checkbox_show_gametype_bomb = gtk.CheckButton('Bomb')
        self.checkbox_show_gametype_survivor = gtk.CheckButton('Survivor')
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
        
        
        
        
        #buttonbox
        buttonbox = gtk.VBox()
        buttonbox.set_border_width(5)
        self.pack_start(buttonbox, False, False)        
        
        resetbutton = gtk.Button('Reset')
        resetbutton.connect('clicked', self.on_reset_clicked)        
        resetimage = gtk.Image()
        resetimage.set_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_BUTTON)
        resetbutton.set_image(resetimage)
        buttonbox.pack_start(resetbutton)
        
                
        searchbutton = gtk.Button('Search')
        searchbutton.connect("clicked", self.on_search_clicked)
        searchimage = gtk.Image()
        searchimage.set_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_BUTTON)
        searchbutton.set_image(searchimage)
        buttonbox.pack_start(searchbutton)
        
        self.show_all()
        
    def on_reset_clicked(self):
        """
        Callback for reset the values of the filter to defaults
        """
        print 'reset'    
        
    def on_search_clicked(self, widget):
        """
        Callback for the search button - triggers the execution of the 
        master server query
        """
        guicontroller = GuiController()
        guicontroller.executeMasterServerQuery(self, self.parent)    
