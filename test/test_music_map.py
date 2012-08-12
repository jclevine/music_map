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
        rows = db_data['song_rows']
        try:
            for row in rows:
                self.assertEqual('theartist', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()

    def test_underscore_in_artist_name(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscores.m3u8')
        rows = db_data['song_rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()


    def test_underscore_in_artist_name_but_not_in_song(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscore_but_not_song.m3u8')
        rows = db_data['song_rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()


    def test_no_underscore_in_artist_name_but_in_song(self):
        db_data = test_utils.insert_playlist_into_music_map('test_artist_has_underscore_but_not_song.m3u8')
        rows = db_data['song_rows']
        try:
            for row in rows:
                self.assertEqual('ben folds', row['artist_key'])
                self.assertEqual('thealbum', row['album_key'])
                self.assertEqual('31', row['track_key'])
                self.assertEqual('track title', row['title_key'])
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
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
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()

    def test_2_types_of_roots(self):
        db_data = test_utils.insert_playlist_into_music_map('two_roots.m3u8',
                                                            music_roots=['.', './_Done_'])

        christian_death_row = {'track_key': '01',
                               'artist_key': 'christian death',
                               'album_key': 'jesus points bones at you',
                               'title_key': 'believers of unpure'}

        beastie_boys_row = {'track_key': '15',
                            'artist_key': 'beastie boys',
                            'album_key': "paul's boutique",
                            'title_key': 'b boy bouillabaisse'}
        expected_rows = [christian_death_row,
                         beastie_boys_row]
        num_expected = len(expected_rows)

        actual_rows = db_data['song_rows']
        try:
            self.assertEquals(len(expected_rows), len(actual_rows))

            # TODO: !2 Move this into a util function.
            # Go through all the actual rows and make sure it's in the
            # list of expected rows. If you find it, remove it from
            # the list of expected rows. If you have all the expected rows
            # by the end you will have no elements in the expected rows list.
            # Also, we make sure that the number of times we got a correct row
            # is the same as the original length of the expected rows list.
            num_rows_correct = 0
            for actual_row in actual_rows:
                for i, expected_row in enumerate(expected_rows):
                    if (expected_row['track_key'] == actual_row['track_key'] and
                        expected_row['artist_key'] == actual_row['artist_key'] and
                        expected_row['album_key'] == actual_row['album_key'] and
                        expected_row['title_key'] == actual_row['title_key']):
                        num_rows_correct = num_rows_correct + 1
                        del(expected_rows[i])
            self.assertEquals(len(expected_rows), 0)
            self.assertEquals(num_expected, num_rows_correct)

        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()

    def test_all_music_1(self):
        db_data = test_utils.insert_playlist_into_music_map('backup_1_all_music.m3u8',
                                                            music_roots=['.', './_Done_'])
        actual_song_rows = db_data['song_rows']
        actual_mm_rows = db_data['mm_rows']
        try:
            self.assertEquals(6467, len(actual_song_rows))
            self.assertEquals(6467, len(actual_mm_rows))
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()

    def test_all_music_2(self):
        db_data = test_utils.insert_playlist_into_music_map('backup_2_all_music.m3u8',
                                                            music_roots=['.', './_Done_'])
        actual_song_rows = db_data['song_rows']
        actual_mm_rows = db_data['mm_rows']
        try:
            self.assertEquals(3644, len(actual_song_rows))
            self.assertEquals(3644, len(actual_mm_rows))
        finally:
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()

    # TODO: !2 Move all test code into the try block so if there is any failure, everything gets closed.
    def test_unicode_madness(self):
        db_data = test_utils.insert_playlist_into_music_map('unicode_madness.m3u8',
                                                            music_roots=['.', './_Done_'])
        actual_rows = db_data['song_rows']
        try:
            for row in actual_rows:
                print(row)
        finally:
            # TODO !3 Move this all into a common function.
            db_data['song_cursor'].close()
            db_data['mm_cursor'].close()
            db_data['conn'].close()


if __name__ == "__main__":
    unittest.main()
