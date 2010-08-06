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
from filemanager import FileManager
from aboutdialog import AboutDialog

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
        
        self.exe_entry.set_text(config['urt_executable'])
        self.path_entry.set_text(config['path_to_executable'])
        self.addcmd_entry.set_text(config['additional_commands'])
        
        defaulttab = int(config['default_tab'])
        if 0 == defaulttab:
            self.srvlist_radio.set_active(True)
        elif 1 == defaulttab:
            self.favlist_radio.set_active(True)
        elif 2 == defaulttab:
            self.reclist_radio.set_active(True)
        else:
            self.srvlist_radio.set_active(True)
        
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
        
        desc_label = gtk.Label('Choose the default tab that is displayed ' \
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
        
        self.buddies_radio = gtk.RadioButton(self.srvlist_radio, 'Start with' \
                                                      + '"Buddies" tab')
        vbox.pack_start(self.buddies_radio, True, True, 0)
        self.buddies_radio.set_border_width(5)
        
        return launchframe
    
    def on_save_clicked(self, widget):
        """
        Callback of the save button
        """
        fm = FileManager()
        config = fm.getConfiguration()
        config['urt_executable'] = self.exe_entry.get_text()
        config['path_to_executable'] = self.path_entry.get_text()
        config['additional_commands'] = self.addcmd_entry.get_text()
        
        defaulttab = 0
        if self.srvlist_radio.get_active():
            defaulttab = 0
        elif self.favlist_radio.get_active():
            defaulttab = 1
        elif self.reclist_radio.get_active():
            defaulttab = 2
        elif self.buddies_radio.get_active():
            defaulttab = 3
        
        config['default_tab'] = defaulttab
        
        
        fm.saveConfiguration()
    
   
        
    def on_about_clicked(self, widget):
        """
        Callback of the about button
        """
        about_dialog = AboutDialog()
        about_dialog.run()
        about_dialog.hide()
        
        