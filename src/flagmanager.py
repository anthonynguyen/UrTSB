'''
Created on 08.08.2010

@author: sorcerer
'''
from globals import Globals
import gtk
import sys

class FlagManager(object):
    """
    Handles loading of imageicon
    """

    __shared_state = {} # borg pattern
    
    instance = None

    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__shared_state # borg pattern
        
        if not self.instance:
            self.instance = True
            
            self.flags = {}
            
            img = gtk.Image()
            self.blank = img.get_pixbuf()
            
    def get_flag(self, country):
        """
        Gets a Pixbuf instance of the flagicon for the passed country.
        If there is already one image with the country code as key in the 
        dict. return this instance, otherwise create a new PixBuf instance.
        
        @param country - country code
        @return flag icon PicBuf instance
        """
        if country in self.flags:
            return self.flags[country]
        else:
            try:
                flag_img = gtk.Image()
                imagename = country.lower() + '.png'
                flag_img.set_from_file(Globals.scriptdir + '/../flags/' + imagename)
                flag_pixbuf = flag_img.get_pixbuf()
                self.flags[country] = flag_pixbuf 
                return flag_pixbuf
            except:
                self.flags[country] = self.blank
                return self.blank
                
            
        