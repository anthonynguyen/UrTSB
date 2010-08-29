#!/usr/bin/env python
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



from urtsb_src.globals import Globals
from urtsb_src.guicontroller import GuiController
from urtsb_src.log import Log
from urtsb_src.ui.window import Window
import getopt
import gobject
import gtk
import logging
import os
import sys
from urtsb_src.filemanager import FileManager

def try_gtk_imports():
    #gtk import stuff   
    try:
        import pygtk
        pygtk.require("2.0")
    except:
        pass
    try:
        import gtk
    except:
        print 'Import GTK libraries failed!'
        sys.exit(1)    

def determine_path ():
    """Borrowed from wxglade.py"""
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print "I'm sorry, but something is wrong."
        print "There is no __file__ variable. Please contact the author."
        sys.exit ()

def usage():
    """
    Prints out usage information
    Commandline parameters
    """
    print 'Available commandline options:'
    print '\t-h or --help\tthis helptext'
    print '\t-d or --debug\tactivating debug output'
      
        
def start ():
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "debug"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)    
        
    loglevel = logging.INFO
    
    for o, a in opts:
        if o in ("-d", "--debug"):
            loglevel = logging.DEBUG
        elif o in ("-h", "--help"):
            usage()
            sys.exit(1)
        else:
            assert False, "unhandled option"    
        
    try_gtk_imports()
   
   
    gobject.threads_init() # enable threads for gtk
    
    #init global definitions:
    Globals.initialize(determine_path())
    
    #init logging
    Log(loglevel)
    
    if sys.platform == 'win32':
        #apply gtk style for win32 (wimp theme)
        gtkrcpath = os.path.normpath(os.path.join(Globals.resource_dir, \
                                                               'win_gtk/gtkrc'))
        gtk.rc_parse(gtkrcpath)
    
    window = Window() # create the urtsb window
    guicontroller = GuiController() # initialize the gui controller
    guicontroller.setWindow(window)  
       
    gtk.main() # run the gtk main loop
    
    #on exit save the window size informations
    Log.log.info('Exiting....')
    fm = FileManager()
    Log.log.debug('Saving window size informations')
    fm.save_window_sizing()
    
if __name__ == "__main__":
    start()

