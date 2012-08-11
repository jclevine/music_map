import unittest
import music_map_db
import os
import test_utils


class TestMusicMap(unittest.TestCase):

    def setUp(self):
        music_map_db.create_dbs(test_utils.TEST_DB_LOC)

    def tearDown(self):
        os.remove('unknown_error.log')
        os.remove('unparseable.log')
        os.remove('music_map.log')
        os.remove(test_utils.TEST_DB_LOC)

    def test_simple(self):
        db_data = test_utils.insert_playlist_into_music_map('test_simple_playlist.m3u8')
        rows = db_data['rows']
        try:
            for row in rows:
                self.assertEqual('theartist', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['cursor'].close()
            db_data['conn'].close()

    def test_underscore_in_artist_name(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscores.m3u8')
        rows = db_data['rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['cursor'].close()
            db_data['conn'].close()


    def test_underscore_in_artist_name_but_not_in_song(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscore_but_not_song.m3u8')
        rows = db_data['rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['cursor'].close()
            db_data['conn'].close()


    def test_no_underscore_in_artist_name_but_in_song(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscore_but_not_song.m3u8')
        rows = db_data['rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['cursor'].close()
            db_data['conn'].close()


    def test_nonexistent_playlist(self):
        self.assertRaises(SystemExit, test_utils.insert_playlist_into_music_map, 'nonexistent.m3u8')


    def test_unparseable_playlist(self):
        db_data = test_utils.insert_playlist_into_music_map('unparseable.m3u8')
        try:
            with open('unparseable.log', 'r') as log:
                unparseable_song = log.readline().strip()
                self.assertEqual('./Ben_Folds/TheAlbum/not track_Ben_Folds_The Track Title.mp3', unparseable_song)
        finally:
            db_data['cursor'].close()
            db_data['conn'].close()

if __name__ == "__main__":
    unittest.main()
