from music_map import MusicMap
import os


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
    MusicMap(params)

