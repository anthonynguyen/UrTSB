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
import gtk


class AboutDialog(gtk.AboutDialog):
    """
    The About dialog of UrTSB
    """

    gplstring = '\n\
 UrTSB is free software: you can redistribute it and/or modify\n\
 it under the terms of the GNU General Public License as published by\n\
 the Free Software Foundation, either version 3 of the License, or\n\
 (at your option) any later version.\n\n\
 UrTSB is distributed in the hope that it will be useful,\n\
 but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
 GNU General Public License for more details.\n\n\
 You should have received a copy of the GNU General Public License\n\
 along with UrTSB.  If not, see <http://www.gnu.org/licenses/>.\n\
'

    def __init__(self):
        """
        Constructor
        """
        gtk.AboutDialog.__init__(self)
        
        gc = GuiController()
        self.set_name(gc.appname)
        self.set_program_name(gc.appname)
        self.set_version(gc.appver)
        self.set_comments(gc.appdesc)
        self.set_website('http://code.google.com/p/urtsb/')
        authors = ['Sorcerer (sorcerersr@googlemail.com)']
        self.set_authors(authors)
        self.set_copyright('(c) 2010')
        self.set_license(self.gplstring)
        
        logo_image = gtk.Image()
        logo_image.set_from_file(Globals.icon_dir+'/logo.png')
        self.set_logo(logo_image.get_pixbuf())
        