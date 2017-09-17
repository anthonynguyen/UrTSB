# UrTSB #
UrTSB is a Game Server Browser for the FPS Urban Terror ( [http://www.urbanterror.info](http://www.urbanterror.info) ) targeted to run on Linux and Windows (Mac users: if you manage to get Python 2.6 and PyGTK running UrTSB should also work on MacOS).

- - - - - - - - - - - - - - - -

### Features ###
 + server search (master server query)
 + filter results (including UrT specific gametypes)
 + display server details - players (with kills, ping) and server vars
 + manage favorites - add/remove servers to a favorites list
 + buddylist - manage a buddylist and search servers your buddies are playing on (note: the search is case sensitiv!). Supports substrings. For example if you add only the string [clantag] a buddysearch will return all servers where players with [clantag] in their name are playing. Good to see where your clanm8s are playing :)
 + of course launching Urban Terror with automatic connection to a selected server
 + view a list of servers you recently played on (if UrTSB was used to connect) including the date of last connection and number  of connections
 + RCON feature

Discussion thread on the official Urban Terror Forums about UrTSB: [http://forums.urbanterror.info/topic/22858-urtsb/](http://forums.urbanterror.info/topic/22858-urtsb/)

### Dependencies ###
+ Python 2.x
+ PyGTK

- - - - - - - - - - - - - - - -

## Changelog ##

### 0.1 ###
initial release

### 0.2 ###

 + major speed improvements of server status requests (makes server search up to two times faster than in v.0.1. Refresh of favorites and recent servers are faster, too)
 + new feature: buddylist. Search servers based on the names of players playing on them. (note: search is case sensitiv!) Manage (add/remove) your Buddies and look where they are playing.
 + serverlists are now sortable by clicking on the table headers
 + added option to set a default tab in the settings
 + fixed bug that prevented a server to be removed from the recent serverslist
 + progressbar issues fixed
 + password of servers can now be remembered. There now is also a checkbox in the password dialog that can enable/disable this function.
 + fixed a bug that causes servers to appear multiple times in the serverlist after multiple searches
 + a lock-icon is now displayed for passworded servers instead of the string 'yes'
 + the selected row in a serverlist is now updated too, if the refresh-button in the details area is clicked.
 + plus some minor bugfixes

### 0.2.1 ###

 + spelling of some labels
 + added 'Add to Favorites' button to the serverdetails area on the 'Buddies' tab

### 0.3 ###

 + added option to disable the update of the selected server row when refresh button is clicked
 + remember filter/query parameters
 + some "under the hood" code improvements
 + fixed a bug that prevented the lock-icon to be displayed on the "Recently Played" tab
 + added feature to display location of the server as a small flag icon
 + handle players with blank names as UnnamedPlayer
 + applied patch to make UrTSB work on windows (contributed by Courgette from the urbanterror.info forums)
 + server connect on double-click / enter pressed and F5 key refreshes serverdetails
 + playerlist and server var list are now sortable
 + now launching UrT in a subprocess (to avoid that UrTSB is blocked while UrT is running)
 + new feature: RCON window for remote server administration
 + added contextmenus to the serverlist and the playerlist

### 0.4 ###

 + applied patch to make UrTSB work on windows (contributed by Courgette from the urbanterror.info forums) + some more changes needed to provide a windows version of UrTSB
 + make use of python distutils (UrTSB can now be installed by calling "python setup.py install")
 + adding a server manually to the favorites now handles the host to be specified by url and not only by ip
 + added logo/icon
 + new filtering panel - advanced filter. The old basic filter panel remains the default. The new advanced filter panel can be activated in the settings. Features:
   - more filter options: g_gear (incl. g_gear calculator), custom variable filtering, servername and mapnamefilter.
   - Refresh of the Serverlist without new master server query
   - Direct server lookup by ip:port or url:port
 + added abort button to abort a query/search/refresh.
 + display servername on rcon window
 + two new context menuitems: "copy address to clipboard" and "copy name and address to clipboard"
 + added commandline option -d (or --debug) which activates debug output
 + added status icons to buddylist (online/offline)
 + removed update selected row on refresh
 + added option to start a buddysearch on startup if the buddytab is set as the default tab
 + window now remembers size and position

### 0.5 (in development) ###
 + display private slots (issue #1)
 + fixed server sorting by playercount ( issue #3 )
 + Works with Urban Terror 4.2 / 4.3
 + Version column
 + Password column is sortable
