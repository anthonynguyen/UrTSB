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



from globals import Globals
from guicontroller import GuiController
from log import Log
from window import Window
import gobject
import logging
import os


if __name__ == '__main__':
   
   
   
    #gtk import stuff   
    import sys
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
  
    gobject.threads_init() # enable threads for gtk
    
    #init global definitions:
    globals = Globals()
    
    #init logging
    #change this line to 
    #logging = Log(logging.DEBUG)
    #to enable debug output
    logging = Log(logging.INFO)
    
    
    window = Window() # create the urtsb window
    guicontroller = GuiController() # initialize the gui controller
    guicontroller.setWindow(window)  
       
    gtk.main() # run the gtk main loop
   
