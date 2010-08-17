from distutils.core import setup
import sys
try:
    import py2exe
    #used to build windows executable
except:
    pass

cfg = {
    'name':'urtsb',
    'version':'0.4',
    'description':'a Game Server Browser for the FPS Urban Terror',
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

files = ["resource/flags/*", "resource/icons/*", "resource/geoip/GeoIP.dat"]

#py2exe (Windows) target 
#needs to be tested !
if cmd == 'py2exe':
    setup(name = cfg['name'],
          version = cfg['version'],
          description = cfg['description'],
          author = cfg['author'],
          author_email = cfg['author_email'],
          url = cfg['url'],
          packages = ['UrTSB', 'UrTSB/ui', 'UrTSB/pygeoip'],
          package_data = {'UrTSB' : files },
          long_description = cfg['long_desc'],
          license = cfg['license'],
          platforms = ["Windows"],
          windows = ['urtsb'] 
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
          packages = ['UrTSB', 'UrTSB/ui', 'UrTSB/pygeoip'],
          package_data = {'UrTSB' : files },
          scripts = ["urtsb"],
          long_description = cfg['long_desc'],
          license = cfg['license'],
          platforms = ["Linux", "Windows"]
    ) 