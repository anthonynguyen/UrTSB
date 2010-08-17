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


from UrTSB.globals import Globals
from UrTSB.guicontroller import GuiController
from UrTSB.log import Log
from UrTSB.ui.window import Window
import gobject
import gtk
import logging
import os
import sys

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
       
        
def start ():
        
    try_gtk_imports()
    
    gobject.threads_init() # enable threads for gtk
    
    #init global definitions:
    Globals.initialize(determine_path())
    
    #init logging
    #change this line to 
    #logging = Log(logging.DEBUG)
    #to enable debug output
    Log(logging.INFO)
    
    
    window = Window() # create the urtsb window
    guicontroller = GuiController() # initialize the gui controller
    guicontroller.setWindow(window)  
       
    gtk.main() # run the gtk main loop
    
    
if __name__ == "__main__":
    start()


#
#
#if __name__ == '__main__':
#   
#   
#   
#    #gtk import stuff   
#    import sys
#    try:
#        import pygtk
#        pygtk.require("2.0")
#    except:
#        pass
#    try:
#        import gtk
#    except:
#        print 'Import GTK libraries failed!'
#        sys.exit(1)
#  
#    gobject.threads_init() # enable threads for gtk
#    
#    #init global definitions:
#    globals = Globals()
#    
#    #init logging
#    #change this line to 
#    #logging = Log(logging.DEBUG)
#    #to enable debug output
#    logging = Log(logging.INFO)
#    
#    
#    window = Window() # create the urtsb window
#    guicontroller = GuiController() # initialize the gui controller
#    guicontroller.setWindow(window)  
#       
#    gtk.main() # run the gtk main loop
#   
