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
              'music_roots': music_roots,
              'db_loc': db_loc,
              'debug': False}

    try:
        MusicMap(params)

        conn = sqlite3.connect(TEST_DB_LOC)
        song_cursor = conn.cursor()
        song_query = """
                SELECT artist_key
                     , album_key
                     , track_key
                     , title_key
                  FROM song
                """
        song_rs = song_cursor.execute(song_query)

        mm_cursor = conn.cursor()
        mm_query = """
                SELECT song_id
                     , location
                     , artist
                     , album
                     , track
                     , title
                     , full_path
                  FROM music_map
                  """
        mm_rs = mm_cursor.execute(mm_query)

        return {'conn': conn,
                'song_cursor': song_cursor,
                'song_rows':sqlite_utils.name_columns(song_rs),
                'mm_cursor': mm_cursor,
                'mm_rows': sqlite_utils.name_columns(mm_rs)}
    except IOError as ioe:
        song_cursor.close()
        mm_cursor.close()
        conn.close()
        raise ioe

def close_all_handlers(log_name):
    for handler in logging.getLogger(log_name).handlers:
        handler.close()
