from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["resource/flags/*", "resource/icons/*", "resource/geoip/GeoIP.dat"]

setup(name = "urtsb",
    version = "0.4",
    description = "a Game Server Browser for the FPS Urban Terror",
    author = "Sorcerer",
    author_email = "sorcerersr@googlemail.com",
    url = "http://code.google.com/p/urtsb/",
    packages = ['UrTSB', 'UrTSB/ui', 'UrTSB/pygeoip'],
    package_data = {'UrTSB' : files },
    scripts = ["urtsb"],
    long_description = """UrTSB is a Game Server Browser for the FPS Urban Terror ( http://www.urbanterror.info""",
    license = "GPLv3",
    platforms = ["Linux", "Windows"]
) 