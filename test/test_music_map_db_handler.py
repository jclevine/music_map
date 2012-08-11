import unittest
import mock
import sqlite3
import test_utils
from music_map_db_handler import MusicMapDBHandler
from song import Song
import os
import music_map_db


class Test(unittest.TestCase):

    def setUp(self):
        music_map_db.create_dbs(test_utils.TEST_DB_LOC)

    def tearDown(self):
        os.remove(test_utils.TEST_DB_LOC)

    @mock.patch('music_map_db_handler.MusicMapDBHandler._song_in_song_table', mock.Mock(return_value=False))
    def test_db_error_on_insert(self):
        conn = sqlite3.connect(test_utils.TEST_DB_LOC)
        db_handler = MusicMapDBHandler(conn.cursor())
        song = Song("./TheArtist/TheAlbum/31_TheArtist_The Track Title.mp3",
                    music_roots=['.'])
        conn.close()
        db_handler.insert_song(song)
        with open("unknown_error.log") as log:
            error = log.readline().strip()
            self.assertEquals('Error inserting song (theartist | thealbum | 31 | track title) into DB: Cannot operate on a closed database.',
                              error)

        test_utils.close_all_handlers('unknown_error')
        os.remove('unknown_error.log')

    @mock.patch('music_map_db_handler.MusicMapDBHandler._song_in_song_table', mock.Mock(return_value=True))
    def test_song_already_in_table_on_insert(self):
        conn = sqlite3.connect(test_utils.TEST_DB_LOC)
        db_handler = MusicMapDBHandler(conn.cursor())
        song = Song("./TheArtist/TheAlbum/31_TheArtist_The Track Title.mp3",
                    music_roots=['.'])
        db_handler.insert_song(song)
        with open("music_map.log") as log:
            error = log.readline().strip()
            self.assertEquals('Song already in DB: theartist | thealbum | 31 | track title',
                              error)

        test_utils.close_all_handlers('music_map')
        os.remove('music_map.log')
        conn.close()


if __name__ == "__main__":
    unittest.main()
