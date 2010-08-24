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
from urtsb_src.globals import Globals
from urtsb_src.guicontroller import GuiController
from urtsb_src.ui.buddiestab import BuddiesTab
from urtsb_src.ui.favoritestab import FavoritesTab
from urtsb_src.ui.recenttab import RecentTab
from urtsb_src.ui.servertab import ServerTab
from urtsb_src.ui.settingstab import SettingsTab
import gtk







class Window():
    """
    This class is the entry point of the UI part of UrTSB.
    It creates the GTK Window.
    """    
    
    
    def __init__(self):
        """
        Constructor. Creating and inititializing the main window of UrTSB.
        """
        
        #window creation and basic window settings
        self.window = gtk.Window()
        gc = GuiController()
        self.window.set_title(gc.appname + ' v.' + gc.appver + ' - ' + gc.appdesc)
        self.window.set_icon_from_file(Globals.icon_dir +'/logo.png')
        self.window.set_default_size(1024, 768)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('destroy', gtk.main_quit)
          
          
        # add a VBox that will contain the main notebookpane and a statusbar  
        mainbox = gtk.VBox()  
        self.window.add(mainbox)  
         
        # the notebook - tabs will be serverlist, favorites,
        # recent servers and settings 
        self.notebook= gtk.Notebook()
        self.notebook.set_border_width(2)
        mainbox.pack_start(self.notebook)
        self.notebook.connect('switch-page', self.on_tab_change)
        
        
        # add the serverlist tab
        self.serverlisttab = ServerTab()
        srvlabel = gtk.Label('Serverlist')        
        self.notebook.append_page(self.serverlisttab, srvlabel)
        
        # add the favorites tab
        self.favoritestab = FavoritesTab()
        favlabel = gtk.Label('Favorites')        
        self.notebook.append_page(self.favoritestab, favlabel)
        
        # add the recently played tab
        self.recenttab = RecentTab()
        recentlabel = gtk.Label('Recently Played')        
        self.notebook.append_page(self.recenttab, recentlabel)
        
        # add the buddies tab
        self.buddiestab = BuddiesTab()
        buddieslabel = gtk.Label('Buddies')
        self.notebook.append_page(self.buddiestab, buddieslabel)
        
        # add the settings tab
        self.settingsstab = SettingsTab()
        settingslabel = gtk.Label('Settings')        
        self.notebook.append_page(self.settingsstab, settingslabel)
        
        #set default tab
        fm = FileManager()
        config = fm.getConfiguration()
        defaulttab = int(config[cfgkey.OPT_DEFAULT_TAB])
        self.notebook.set_current_page(defaulttab)
        
        #connect key press event to be able to create keyboard shortcuts
        self.window.connect('key-press-event', self.on_key_pressed_event)
       
        
        self.window.show_all()


       
    def on_tab_change(self, notebook, page, page_num):
        """
        Callback method handling tab changes.
        
        @param notebook - the notebook instance
        @param page - notebookpage 
        @param page_num - number of the current page 
        
        """
        #load favorites and recent servers directly if switched to
        #these tabs 
        gc = GuiController()
        if 1 == page_num: #favorites
            #gc.loadFavorites(self.favoritestab)
            gc.executeFavoritesLoading(self.favoritestab)
        if 2 == page_num: #recent server
            #gc.loadRecentServer(self.recenttab)
            gc.executeRecentServersLoading(self.recenttab)
        if 3 == page_num: #buddies tab
            gc.execute_buddies_loading(self.buddiestab)
            
    def refresh(self):
        """
        refresh of the serverdetails view of the currently active tab of the
        currently selected server
        """        
        
        #get the current tab
        pagenum = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(pagenum)
        
        selection = tab.serverlist.serverlistview.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            row =  model[paths[0][0]]
            server = row[8]
            guicontroller = GuiController()
            guicontroller.setDetailServer(server, tab)
            
    def on_key_pressed_event(self, widget, event):
        """
        Handling of keyboard events
        """
        # handle F5 key to call a refresh
        if 'F5' == gtk.gdk.keyval_name(event.keyval):
            self.refresh()