import unittest
import music_map_db
import os
import shutil
from music_map import MusicMap


class Test(unittest.TestCase):


    def setUp(self):
        music_map_db.create_dbs()


    def tearDown(self):
        shutil.rmtree(r'c:\_src\music_map\test\__pycache__')
        os.remove('music_map.log')
        os.remove('unknown_error.log')
        os.remove('unparseable.log')
        os.remove('music_map.sqlite')

    def test(self):
        params = {'playlist_loc': os.path.abspath(r'c:\_src\music_map\test\data\test_simple_playlist.m3u8'),
                  'music_roots': ['.'],
                  'db_loc': os.path.abspath(r'c:\_src\music_map\test\music_map.sqlite'),
                  'debug': False}
        MusicMap(params)
        pass


if __name__ == "__main__":
    unittest.main()