import unittest
from song import Song


class SongTest(unittest.TestCase):

    def test_parse_track_artist_title(self):
        song_path = "./Elliott_Smith/Elliott_Smith/06_Elliott Smith_Coming up Roses.mp3"
        song = Song(song_path, ['.'])
        self.assertEqual('elliott smith', song.artist_key)
        self.assertEqual('Elliott_Smith', song.orig_artist)

        self.assertEqual('elliott smith', song.album_key)
        self.assertEqual('Elliott_Smith', song.orig_album)

        self.assertEqual('06', song.track_key)
        self.assertEqual('06', song.orig_track)

        self.assertEqual('coming up roses', song.title_key)
        self.assertEqual('Coming up Roses', song.orig_title)

    def test_parse_done_root_track_artist_title(self):
        song_path = "./_Done_/Black Sabbath/Master Of Reality/04_Black Sabbath_Children Of The Grave.mp3"
        song = Song(song_path, ['./_Done_'])
        self.assertEqual('black sabbath', song.artist_key)
        self.assertEqual('Black Sabbath', song.orig_artist)

        self.assertEqual('master of reality', song.album_key)
        self.assertEqual('Master Of Reality', song.orig_album)

        self.assertEqual('04', song.track_key)
        self.assertEqual('04', song.orig_track)

        self.assertEqual('children of grave', song.title_key)
        self.assertEqual('Children Of The Grave', song.orig_title)

    def test_parse_root_track_dot_title(self):
        song_path = "./Dead_Kennedys/Plastic_Surgery_Disasters_+_In_God_We_Trust,_Inc./02.Terminal_Preppie.mp3"
        song = Song(song_path, ['.'])
        self.assertEqual('dead kennedys', song.artist_key)
        self.assertEqual('Dead_Kennedys', song.orig_artist)

        self.assertEqual('plastic surgery disasters in god we trust inc', song.album_key)
        self.assertEqual('Plastic_Surgery_Disasters_+_In_God_We_Trust,_Inc.', song.orig_album)

        self.assertEqual('02', song.track_key)
        self.assertEqual('02', song.orig_track)

        self.assertEqual('terminal preppie', song.title_key)
        self.assertEqual('Terminal_Preppie', song.orig_title)

    def test_unparseable_done_backup_1(self):
        song_path = "./_Done_/Belle_and_Sebastian/The Boy with the Arab Strap/06_Belle & Sebastian_Seymour Stein.mp3"
        song = Song(song_path, ['.', './_Done_'])
        self.assertEqual('belle sebastian', song.artist_key)
        self.assertEqual('Belle_and_Sebastian', song.orig_artist)

        self.assertEqual('boy with arab strap', song.album_key)
        self.assertEqual('The Boy with the Arab Strap', song.orig_album)

        self.assertEqual('06', song.track_key)
        self.assertEqual('06', song.orig_track)

        self.assertEqual('seymour stein', song.title_key)
        self.assertEqual('Seymour Stein', song.orig_title)
