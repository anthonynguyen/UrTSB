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


from favoritestab import FavoritesTab

from recenttab import RecentTab
from servertab import ServerTab
from settingstab import SettingsTab


import gtk
from guicontroller import GuiController
from filemanager import FileManager



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
        self.window.set_default_size(1024, 768)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('destroy', gtk.main_quit)
          
          
        # add a VBox that will contain the main notebookpane and a statusbar  
        mainbox = gtk.VBox()  
        self.window.add(mainbox)  
         
        # the notebook - tabs will be serverlist, favorites,
        # recent servers and settings 
        notebook= gtk.Notebook()
        notebook.set_border_width(2)
        mainbox.pack_start(notebook)
        notebook.connect('switch-page', self.on_tab_change)
        
        
        # add the serverlist tab
        self.serverlisttab = ServerTab()
        srvlabel = gtk.Label('Serverlist')        
        notebook.append_page(self.serverlisttab, srvlabel)
        
        # add the favorites tab
        self.favoritestab = FavoritesTab()
        favlabel = gtk.Label('Favorites')        
        notebook.append_page(self.favoritestab, favlabel)
        
        # add the recently played tab
        self.recenttab = RecentTab()
        recentlabel = gtk.Label('Recently Played')        
        notebook.append_page(self.recenttab, recentlabel)
        
        # add the settings tab
        self.settingsstab = SettingsTab()
        settingslabel = gtk.Label('Settings')        
        notebook.append_page(self.settingsstab, settingslabel)
        
        #set default tab
        fm = FileManager()
        config = fm.getConfiguration()
        defaulttab = int(config['default_tab'])
        notebook.set_current_page(defaulttab)
        
        # add a statusbar with a progressbar inside
#        statusbar = gtk.Statusbar()
#        statusbar.set_border_width(2)
#        
#        self.progressbar = gtk.ProgressBar()
#        statusbar.add(self.progressbar)
#        mainbox.pack_start(statusbar, False, False) 
       
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
            gc.loadFavorites(self.favoritestab)
        if 2 == page_num: #recent server
            gc.loadRecentServer(self.recenttab)
