# -*- coding: utf-8 -*-

import os
import json

from movie import Movie
from fresh_tomatoes import open_movies_page


ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATA_FOLDERPATH = os.path.join(ROOT, 'data')
DATA_FILEPATH = os.path.join(DATA_FOLDERPATH, 'moviedata.json')


def toMovie(movie):
    return Movie(
        imdb_id=movie['imdb_id'],
        title="{title} ({year})".format(title=movie['title'],
                                        year=movie['year']),
        yt_url=movie['youtube_trailer_url']
    )


def main():
    movies_data = json.loads(open(DATA_FILEPATH, 'rt').read())
    movies = map(toMovie, movies_data)
    open_movies_page(movies)

if __name__ == '__main__':
    main()
