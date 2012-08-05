import unittest
import music_map_db
import os
from music_map import MusicMap
import sqlite3
from util import sqlite_utils


class TestMusicMap(unittest.TestCase):


    def setUp(self):
        music_map_db.create_dbs()


    def tearDown(self):
        os.remove('unknown_error.log')
        os.remove('unparseable.log')
        os.remove('music_map.sqlite')
        os.remove('music_map.log')

    def test_simple(self):
        db_loc = os.path.abspath(r'c:\_src\music_map\test\music_map.sqlite')
        params = {'playlist_loc': os.path.abspath(r'c:\_src\music_map\test\data\test_simple_playlist.m3u8'),
                  'music_roots': ['.'],
                  'db_loc': db_loc,
                  'debug': False}
        MusicMap(params)

        conn = sqlite3.connect(db_loc)
        cursor = conn.cursor()
        query = """
                SELECT artist_key
                     , album_key
                     , track_key
                     , title_key
                  FROM song
                """
        rs = cursor.execute(query)
        rows = sqlite_utils.name_columns(rs)
        for row in rows:
            self.assertEqual('theartist', row['artist_key'])
            self.assertEqual('thealbum', row['album_key'])
            self.assertEqual('31', row['track_key'])
            self.assertEqual('track title', row['title_key'])
        cursor.close()

if __name__ == "__main__":
    unittest.main()
