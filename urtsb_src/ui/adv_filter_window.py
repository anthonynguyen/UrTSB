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
from urtsb_src.filemanager import FileManager, filterkey, cfgvalues
from urtsb_src.globals import Globals
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
        self.set_icon_from_file(Globals.icon_dir +'/logo.png')
        self.set_default_size(700, 500)
        self.filter = filter
        #buttons
        applybutton = gtk.Button('Apply')
        cancelbutton = gtk.Button('Cancel')
        defaultbutton = gtk.Button('Defaults')
        resetbutton = gtk.Button('Reset')
        
        applybutton.connect("clicked", self.on_apply_clicked)
        cancelbutton.connect("clicked", self.on_cancel_clicked)
        defaultbutton.connect("clicked", self.on_default_clicked)
        resetbutton.connect("clicked", self.on_reset_clicked)
        
        self.action_area.pack_start(defaultbutton, False, False)
        self.action_area.pack_start(resetbutton, False, False)
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
                                                             'Include (equals)')
        self.radio_gear_exclude = gtk.RadioButton(self.radio_gear_disable, \
                                                         'Exclude (not equals)')
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
        
        #connect to the toggled signal
        self.checkbox_grenades.connect('toggled', self.on_gear_checkbox_changed)
        self.checkbox_snipers.connect('toggled', self.on_gear_checkbox_changed)
        self.checkbox_spas.connect('toggled', self.on_gear_checkbox_changed)
        self.checkbox_pistols.connect('toggled', self.on_gear_checkbox_changed)
        self.checkbox_automatics.connect('toggled', \
                                                  self.on_gear_checkbox_changed)
        self.checkbox_negev.connect('toggled', self.on_gear_checkbox_changed)
        
        #the value textfield
        self.gearvalue = gtk.Entry()
        self.gearvalue.set_width_chars(4)
        self.gearvalue.set_editable(False)
        
        #the add button
        add_button = gtk.Button('Add')
        add_button.set_border_width(5)
        add_button.connect('clicked', self.on_add_gear_value_clicked)
        
        
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
        self.gearlistview = gear_set_treeview
        gear_scrolled_window.add(gear_set_treeview)
                
        self.column_gear_value = gtk.TreeViewColumn("Gear Value")
                
        gear_set_treeview.append_column(self.column_gear_value)
        
        var_cell0=gtk.CellRendererText()
        
        self.column_gear_value.pack_start(var_cell0, expand=True)
        self.column_gear_value.add_attribute(var_cell0, 'text', 0)
        self.column_gear_value.set_reorderable(True)
          
        
        btn_hbox = gtk.HBox()  
        gear_values_vbox.pack_start(btn_hbox, False, False)
        
        clear_button = gtk.Button('Clear')
        clear_button.set_border_width(5)
        btn_hbox.pack_start(clear_button, True, True)
        clear_button.connect('clicked', self.on_clear_gear_list_clicked)
        
        remove_button = gtk.Button('Remove Selected')
        remove_button.set_border_width(5)
        btn_hbox.pack_start(remove_button, True, True)
        remove_button.connect('clicked', self.on_remove_selected_gear_value)
        
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
        
       
        self.radio_cvar_include = gtk.RadioButton(None, 'Include (equals)')
        self.radio_cvar_include.set_border_width(5)
        self.radio_cvar_exclude = gtk.RadioButton(self.radio_cvar_include, \
                                                         'Exclude (not equals)')
        self.radio_cvar_exclude.set_border_width(5)
       
        editing_table.attach(self.radio_cvar_include, 1,2,2,3)
        editing_table.attach(self.radio_cvar_exclude, 1,2,3,4)
        
        add_button = gtk.Button('Add')
        editing_table.attach(add_button, 1,2,4,5)
        add_button.connect('clicked', self.on_add_var_filter_clicked)
        
        #the treeview displaying current CVAR filter settings
        cvar_values_vbox = gtk.VBox()
        cvar_main_hbox.pack_start(cvar_values_vbox)
        cvar_scrolled_window = gtk.ScrolledWindow()
        cvar_scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        cvar_values_vbox.pack_start(cvar_scrolled_window)
        
        self.cvarliststore = gtk.ListStore(str, str, str, object)
        cvar_set_treeview = gtk.TreeView(model=self.cvarliststore)
        self.varfilterview = cvar_set_treeview
        cvar_scrolled_window.add(cvar_set_treeview)
                
        self.column_cvar_variable = gtk.TreeViewColumn('Variable')
        self.column_cvar_value = gtk.TreeViewColumn('Value')
        self.column_cvar_type = gtk.TreeViewColumn('Type')
        
        cvar_set_treeview.append_column(self.column_cvar_variable)
        cvar_set_treeview.append_column(self.column_cvar_value)
        cvar_set_treeview.append_column(self.column_cvar_type)
        
        var_cell0=gtk.CellRendererText()
        var_cell1=gtk.CellRendererText()
        var_cell2=gtk.CellRendererText()
              
        self.column_cvar_variable.pack_start(var_cell0, expand=True)
        self.column_cvar_value.pack_start(var_cell1, expand=False)
        self.column_cvar_type.pack_start(var_cell2, expand=False)
        
        self.column_cvar_variable.add_attribute(var_cell0, 'text', 0)
        self.column_cvar_value.add_attribute(var_cell1, 'text', 1)  
        self.column_cvar_type.add_attribute(var_cell2, 'text', 2)
                  
        
        btn_hbox = gtk.HBox()
        cvar_values_vbox.pack_start(btn_hbox, False, False)
        
        clear_button = gtk.Button('Clear')
        clear_button.set_border_width(5)
        btn_hbox.pack_start(clear_button, True, True)
        clear_button.connect('clicked', self.on_clear_var_list_clicked)
        
        remove_button = gtk.Button('Remove Selected')
        remove_button.set_border_width(5)
        btn_hbox.pack_start(remove_button, True, True)
        remove_button.connect('clicked', self.on_remove_selected_var)
        
        self.vbox.pack_start(cvar_frame, False, False)
      
    def calculate_gear_value(self):
        """
        Calculates the g_gear value
        """
        
        retval = 63
        if self.checkbox_grenades.get_active():
            retval -= 1
        if self.checkbox_snipers.get_active():
            retval -= 2
        if self.checkbox_spas.get_active():
            retval -= 4
        if self.checkbox_pistols.get_active():
            retval -= 8
        if self.checkbox_automatics.get_active():
            retval -= 16
        if self.checkbox_negev.get_active():
            retval -= 32
        
        return retval
      
      
    def set_default_values(self, reset):
        """
        Set default values to all input elements of the filter.
        Differs between application defaults and the values that are stored
        in a file to remember user choices.
        
        @param reset - boolean: if True use application defaults, otherwise load
                       values from file. 
       
        """
        
        self.gearliststore.clear()
        self.cvarliststore.clear()
        
        fm = FileManager()
        stored_filter = fm.get_remembered_filter_parameters()
        
        #gearcheckbox is not stored, only the listview
        #initialize with all checked
        self.checkbox_grenades.set_active(True)
        self.checkbox_snipers.set_active(True)
        self.checkbox_spas.set_active(True)
        self.checkbox_pistols.set_active(True)
        self.checkbox_automatics.set_active(True)
        self.checkbox_negev.set_active(True)
        
        
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
            
            self.mapnameentry.set_text('')
            self.servernameentry.set_text('')
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
            
            if filterkey.FLT_MAP_NAME in stored_filter:
                self.mapnameentry.set_text(stored_filter[filterkey.\
                                                                  FLT_MAP_NAME])
            if filterkey.FLT_SERVER_NAME in stored_filter:
                self.servernameentry.set_text(stored_filter[filterkey.\
                                                               FLT_SERVER_NAME])
            
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
            
            #the gearvalue list
            if filterkey.FLT_GEAR in stored_filter:
                value = stored_filter[filterkey.FLT_GEAR]
                if cfgvalues.DISABLED == value:
                    self.radio_gear_disable.set_active(True)
                    self.radio_gear_exclude.set_active(False)
                    self.radio_gear_include.set_active(False)
                elif cfgvalues.INCLUDE == value:
                    self.radio_gear_disable.set_active(False)
                    self.radio_gear_exclude.set_active(False)
                    self.radio_gear_include.set_active(True)
                elif cfgvalues.EXCLUDE == value:
                    self.radio_gear_disable.set_active(False)
                    self.radio_gear_exclude.set_active(True)
                    self.radio_gear_include.set_active(False)
            
            if filterkey.FLT_GEAR_LIST in stored_filter:
                for value in stored_filter[filterkey.FLT_GEAR_LIST]:
                    self.gearliststore.append([value])
                    
            if filterkey.FLT_VAR_LIST in stored_filter:
                for value in stored_filter[filterkey.FLT_VAR_LIST]:
                    self.cvarliststore.append([value[0], value[1], \
                                               value[2], value])
            
        
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
        
        if self.radio_gear_disable.get_active():
            filter[filterkey.FLT_GEAR] = cfgvalues.DISABLED
        elif self.radio_gear_include.get_active():
            filter[filterkey.FLT_GEAR] = cfgvalues.INCLUDE
        elif self.radio_gear_exclude.get_active():
            filter[filterkey.FLT_GEAR] = cfgvalues.EXCLUDE
        
        #iterate over gearliststore to create a list of geavalues 
        iter = self.gearliststore.iter_children(None)
        gearvalues = [] #empty list
        while iter:
            value = self.gearliststore.get_value(iter, 0)
            gearvalues.append(value)
            iter = self.gearliststore.iter_next(iter)
        filter[filterkey.FLT_GEAR_LIST] = gearvalues
               
        #iterate over varliststore to create the list of filter vars
        iter = self.cvarliststore.iter_children(None)
        varlist = []
        while iter:
            varfilter = self.cvarliststore.get_value(iter, 3)
            varlist.append(varfilter)
            iter = self.cvarliststore.iter_next(iter)
        filter[filterkey.FLT_VAR_LIST] = varlist
        
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
            
            
    def on_cancel_clicked(self, widget):
            """
            Callback of the Cancel button
            """
            #do nothing just close the dialog
            
            self.destroy()
        
    def on_reset_clicked(self, widget):
        """
        Callback of the reset button
        Reset the filter to the last applied values
        """
        self.set_default_values(False)
    
    def on_add_gear_value_clicked(self, widget):
        """
        Callback of the add button in the gear selection filter area
        Adds the current gear value to the gear value list
        """
        gearvalue = self.gearvalue.get_text()
        self.gearliststore.append([gearvalue])
        
    def on_clear_gear_list_clicked(self, widget):
        """
        Callback of the clear gear list button
        clears the treeview
        """
        self.gearliststore.clear()
        
    def on_clear_var_list_clicked(self, button):
        """
        Callback of the clear varlist button
        clears the treeview/liststore
        """
        self.cvarliststore.clear()
        
    def on_default_clicked(self, widget):
        """
        Callback of the defaults button
        Reset the filter to the default values (not the stored/last applied 
        values)
        """
        self.set_default_values(True)
        
    def on_gear_checkbox_changed(self, checkbox):
        """
        Callback for the toggled signal of the gear (weapons) checkboxes
        triggers the calculation of the g_gear value and sets it to the
        text entry
        """
        g_gear_value = self.calculate_gear_value()
        self.gearvalue.set_text(str(g_gear_value))
        
    def on_remove_selected_gear_value(self, button):
        """
        Callback of the remove selected button of the gear value treeview list
        """
        selection = self.gearlistview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            self.gearliststore.remove(iter)
            
    def on_remove_selected_var(self, button):
        """
        Callback of the remoce selected button of the custom filtering area
        """
        selection = self.varfilterview.get_selection()
        result = selection.get_selected()
        if result: 
            iter = result[1]
            self.cvarliststore.remove(iter)
            
    def on_add_var_filter_clicked(self, button):
        """
        Callback of the add button in the custom variable filtering area
        """
        varname = self.variable_entry.get_text()
        varvalue = self.value_entry.get_text()
        #both values not None and larger than 0
        if not None == varname and not len(varname) == 0 and not None\
                                         == varvalue and not len(varvalue) == 0:
            var = [None]*3
            var[0] = varname
            var[1] = varvalue
            if self.radio_cvar_include.get_active():
                var[2] = cfgvalues.INCLUDE
            elif self.radio_cvar_exclude.get_active():
                var[2] = cfgvalues.EXCLUDE
            
            self.cvarliststore.append([var[0], var[1], var[2], var])