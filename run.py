from myepisodes import MyEpisodes
from trakt import Trakt
from hashlib import sha1
import tvdb_api, urllib2, json, sys, time, ConfigParser, unicodedata

config = ConfigParser.ConfigParser()
config.read('myepisodes_export.ini')

tvdb = tvdb_api.Tvdb()

my_episodes = MyEpisodes(
        config.get('MyEpisodes', 'Username'),
        config.get('MyEpisodes', 'Password'))
login = my_episodes.login()
if(login == False):
    print "ERROR - Could not login to MyEpisodes"
    sys.exit(1)

my_episodes.get_show_list()


trakt = Trakt(
        config.get('Trakt', 'ClientId'),
        config.get('Trakt', 'ClientSecret'))

print "Requesting Trakt.tv authorization..."
print "To authorize access to you trakt.tv account access the following URL in a web browser and copy the authorization code:"
print trakt.get_authorize_url()
code = raw_input('Paste the authorization code here: ')
trakt.authorize(code)

for show in my_episodes.show_list:
    show['name'] = unicodedata.normalize('NFKD', show['name']).encode('ascii','ignore')
    print "\nProcessing: {}".format(show['name'])
    try:
        tvdb_data = tvdb[show['name']]

    except:
        f = open('fails.txt', 'a')
        f.write("%s\n" % show['name'])
        print "ERROR - Could not get TVDB ID for {}".format(show['name'])
        print "Skipping show: {}".format(show['name'])
        continue

    print '  Importing collection...'
    collection_data = my_episodes.get_collection_episodes(show["id"])
    collection_changes = trakt.add_to_collection(
            tvdb_data['seriesname'],
            tvdb_data['id'],
            collection_data)

    added = collection_changes['added']['episodes']
    updated = collection_changes['updated']['episodes']
    existing = collection_changes['existing']['episodes']
    if added > 0:
        print "    Added: {} episodes".format(added)
    if updated > 0:
        print "    Updated: {} episodes".format(updated)
    if existing > 0:
        print "    Existing: {} episodes".format(existing)
    if added == 0 and updated == 0 and existing == 0:
        print '    Show not found.'
    
    print '  Importing watched episodes...'
    watched_data = my_episodes.get_seen_episodes(show["id"])
    watched_changes = trakt.add_to_watched_history(
            tvdb_data['seriesname'],
            tvdb_data['id'],
            watched_data)

    added = watched_changes['added']['episodes']
    if added > 0:
        print "    Added: {} episodes".format(added) 
    else:
        print '    Show not found.'
    
    print '  Adding show to watch list...'
    watchlist_changes = trakt.add_to_watchlist(
            tvdb_data['seriesname'],
            tvdb_data['id'])

    added = watchlist_changes['added']['shows']
    existing = watchlist_changes['existing']['shows']
    not_found = watchlist_changes['not_found']['shows']
    if added > 0:
        print '    Added to watch list.'
    if existing > 0:
        print '    Show already on watch list.'
    if len(not_found) > 0:
       print '     Show not found.' 
#