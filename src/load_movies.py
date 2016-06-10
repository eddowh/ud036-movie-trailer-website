# -*- coding: utf-8 -*-

import os
import json

from movie import Movie
from fresh_tomatoes import open_movies_page


ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATA_FOLDERPATH = os.path.join(ROOT, 'data')
DATA_FILEPATH = os.path.join(DATA_FOLDERPATH, 'moviedata.json')


def main():
    movies_data = json.loads(open(DATA_FILEPATH, 'rt').read())
    movies = map(lambda m: Movie(imdb_id=m['imdb_id'],
                                 yt_url=m['youtube_trailer_url']),
                 movies_data)
    open_movies_page(movies)

if __name__ == '__main__':
    main()
