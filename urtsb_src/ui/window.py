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
from urtsb_src.filter import Filter, FilterType
from urtsb_src.globals import Globals
from urtsb_src.guicontroller import GuiController
from urtsb_src.log import Log
from urtsb_src.ui.buddiestab import BuddiesTab
from urtsb_src.ui.favoritestab import FavoritesTab
from urtsb_src.ui.recenttab import RecentTab
from urtsb_src.ui.servertab import ServerTab
from urtsb_src.ui.settingstab import SettingsTab
import gtk







class Window(gtk.Window):
    """
    This class is the entry point of the UI part of UrTSB.
    It creates the GTK Window.
    """    
    #override configure event to react in window resize
    __gsignals__ = {
        "configure-event" : "override"
        }
    
    instance= None
    
    def __init__(self):
        """
        Constructor. Creating and inititializing the main window of UrTSB.
        """
        gtk.Window.__init__(self)
        Window.instance = self
        
        #window creation and basic window settings
        fm = FileManager()
        window_sizing = fm.get_window_sizing()
        
        gc = GuiController()
        self.set_title(gc.appname + ' v.' + gc.appver + ' - ' + gc.appdesc)
        self.set_icon_from_file(Globals.icon_dir +'/logo.png')
        
        if window_sizing.maximized:
            self.maximize()
        else:
            self.unmaximize()
        self.set_default_size(window_sizing.width, window_sizing.height)
        if None == window_sizing.x and None == window_sizing.y:
            self.set_position(gtk.WIN_POS_CENTER)
        else:
            self.move(window_sizing.x, window_sizing.y)
        self.connect('destroy', gtk.main_quit)
          
          
        # add a VBox that will contain the main notebookpane and a statusbar  
        mainbox = gtk.VBox()  
        self.add(mainbox)  
         
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
        #this variable is used to dertermine if the tabswitch is the first
        #after application start 
        self.first_switch = True
        
        self.notebook.set_current_page(defaulttab)
        
        #connect key press event to be able to create keyboard shortcuts
        self.connect('key-press-event', self.on_key_pressed_event)
       
        #connect window-state-event to handle maximize/demaximize
        self.connect('window-state-event', self.on_window_state_changed)
        
        self.show_all()

    def do_configure_event(self, event):
        """
        overrides the default do_configure_event method
        handles window move and resize and stores this information
        """
        fm = FileManager()
        window_sizing = fm.get_window_sizing()
        window_sizing.width = event.width
        window_sizing.height = event.height
        window_sizing.x = event.x
        window_sizing.y = event.y
        
        Log.log.debug('Window: size = ' + str(window_sizing.width) + 'x' +
                      str(window_sizing.height) + '  position = ' +
                      str(window_sizing.x) + ', ' + str(window_sizing.y))
        
        gtk.Window.do_configure_event(self, event)
       
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
            self.favoritestab.filter.lock()
        if 2 == page_num: #recent server
            #gc.loadRecentServer(self.recenttab)
            gc.executeRecentServersLoading(self.recenttab)
            self.recenttab.filter.lock()
        if 3 == page_num: #buddies tab
            fm = FileManager()
            config = fm.getConfiguration()
            execute = fm.value_as_boolean(config[cfgkey.OPT_BUDDYSEARCH])
            if self.first_switch and execute:
                gc.execute_buddies_loading(self.buddiestab, execute=True)
            else:
                gc.execute_buddies_loading(self.buddiestab)
                 
        self.first_switch = False
            
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
            
    def on_window_state_changed(self, window, event):
        """
        Callback of the def "window-state-event"
        Needed to handle maximize/demaximize of the window
        """
        fm = FileManager()
        window_sizing = fm.get_window_sizing()
        if event.new_window_state & gtk.gdk.WINDOW_STATE_MAXIMIZED:
            Log.log.debug('UrTSB Window maximized')
            window_sizing.maximized = True
        else:
            Log.log.debug('UrTSB Window not maximized')
            window_sizing.maximized = False