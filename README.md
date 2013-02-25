Intro
=====

Export myepisodes.com data into trakt.tv

Currently supports:
 - Moving all watched episodes to trakt.tv
 - Adding all series to the trakt.tv watchlist

Does not currently support:
 - Marking items as collected
 - - _Not sure which trakt API call to make_
 - Custom mapping of seasons to tvdb IDs
 - - _as some cannot be found on tvdb by name, or get the wrong version (e.g. Once Upon a Time 1973 vs 2011)_
 - Locally caching data
 - - _so we dont have to recheck completed seasons, refetch tvdb ID mappings etc_


Requires
=========
 - tvdb_api
 - - `easy_install tvdb_api`
 - BeautifulSoup
 - - `pip install beautifulsoup`
