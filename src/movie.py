# -*- coding: utf-8 -*-

from requests.exceptions import HTTPError
import json
import logging
import os

import omdb

# file paths
ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
CACHE = os.path.join(ROOT, 'cache')
if not os.path.exists(CACHE):
    os.mkdir(CACHE)

# set up logger
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('main')
logging.basicConfig(format=LOGGING_FORMAT,
                    level=logging.DEBUG)


class MissingMovieTitle(Exception):
    pass


class Movie(object):

    def __init__(self, imdb_id=None, title=None, poster=None, yt_url=''):
        if title is not None:
            self.title = title
            self.poster_image_url = poster
        else:  # no movie title
            raise MissingMovieTitle('movie must have a title')
        # fetch omdb, override only if it works
        if imdb_id is not None:
            self._imdb_id = imdb_id
            self._cache_fpath = os.path.join(CACHE, self._imdb_id + '.json')
            self.retrieve()
        self.trailer_youtube_url = yt_url

    def __str__(self):
        return "<Movie: {title}>".format(title=self.title)

    def retrieve(self):
        if os.path.exists(self._cache_fpath):
            logger.debug('Getting cached data of IMDB ID {id} ...'
                         .format(id=self._imdb_id))
            content = self._get_cache()
            self._set_from_omdb(content)
        else:
            self._fetch_omdb()

    def _get_cache(self):
        if self._imdb_id:
            return json.loads(open(self._cache_fpath, "rt").read())

    def _set_from_omdb(self, content):
        self.title = "{title} ({year})".format(title=content['Title'],
                                               year=content['Year'])
        self.poster_image_url = content['Poster']

    def _fetch_omdb(self):
        try:
            logger.debug('Fetching IMDB ID {id} ...'.format(id=self._imdb_id))
            res = omdb.request(i=self._imdb_id, r='json')
            raw_json = res.content.decode('utf-8')
            content = json.loads(raw_json)
            self._set_from_omdb(content)
        except (HTTPError, KeyError):
            pass
        else:  # save to cache
            with open(self._cache_fpath, "wt") as fd:
                fd.write(raw_json)
