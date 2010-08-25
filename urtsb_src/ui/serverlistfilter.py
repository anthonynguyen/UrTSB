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



from threading import Thread
from urtsb_src.filemanager import FileManager, filterkey
from urtsb_src.filter import Filter, FilterType
from urtsb_src.guicontroller import GuiController
from urtsb_src.ui.gametypes_filter import GametypesFilter
import gtk



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
        
        self.gametypes = GametypesFilter()
        self.gametypes.set_border_width(2)
        
        self.pack_start(queryframe, False, False)
        self.pack_start(filterframe, True, True)
        self.pack_start(self.gametypes, False, False)
        
        #query parameters, empty and full
        querybox = gtk.VBox()
        querybox.set_border_width(5)
                
        self.checkbox_showfull = gtk.CheckButton('show full')
        self.checkbox_showfull.show()
        self.checkbox_showempty = gtk.CheckButton('show empty')
        self.checkbox_showempty.show()
        
        
        
        #filterframe content
        
        filtertable = gtk.Table(2,3)
        filtertable.set_border_width(5)
        
        filterframe.add(filtertable)
        
        self.checkbox_hide_non_responsive = gtk.CheckButton('hide non responsive')
        self.checkbox_hide_passworded = gtk.CheckButton('hide passworded')
        minplayerlabel = gtk.Label('min. players:')
        maxplayerlabel = gtk.Label('max. players:')
      
        self.minplayerentry = gtk.SpinButton()
        self.maxplayerentry = gtk.SpinButton()
        
        self.minplayerentry.set_range(0,99)
        self.maxplayerentry.set_range(0,99)
             
        filtertable.attach(self.checkbox_hide_non_responsive, 0,1,0,1 )
        filtertable.attach(self.checkbox_hide_passworded, 0,1,1,2 )
        filtertable.attach(minplayerlabel, 1,2,0,1 )
        filtertable.attach(maxplayerlabel, 1,2,1,2 )
        filtertable.attach(self.minplayerentry, 2,3,0,1 )
        filtertable.attach(self.maxplayerentry, 2,3,1,2 )
        
        querybox.pack_start(self.checkbox_showfull)
        querybox.pack_start(self.checkbox_showempty)
        queryframe.add(querybox)
        
        #buttonbox
        buttonbox = gtk.VBox()
        buttonbox.set_border_width(5)
        self.pack_start(buttonbox, False, False)        
        
        resetbutton = gtk.Button('Reset')
        resetbutton.connect('clicked', self.on_reset_clicked)        
        resetimage = gtk.Image()
        resetimage.set_from_stock(gtk.STOCK_REVERT_TO_SAVED,\
                                                           gtk.ICON_SIZE_BUTTON)
        resetbutton.set_image(resetimage)
        buttonbox.pack_start(resetbutton)
        
                
        self.searchbutton = gtk.Button('Search')
        self.searchbutton.connect("clicked", self.on_search_clicked)
        searchimage = gtk.Image()
        searchimage.set_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_BUTTON)
        self.searchbutton.set_image(searchimage)
        buttonbox.pack_start(self.searchbutton)
        
        
        self.set_default_values(False)
        
        self.show_all()
        
        
    def set_default_values(self, reset):
        """
        Set default values to all input elements of the filter.
        Differs between application defaults and the values that are stored
        in a file to remember user choices.
        
        @param reset - boolean: if True use application defaults, otherwise load
                       values from file. 
       
        """
        
        fm = FileManager()
        stored_filter = fm.get_remembered_filter_parameters()
        
        if reset or None == stored_filter: #reset to application defaults            
            self.gametypes.checkbox_show_gametype_all.set_active(True)
            # emits the 'toggled' signal
            self.gametypes.checkbox_show_gametype_all.toggled() 
            
            self.checkbox_hide_non_responsive.set_active(True)
            self.checkbox_hide_passworded.set_active(True)
            
            #defaults for min and maxplayer spinbuttons
            self.minplayerentry.set_value(0)
            self.maxplayerentry.set_value(99)
            
            self.checkbox_showfull.set_active(False)
            self.checkbox_showempty.set_active(False)
        else: #reset to stored values
            
            #gametypes
            value = fm.value_as_boolean(stored_filter[filterkey.GT_ALL])
            self.gametypes.checkbox_show_gametype_all.set_active(True)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_BOMB])
            self.gametypes.checkbox_show_gametype_bomb.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_TS])
            self.gametypes.checkbox_show_gametype_survivor.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_CTF])
            self.gametypes.checkbox_show_gametype_ctf.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_TDM])
            self.gametypes.checkbox_show_gametype_tdm.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_CAH])
            self.gametypes.checkbox_show_gametype_cah.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_FTL])
            self.gametypes.checkbox_show_gametype_ftl.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_FFA])
            self.gametypes.checkbox_show_gametype_ffa.set_active(value)
            
            #other filters:
            #defaults for min and maxplayer spinbuttons
            value = int(stored_filter[filterkey.FLT_MIN_PLAYERS])
            self.minplayerentry.set_value(value)
            
            value = int(stored_filter[filterkey.FLT_MAX_PLAYERS])
            self.maxplayerentry.set_value(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.\
                                                             FLT_HIDE_NON_RESP])
            self.checkbox_hide_non_responsive.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.\
                                                           FLT_HIDE_PASSWORDED])
            self.checkbox_hide_passworded.set_active(value)
            
            #query params
            value = fm.value_as_boolean(stored_filter[filterkey.QRY_SHOW_FULL])
            self.checkbox_showfull.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.QRY_SHOW_EMPTY])
            self.checkbox_showempty.set_active(value)
        
    def on_reset_clicked(self, button):
        """
        Callback for reset the values of the filter to defaults
        """
        self.set_default_values(True)
        
    def on_search_clicked(self, widget):
        """
        Callback for the search button - triggers the execution of the 
        master server query
        """
        #disable the button, so that no multiple queries are launched while
        #still one is active
        self.lock()
        #update the filter dict of the filemanager
        self.save_filter()
        
        filter = Filter(FilterType.BASIC_FILTER)
        filter.initialize_from_stored_filter_settings()    
        
        guicontroller = GuiController()
        guicontroller.executeMasterServerQuery(filter, self.parent)    
     
    
    def save_filter(self):
        """
        writes the current filter/query params to the filter dict
        """
        fm = FileManager()
        filter = fm.get_remembered_filter_parameters()
        if not filter: 
            # TODO: clean up this dirty hack ;)
            fm.filter = {}
            filter = fm.filter
        
        #process gametypes
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_all.get_active())
        filter[filterkey.GT_ALL] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                       checkbox_show_gametype_bomb.get_active())
        filter[filterkey.GT_BOMB] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                   checkbox_show_gametype_survivor.get_active())
        filter[filterkey.GT_TS] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_ctf.get_active())
        filter[filterkey.GT_CTF] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_tdm.get_active())
        filter[filterkey.GT_TDM] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_cah.get_active())
        filter[filterkey.GT_CAH] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_ftl.get_active())
        filter[filterkey.GT_FTL] = value
        
        value = fm.value_from_boolean(self.gametypes.\
                                        checkbox_show_gametype_ffa.get_active())
        filter[filterkey.GT_FFA] = value
        
        #other filters
        filter[filterkey.FLT_MIN_PLAYERS] = self.\
                                               minplayerentry.get_value_as_int()
        filter[filterkey.FLT_MAX_PLAYERS] = self.\
                                               maxplayerentry.get_value_as_int()
        
        value = fm.value_from_boolean(self.\
                                      checkbox_hide_non_responsive.get_active())
        filter[filterkey.FLT_HIDE_NON_RESP] = value
        
        value = fm.value_from_boolean(self.\
                                          checkbox_hide_passworded.get_active())
        filter[filterkey.FLT_HIDE_PASSWORDED] = value
        
        #query params
        value = fm.value_from_boolean(self.checkbox_showfull.get_active())
        filter[filterkey.QRY_SHOW_FULL] = value
        
        value = fm.value_from_boolean(self.checkbox_showempty.get_active())
        filter[filterkey.QRY_SHOW_EMPTY] = value
        
        
        #write to file
        t = Thread(target=fm.save_filter_to_remember)
        t.setDaemon(True)
        t.start()
        
        
    
    def get_filter_name(self):
        """
        Returns a string to identify this filter
        
        @return identificationstring of this filter
        """
        return 'serverlistfilter' 
    
    def lock(self):
        """
        Locks the UI-Elements for search so no two concurrent 
        requests can be executed!
        """
        self.searchbutton.set_sensitive(False)
        
    def unlock(self):
        """
        Unlocks the UI Elements for search after the request
        has finished.
        """
        self.searchbutton.set_sensitive(True)
