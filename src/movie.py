# -*- coding: utf-8 -*-

import json
import logging

import omdb

# set up logger
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('main')
logging.basicConfig(format=LOGGING_FORMAT,
                    level=logging.DEBUG)


class MissingMovieTitle(Exception):
    pass


class Movie(object):

    def __init__(self, imdb_id=None, title=None, poster=None, yt_url=''):
        if imdb_id is not None:
            self._imdb_id = imdb_id
            logger.debug('Fetching IMDB ID {id} ...'.format(id=self._imdb_id))
            res = omdb.request(i=self._imdb_id, r='json')
            content = json.loads(res.content.decode('utf-8'))
            self.title = "{title} ({year})".format(title=content['Title'],
                                                   year=content['Year'])
            self.poster_image_url = content['Poster']
        elif title is not None:
            self.title = title
            self.poster_image_url = poster
        else:  # no movie title
            raise MissingMovieTitle('movie must have a title')
        self.trailer_youtube_url = yt_url

    def __str__(self):
        return "<Movie: {title}>".format(title=self.title)
