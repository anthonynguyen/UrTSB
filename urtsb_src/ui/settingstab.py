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




from urtsb_src.filemanager import FileManager, cfgkey, cfgvalues
from urtsb_src.ui.aboutdialog import AboutDialog
from urtsb_src.ui.servertab import ServerTab
import gtk

class SettingsTab(gtk.VBox):
    """
    Content of the settings tab.
    """


    def __init__(self):
        """
        Constructor
        """
        gtk.VBox.__init__(self)
        
        #add two hboxes
        hboxtop = gtk.HBox()
        hboxbottom = gtk.HBox()
        
        contentbox_topleft = gtk.HBox()
        hboxtop.pack_start(contentbox_topleft, False, True)
        
        vboxlaunch = gtk.VBox()
        launcherframe = self.create_launch_settings_frame()
        vboxlaunch.pack_start(launcherframe, False, False)
        
        tabframe = self.create_tab_settings_frame()
        vboxlaunch.pack_start(tabframe, False, False)
        
        contentbox_topleft.pack_start(vboxlaunch, True, True)
        
        self.pack_start(hboxtop, True, True)
        self.pack_start(hboxbottom, False, False)
            
        
        buttonbox = gtk.HBox()
        buttonbox.set_border_width(5)
        hboxbottom.pack_end(buttonbox, False, False)
        
        
        savebutton = gtk.Button('Save')
        savebutton.set_border_width(5)
    
        aboutbutton = gtk.Button('About UrTSB')
        aboutbutton.set_border_width(5)
        
               
        buttonbox.pack_end(savebutton, False, False)
        buttonbox.pack_end(aboutbutton, False, False)
       
        #callback connections
        savebutton.connect("clicked", self.on_save_clicked)
        aboutbutton.connect("clicked", self.on_about_clicked)
       
        self.set_defaults()
        
        self.show_all()
        
    def set_defaults(self):
        """
        Set ui input element values to the values read from configuration
        """    
        fm = FileManager()
        config = fm.getConfiguration()
        
        self.exe_entry.set_text(config[cfgkey.URT_EXE])
        self.path_entry.set_text(config[cfgkey.URT_EXE_PATH])
        self.addcmd_entry.set_text(config[cfgkey.URT_EXE_PARAMS])
        
        defaulttab = int(config[cfgkey.OPT_DEFAULT_TAB])
        if 0 == defaulttab:
            self.srvlist_radio.set_active(True)
            self.checkbox_buddysearch.set_sensitive(False)
            self.checkbox_buddysearch.set_active(False)
        elif 1 == defaulttab:
            self.favlist_radio.set_active(True)
            self.checkbox_buddysearch.set_sensitive(False)
            self.checkbox_buddysearch.set_active(False)
        elif 2 == defaulttab:
            self.reclist_radio.set_active(True)
            self.checkbox_buddysearch.set_sensitive(False)
            self.checkbox_buddysearch.set_active(False)
        elif 3 == defaulttab:
            self.buddies_radio.set_active(True)
            self.checkbox_buddysearch.set_sensitive(True)
            self.checkbox_buddysearch.set_active(fm.value_as_boolean(\
                                                config[cfgkey.OPT_BUDDYSEARCH]))
        else:
            self.srvlist_radio.set_active(True)
        
                   
        if cfgvalues.BASIC_FILTER == config[cfgkey.OPT_FILTER]:
            self.filter_basic_radio.set_active(True)
            self.filter_advanced_radio.set_active(False)
        elif cfgvalues.ADVANCED_FILTER == config[cfgkey.OPT_FILTER]:
            self.filter_basic_radio.set_active(False)
            self.filter_advanced_radio.set_active(True)
        else: #fallback to basic
            self.filter_basic_radio.set_active(True)
            self.filter_advanced_radio.set_active(False)
            
            
    def create_launch_settings_frame(self):
        """
        Creates a frame containing the settings needed to run Urban Terror
        """
        launchframe = gtk.Frame('Urban Terror Launch Settings')
        launchframe.set_border_width(2)
               
        launchtable = gtk.Table(3,2)
        launchtable.set_border_width(5)
        launchframe.add(launchtable)
        
        exe_label = gtk.Label('UrT Executable:')
        path_label = gtk.Label('Path to Executable:')
        addcmd_label= gtk.Label('Additional Parameters:')
        
        self.exe_entry = gtk.Entry()
        self.path_entry = gtk.Entry()
        self.addcmd_entry = gtk.Entry()
        
        self.exe_entry.set_width_chars(50)
        self.path_entry.set_width_chars(50)
        self.addcmd_entry.set_width_chars(50)
        
        launchtable.attach(exe_label,0,1,0,1)
        launchtable.attach(path_label,0,1,1,2)
        launchtable.attach(addcmd_label,0,1,2,3)
        
        launchtable.attach(self.exe_entry,1,2,0,1)
        launchtable.attach(self.path_entry,1,2,1,2)
        launchtable.attach(self.addcmd_entry,1,2,2,3)
        
        return launchframe
    
    
    def create_tab_settings_frame(self):
        """
        Creates a frame containing the settings that affects the window UI
        behaviour of UrTSB
        """
        launchframe = gtk.Frame('UrTSB Window Behaviour Settings')
        launchframe.set_border_width(2)
               
        vbox = gtk.VBox()
        launchframe.add(vbox)
        
        desc_label = gtk.Label('\nChoose the default tab that is displayed ' \
                                                     + 'directly after startup')
        vbox.pack_start(desc_label, True, True, 0)
        
        
        self.srvlist_radio = gtk.RadioButton(None, 'Start with "Servers" tab')
        vbox.pack_start(self.srvlist_radio, True, True, 0)
        self.srvlist_radio.set_border_width(5)   
        
       
        self.favlist_radio = gtk.RadioButton(self.srvlist_radio, 'Start with' \
                                                            + '"Favorites" tab')
        self.favlist_radio.set_active(True)
        vbox.pack_start(self.favlist_radio, True, True, 0)
        self.favlist_radio.set_border_width(5)
        
            
        self.reclist_radio = gtk.RadioButton(self.srvlist_radio, 'Start with' \
                                                      + '"Recently Played" tab')
        vbox.pack_start(self.reclist_radio, True, True, 0)
        self.reclist_radio.set_border_width(5)
        
        
        buddieoptionbox = gtk.HBox()
        
        self.buddies_radio = gtk.RadioButton(self.srvlist_radio, 'Start with' \
                                                      + '"Buddies" tab')
        vbox.pack_start(buddieoptionbox, True, True, 0)
        buddieoptionbox.pack_start(self.buddies_radio)
        self.buddies_radio.set_border_width(5)
        
        
        self.checkbox_buddysearch = gtk.CheckButton('Execute search for buddies '
                                                    + 'on startup')
        buddieoptionbox.pack_start(self.checkbox_buddysearch)
        
        
        self.srvlist_radio.connect('clicked', self.on_tab_checkbox_activate)
        self.favlist_radio.connect('clicked', self.on_tab_checkbox_activate)
        self.reclist_radio.connect('clicked', self.on_tab_checkbox_activate)
        self.buddies_radio.connect('clicked', self.on_tab_checkbox_activate)
       
        
        # filter option (choose basic or advanced filter)
        
        desc3_label = gtk.Label('\n\nFilter Options')
        vbox.pack_start(desc3_label)
        
        
        self.filter_basic_radio = gtk.RadioButton(None, 'use the basic filter' \
                                                                     + ' panel')
        self.filter_basic_radio.set_active(False)
        vbox.pack_start(self.filter_basic_radio, True, True, 0)
        self.filter_basic_radio.set_border_width(5)   
       
        self.filter_advanced_radio = gtk.RadioButton(self.filter_basic_radio, \
                                                      'use the advanced filter')
        vbox.pack_start(self.filter_advanced_radio, True, True, 0)
        self.filter_advanced_radio.set_border_width(5)
        
      
        
        
        return launchframe
    
    def on_save_clicked(self, widget):
        """
        Callback of the save button
        """
                
        fm = FileManager()
        config = fm.getConfiguration()
        config[cfgkey.URT_EXE] = self.exe_entry.get_text()
        config[cfgkey.URT_EXE_PATH] = self.path_entry.get_text()
        config[cfgkey.URT_EXE_PARAMS] = self.addcmd_entry.get_text()
        
        defaulttab = 0
        if self.srvlist_radio.get_active():
            defaulttab = 0
        elif self.favlist_radio.get_active():
            defaulttab = 1
        elif self.reclist_radio.get_active():
            defaulttab = 2
        elif self.buddies_radio.get_active():
            defaulttab = 3
        
        config[cfgkey.OPT_DEFAULT_TAB] = defaulttab
        
        if self.filter_basic_radio.get_active():
            config[cfgkey.OPT_FILTER] = cfgvalues.BASIC_FILTER
        elif self.filter_advanced_radio.get_active():
            config[cfgkey.OPT_FILTER] = cfgvalues.ADVANCED_FILTER
        else: #fallback
            config[cfgkey.OPT_FILTER] = cfgvalues.BASIC_FILTER
        
        
        config[cfgkey.OPT_BUDDYSEARCH] =\
                   fm.value_from_boolean(self.checkbox_buddysearch.get_active())
        
            
        #refresh the serverlist tab to make changes to the filter available 
        #without restart
        window = self.parent.parent.parent
        notebook = window.notebook
        notebook.remove_page(0)
        window.serverlisttab = ServerTab()
        srvlabel = gtk.Label('Serverlist')
        notebook.insert_page(window.serverlisttab, srvlabel, 0)        
        
        fm.saveConfiguration()
    
   
        
    def on_about_clicked(self, widget):
        """
        Callback of the about button
        """
        about_dialog = AboutDialog()
        about_dialog.run()
        about_dialog.hide()
        
    def on_tab_checkbox_activate(self, widget):
        """
        Callback executed when the radiobuttons are clicked
        enables disables the checkbox 
        """
        if widget == self.buddies_radio:
            self.checkbox_buddysearch.set_sensitive(True)
        else:
            self.checkbox_buddysearch.set_active(False)
            self.checkbox_buddysearch.set_sensitive(False)
            