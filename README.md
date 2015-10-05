_Note: I am not supporting this as it was just a run-once script I put up if it is useful to others. Will accept pull requests though if it will help others_

Intro
=====
Export myepisodes.com data into trakt.tv

Currently supports:

 - Moving all watched episodes to trakt.tv
 - Adding all series to the trakt.tv watchlist

Does not currently support:

 - Custom mapping of seasons to tvdb IDs
  - _as some cannot be found on tvdb by name, or get the wrong version (e.g. Once Upon a Time 1973 vs 2011)_
 - Locally caching data
  - _so we dont have to recheck completed seasons, refetch tvdb ID mappings etc_


Requires
========
 - tvdb_api
  - `easy_install tvdb_api`
 - BeautifulSoup
  - `pip install beautifulsoup`


Usage
=====
 1. Check you have the requirements
 2. Go to http://trakt.tv/oauth/applications(http://trakt.tv/oauth/applications) and create a new application using urn:ietf:wg:oauth:2.0:oob as the redirect uri.
 3. Set the client id and client secret for the new application in myepisodes_export.ini
 4. Set your user name and password for myepisodes.com in myepisodes_export.ini
 5. Run `python ./run.py`
 6. Check the fails.txt afterwards to see, if some show could not be imported

_Note: If your season-episode string does not match 1x18 (e.g. if you have it set as s01e18 in
'Season & Episode numbering Format' in your MyEpisodes control panel) you may need to edit
`myepisodes.py` on line 80 (`episode_data = episode.string.split('x')`)._

Todo
====

The authentication method should be improved as each user shouldn't need to have to create their own application with trakt.tv.
The reason why it works like it does it to avoid having a public client secret.

Thanks
======

The myepisodes script is by maximeh from https://github.com/maximeh/script.myepisodes/
