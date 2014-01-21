#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import cookielib
import re
import urllib, urllib2, urlparse

MYEPISODE_URL = "http://www.myepisodes.com"


class MyEpisodes(object):

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password
        self.shows = []
        self.show_list = []

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', 'Lynx/2.8.1pre.9 libwww-FM/2.14')
        ]

    def send_req(self, url, data=None):
        try:
            response = self.opener.open(url, data)
            return ''.join(response.readlines())
        except:
            return None

    def login(self):
        login_data = urllib.urlencode({
            'username': self.userid,
            'password': self.password,
            'action': "Login",
            })
        login_url = "%s/%s" % (MYEPISODE_URL, "login.php")
        data = self.send_req(login_url, login_data)
        # Quickly check if it seems we are logged on.
        if (data is None) or (self.userid not in data):
            return False

        return True

    def get_show_list(self):
        # Populate shows with the list of show_ids in our account
        wasted_url = "%s/%s" % (MYEPISODE_URL, "life_wasted.php")
        data = self.send_req(wasted_url)
        if data is None:
            return False
        soup = BeautifulSoup(data)
        mylist = soup.find("table", {"class": "mylist"})
        mylist_tr = mylist.findAll("tr")[1:-1]
        for row in mylist_tr:
            link = row.find('a', {'href': True})
            showid = urlparse.parse_qs(link.get('href'))['showid'][0]
            self.shows.append(int(showid))
            self.show_list.append({'id': int(showid), 'name': link.string})
        return True

    def get_show_data(self, show_id):
        # Try to add the show to your account.
        url = "%s/views.php?type=epsbyshow&showid=%d" % (MYEPISODE_URL, show_id)
        data = self.send_req(url)
        if data is None:
            return False
        soup = BeautifulSoup(data)
        out = []
        mylist = soup.find("table", {"class": "mylist"})
        mylist_tr = mylist.findAll("tr", {"class": ["Episode_One", "Episode_Two"]})
        for row in mylist_tr:
            episode = row.find('td', {'class': "longnumber"})
            episode_data = episode.string.split('x')
            acquired = row.find('input', attrs={'type': "checkbox", "onclick": re.compile("MarkAcquired")})
            is_acquired = True if acquired.get('checked') else False
            viewed = row.find('input', attrs={'type': "checkbox", "onclick": re.compile("MarkViewed")})
            is_viewed = True if viewed.get('checked') else False
            out.append({'season': episode_data[0], 'episode': episode_data[1], 'acquired': is_acquired, 'viewed': is_viewed})
        return out

    def get_seen_episodes(self, show_id):
        data = self.get_show_data(show_id)
        out = [{'season': int(row['season']), 'episode': int(row['episode'])} for row in data if row['viewed']]
        return out

    def get_collection_episodes(self, show_id):
        data = self.get_show_data(show_id)
        out = [{'season': int(row['season']), 'episode': int(row['episode'])} for row in data if row['acquired']]
        return out
