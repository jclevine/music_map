from music_map import MusicMap
import os
import sqlite3
from util import sqlite_utils
import logging


TEST_PATH = os.path.abspath(r'c:\_src\music_map\test')
TEST_DB = 'music_map.sqlite'
TEST_DB_LOC = os.path.join(TEST_PATH, TEST_DB)


def insert_playlist_into_music_map(playlist_name,
                                   music_roots=['.']):
    db_loc = TEST_DB_LOC
    simple_playlist_loc = os.path.join(TEST_PATH, 'data', playlist_name)
    params = {'playlist_loc': simple_playlist_loc,
              'music_roots': ['.'],
              'db_loc': db_loc,
              'debug': False}

    try:
        MusicMap(params)

        conn = sqlite3.connect(TEST_DB_LOC)
        cursor = conn.cursor()
        query = """
                SELECT artist_key
                     , album_key
                     , track_key
                     , title_key
                  FROM song
                """
        rs = cursor.execute(query)
        return {'conn': conn,
                'cursor': cursor,
                'rows':sqlite_utils.name_columns(rs)}
    except IOError as ioe:
        conn.close()
        cursor.close()
        raise ioe

def close_all_handlers(log_name):
    for handler in logging.getLogger(log_name).handlers:
        handler.close()