
from distutils.core import setup
from urtsb_src.globals import Globals
import glob
import sys
try:
    import py2exe
    #used to build windows executable
except:
    pass

cfg = {
    'name':Globals.app_name,
    'version':Globals.app_ver,
    'description':Globals.app_desc,
    'author':'Sorcerer',
    'author_email':'sorcerersr@googlemail.com',
    'url':'http://code.google.com/p/urtsb/',
    'long_desc':'UrTSB is a Game Server Browser for the FPS Urban Terror'\
                                            +' ( http://www.urbanterror.info )',
    'license':'GPLv3'    
    }



try:
    cmd = sys.argv[1]
except IndexError:
    print 'Usage: setup.py sdist|build|install|py2exe|py2app...'
    raise SystemExit

files = ["resource/flags/*", "resource/icons/*", \
         "resource/geoip/GeoIP.dat", "resource/win_gtk/*"]

#py2exe (Windows) target 
#needs to be tested !
if cmd == 'py2exe':
    setup(name = cfg['name'],
          version = cfg['version'],
          description = cfg['description'],
          author = cfg['author'],
          author_email = cfg['author_email'],
          url = cfg['url'],
          long_description = cfg['long_desc'],
          license = cfg['license'],
          platforms = ["Windows"],
          windows = [
            {
                "script": "urtsb",
                "icon_resources": [(1, "urtsb_src/resource/icons/icon.ico")]
            }
          ],
          options = {
                'py2exe': {
                        'packages': ['encodings'],
                        'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
                        'unbuffered': True,
                        'optimize': 2
                          }
            },
          data_files = [ ('resource/flags', glob.glob('urtsb_src/resource/flags\\*.png')),
                          ('resource/icons', glob.glob('urtsb_src/resource/icons\\*.png')),
                          ('resource/geoip', ['urtsb_src/resource/geoip/GeoIP.dat']),
                          ('resource/win_gtk', ['urtsb_src/resource/win_gtk/gtkrc']),
                          ('lib/gtk-2.0/2.10.0/engines', ['urtsb_src/resource/win_gtk/libwimp.dll']),
                          ('lib/gtk-2.0/2.10.0/engines', ['urtsb_src/resource/win_gtk/libpixmap.dll']) ]
          )
#py2app (MacOS) target
elif cmd == 'py2app':
    print 'py2app is not yet supported !'
#everything else:
else:
    setup(name = cfg['name'],
          version = cfg['version'],
          description = cfg['description'],
          author = cfg['author'],
          author_email = cfg['author_email'],
          url = cfg['url'],
          packages = ['urtsb_src', 'urtsb_src/ui', 'urtsb_src/pygeoip'],
          package_data = {'urtsb_src' : files },
          scripts = ["urtsb"],
          long_description = cfg['long_desc'],
          license = cfg['license'],
          platforms = ["Linux", "Windows"]
    ) 