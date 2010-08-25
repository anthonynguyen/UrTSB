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
from urtsb_src.ui.gametypes_filter import GametypesFilter
import gtk

class AdvancedFilterWindow(gtk.Dialog):
    """
    
    """


    def __init__(self, filter):
        """
        Constructor
        """
        gtk.Dialog.__init__(self, 'Advanced Filter Settings', None,\
                              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.set_default_size(700, 500)
        self.filter = filter
        #buttons
        applybutton = gtk.Button('Apply')
        cancelbutton = gtk.Button('Cancel')
        
        applybutton.connect("clicked", self.on_apply_clicked)
        cancelbutton.connect("clicked", self.on_cancel_clicked)
        
        
        self.action_area.pack_start(cancelbutton, False, False)
        self.action_area.pack_start(applybutton, False, False)
        
        self.setup_filter_elements()
        
        self.set_default_values(False)
        
        self.show_all()
        
    def setup_filter_elements(self):
        """
        setup the filter elements
        """
        
        basic_filter_box = gtk.HBox()
        self.vbox.pack_start(basic_filter_box, False, False)
        
        queryframe = gtk.Frame('Query Parameters')
        queryframe.set_border_width(2)
        
        filterframe = gtk.Frame('Basic Filter')
        filterframe.set_border_width(2)
                
        basic_filter_box.pack_start(queryframe, False, False)
        basic_filter_box.pack_start(filterframe, True, True)
        
        #query parameters, empty and full
        querybox = gtk.VBox()
        querybox.set_border_width(5)
                
        self.checkbox_showfull = gtk.CheckButton('show full')
        self.checkbox_showfull.show()
        self.checkbox_showempty = gtk.CheckButton('show empty')
        self.checkbox_showempty.show()
                
        #filterframe content
        
        filtertable = gtk.Table(2,5)
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
        
        map_label = gtk.Label('Mapname contains:')
        server_label = gtk.Label('Servername contains:')
        
        self.mapnameentry = gtk.Entry()
        self.servernameentry = gtk.Entry()
             
        filtertable.attach(self.checkbox_hide_non_responsive, 0,1,0,1 )
        filtertable.attach(self.checkbox_hide_passworded, 0,1,1,2 )
        filtertable.attach(minplayerlabel, 1,2,0,1 )
        filtertable.attach(maxplayerlabel, 1,2,1,2 )
        filtertable.attach(self.minplayerentry, 2,3,0,1 )
        filtertable.attach(self.maxplayerentry, 2,3,1,2 )
        filtertable.attach(map_label, 3,4,0,1)
        filtertable.attach(self.mapnameentry, 4,5,0,1)
        filtertable.attach(server_label, 3,4,1,2)
        filtertable.attach(self.servernameentry, 4,5,1,2)
        
        
        querybox.pack_start(self.checkbox_showfull)
        querybox.pack_start(self.checkbox_showempty)
        queryframe.add(querybox)
        
        
        self.gametypesfilter = GametypesFilter()
        self.vbox.pack_start(self.gametypesfilter, False, False)
        
        self.create_gear_chooser()
        self.create_cvar_filter()
        
    def create_gear_chooser(self):
        """
        Creates the ui elements to choose a g_gear configuration
        """
        
        gear_frame = gtk.Frame('Gear Settings Filter')
        
        
        
        gear_type_box = gtk.HBox()
        #the include exclude chooser
        self.radio_gear_disable = gtk.RadioButton(None, 'Disabled')
        self.radio_gear_include = gtk.RadioButton(self.radio_gear_disable, \
                                                                      'Include')
        self.radio_gear_exclude = gtk.RadioButton(self.radio_gear_disable, \
                                                                      'Exclude')
        gear_type_box.pack_start(self.radio_gear_disable)
        gear_type_box.pack_start(self.radio_gear_include)
        gear_type_box.pack_start(self.radio_gear_exclude)
        gear_type_box.set_border_width(5)
        
        
        
        gearhbox = gtk.HBox()
        
        gear_frame.add(gearhbox)
        
        gear_choose_area_vbox = gtk.VBox()
        
        
       
        
        gear_table = gtk.Table(4,2)
        gear_table.set_border_width(15)
        gearhbox.pack_start(gear_choose_area_vbox)
        gear_choose_area_vbox.pack_start(gear_type_box)
       
        gear_choose_area_vbox.pack_start(gear_table)
        
        #the checkboxes
        self.checkbox_grenades = gtk.CheckButton('Grenades')
        self.checkbox_snipers = gtk.CheckButton('Snipers')
        self.checkbox_spas = gtk.CheckButton('Spas')
        self.checkbox_pistols = gtk.CheckButton('Pistols')
        self.checkbox_automatics = gtk.CheckButton('Automatic Guns')
        self.checkbox_negev = gtk.CheckButton('Negev')
        
        #the value textfield
        self.gearvalue = gtk.Entry()
        self.gearvalue.set_width_chars(4)
        
        #the add button
        add_button = gtk.Button('Add')
        add_button.set_border_width(5)
        
        #now put all into the table
        gear_table.attach(self.checkbox_grenades, 0,1,0,1 )
        gear_table.attach(self.checkbox_snipers, 0,1,1,2 )
        gear_table.attach(self.checkbox_spas, 0,1,2,3 )
        gear_table.attach(self.gearvalue, 0,1,3,4 )
        
        gear_table.attach(self.checkbox_pistols, 1,2,0,1 )
        gear_table.attach(self.checkbox_automatics, 1,2,1,2 )
        gear_table.attach(self.checkbox_negev, 1,2,2,3 )
        gear_table.attach(add_button, 1,2,3,4 )
        
        #gear settings treeview area
        gear_values_vbox = gtk.VBox()
        gearhbox.pack_start(gear_values_vbox)
        gear_scrolled_window = gtk.ScrolledWindow()
        gear_scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        gear_values_vbox.pack_start(gear_scrolled_window)
        
        self.gearliststore = gtk.ListStore(str)
        gear_set_treeview = gtk.TreeView(model=self.gearliststore)
        gear_scrolled_window.add(gear_set_treeview)
                
        self.column_gear_value = gtk.TreeViewColumn("Gear Value")
                
        gear_set_treeview.append_column(self.column_gear_value)
        
        var_cell0=gtk.CellRendererText()
        
        self.column_gear_value.pack_start(var_cell0, expand=True)
        self.column_gear_value.add_attribute(var_cell0, 'text', 0)
        self.column_gear_value.set_reorderable(True)
          
        
        remove_button = gtk.Button('Remove Selected')
        remove_button.set_border_width(5)
        gear_values_vbox.pack_start(remove_button, False, False)
        
        self.vbox.pack_start(gear_frame, False, False)
        
        
    def create_cvar_filter(self):
        """
        Creates the ui-elements for the custom server cvars filtering
        """
        
        cvar_frame = gtk.Frame('Custom Sever CVARS Filtering')
        
        cvar_main_hbox = gtk.HBox()
        cvar_frame.add(cvar_main_hbox)
        
        
        #settings editing area
        cvar_set_vbox = gtk.VBox()
        cvar_main_hbox.pack_start(cvar_set_vbox)
        
        
        variable_label = gtk.Label('Variable:')
        value_label = gtk.Label('Value:')
        
        self.variable_entry = gtk.Entry()
        self.value_entry = gtk.Entry()
        
        editing_table = gtk.Table(5,2)
        editing_table.attach(variable_label, 0,1,0,1)
        editing_table.attach(self.variable_entry,1,2,0,1)
        editing_table.attach(value_label, 0,1,1,2)
        editing_table.attach(self.value_entry, 1,2,1,2)
        editing_table.set_border_width(10)
        cvar_set_vbox.pack_start(editing_table)
        
       
        self.radio_cvar_include = gtk.RadioButton(None, 'Include')
        self.radio_cvar_include.set_border_width(5)
        self.radio_cvar_exclude = gtk.RadioButton(self.radio_cvar_include, \
                                                                      'Exclude')
        self.radio_cvar_exclude.set_border_width(5)
       
        editing_table.attach(self.radio_cvar_include, 1,2,2,3)
        editing_table.attach(self.radio_cvar_exclude, 1,2,3,4)
        
        add_button = gtk.Button('Add')
        editing_table.attach(add_button, 1,2,4,5)
        
        
        #the treeview displaying current CVAR filter settings
        cvar_values_vbox = gtk.VBox()
        cvar_main_hbox.pack_start(cvar_values_vbox)
        cvar_scrolled_window = gtk.ScrolledWindow()
        cvar_scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        cvar_values_vbox.pack_start(cvar_scrolled_window)
        
        self.cvarliststore = gtk.ListStore(str, str)
        cvar_set_treeview = gtk.TreeView(model=self.gearliststore)
        cvar_scrolled_window.add(cvar_set_treeview)
                
        self.column_cvar_variable = gtk.TreeViewColumn('Variable')
        self.column_cvar_value = gtk.TreeViewColumn('Value')
        
        cvar_set_treeview.append_column(self.column_cvar_variable)
        cvar_set_treeview.append_column(self.column_cvar_value)
        
        var_cell0=gtk.CellRendererText()
        var_cell1=gtk.CellRendererText()
        
        
        self.column_cvar_variable.pack_start(var_cell0, expand=True)
        self.column_cvar_value.pack_start(var_cell1, expand=False)
        
        self.column_cvar_variable.add_attribute(var_cell0, 'text', 0)
        self.column_cvar_value.add_attribute(var_cell1, 'text', 1)  
                  
        
        remove_button = gtk.Button('Remove Selected')
        remove_button.set_border_width(5)
        cvar_values_vbox.pack_start(remove_button, False, False)
        
        self.vbox.pack_start(cvar_frame, False, False)
      
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
            self.gametypesfilter.checkbox_show_gametype_all.set_active(True)
            # emits the 'toggled' signal
            self.gametypesfilter.checkbox_show_gametype_all.toggled() 
            
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
            self.gametypesfilter.checkbox_show_gametype_all.set_active(True)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_BOMB])
            self.gametypesfilter.checkbox_show_gametype_bomb.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_TS])
            self.gametypesfilter.checkbox_show_gametype_survivor.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_CTF])
            self.gametypesfilter.checkbox_show_gametype_ctf.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_TDM])
            self.gametypesfilter.checkbox_show_gametype_tdm.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_CAH])
            self.gametypesfilter.checkbox_show_gametype_cah.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_FTL])
            self.gametypesfilter.checkbox_show_gametype_ftl.set_active(value)
            
            value = fm.value_as_boolean(stored_filter[filterkey.GT_FFA])
            self.gametypesfilter.checkbox_show_gametype_ffa.set_active(value)
            
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
        value = fm.value_from_boolean(self.gametypesfilter.\
                                        checkbox_show_gametype_all.get_active())
        filter[filterkey.GT_ALL] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                       checkbox_show_gametype_bomb.get_active())
        filter[filterkey.GT_BOMB] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                   checkbox_show_gametype_survivor.get_active())
        filter[filterkey.GT_TS] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                        checkbox_show_gametype_ctf.get_active())
        filter[filterkey.GT_CTF] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                        checkbox_show_gametype_tdm.get_active())
        filter[filterkey.GT_TDM] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                        checkbox_show_gametype_cah.get_active())
        filter[filterkey.GT_CAH] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
                                        checkbox_show_gametype_ftl.get_active())
        filter[filterkey.GT_FTL] = value
        
        value = fm.value_from_boolean(self.gametypesfilter.\
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
        
        #mapname and servername filter
        filter[filterkey.FLT_MAP_NAME] = self.mapnameentry.get_text()
        filter[filterkey.FLT_SERVER_NAME] = self.servernameentry.get_text()        
        
        #query params
        value = fm.value_from_boolean(self.checkbox_showfull.get_active())
        filter[filterkey.QRY_SHOW_FULL] = value
        
        value = fm.value_from_boolean(self.checkbox_showempty.get_active())
        filter[filterkey.QRY_SHOW_EMPTY] = value
        
        
        #write to file
        t = Thread(target=fm.save_filter_to_remember)
        t.setDaemon(True)
        t.start()
        

        
    def on_apply_clicked(self, widget):
            """
            Callback of the Apply button
            """
            self.save_filter()
            
            self.destroy()
            
            
    def on_cancel_clicked(self, widger):
            """
            Callback of the Cancel button
            """
            #do nothing just close the dialog
            
            self.destroy()
        
            
        