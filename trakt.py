#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods to access the Trakt.tv API. 
See the complete API documentation at http://docs.trakt.apiary.io
"""

import json
import errno
import urllib2

class Trakt(object):
    BASE_URL = 'https://api-v2launch.trakt.tv'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_authorize_url(self):
        return "https://trakt.tv/oauth/authorize?response_type=code&client_id={}&redirect_uri=urn:ietf:wg:oauth:2.0:oob".format(self.client_id) 

    def authorize(self, code):
        self.code = code
        self._request_token()

    def add_to_collection(self, series_name, tvdb_id, collection_data):
        trakt_data = {
            'shows': [
                {
                    'title': series_name,
                    'ids': { 'tvdb': tvdb_id },
                    'seasons': collection_data
                }
            ]
        }
        return self._send_req('/sync/collection', trakt_data)

    def add_to_watched_history(self, series_name, tvdb_id, seen_data):
        trakt_data = {
            'shows': [
                {
                    'title': series_name,
                    'ids': { 'tvdb': tvdb_id },
                    'seasons': seen_data
                }
            ]
        }
        return self._send_req('/sync/history', trakt_data)

    def add_to_watchlist(self, series_name, tvdb_id):
        trakt_data = {
            'shows': [
                {
                    'title': series_name,
                    'ids': { 'tvdb': tvdb_id }
                }
            ]
        }
        return self._send_req('/sync/watchlist', trakt_data)

    def _send_req(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self._token,
            'trakt-api-version': '2',
            'trakt-api-key': self.client_id
        }
        req = urllib2.Request(self.BASE_URL + url, data=json.dumps(data), headers=headers)
        resp = self._urlopen_with_retry(req)
        return json.load(resp)

    def _request_token(self):
        values = {
                'code': self.code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
                'grant_type': 'authorization_code'
        }
        headers = {
            'Content-Type': 'application/json',
        }
        req = urllib2.Request(self.BASE_URL + '/oauth/token', data=json.dumps(values), headers=headers)
        resp = self._urlopen_with_retry(req)
        json_response = json.load(resp)
        self._token = json_response['access_token']

    def _urlopen_with_retry(self, req):
        timeout = 30
        for _ in range(5):
            try:
                return urllib2.urlopen(req, timeout=timeout)
                break
            except urllib2.URLError as err:
                timeout = timeout * 2
                print "Request timed out, retrying in {} seconds".format(timeout)
                continue
            else:
                raise err

        
