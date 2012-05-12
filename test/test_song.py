import unittest
from song import Song


class SongTest(unittest.TestCase):

    def test_regular_song_parse(self):
        song_path = "./media/Backup1/Christian Death/Jesus Points the Bones at You/01 - Christian Death - Believers of the Unpure.mp3"
        song = Song(song_path)
        self.assertEqual('christian death', song.artist)
        self.assertEqual('Christian Death', song.orig_artist)

        self.assertEqual('jesus points the bones at you', song.album)
        self.assertEqual('Jesus Points the Bones at You', song.orig_album)

        self.assertEqual('01', song.track)
        self.assertEqual('01', song.orig_track)

        self.assertEqual('believers of the unpure', song.title)
        self.assertEqual('Believers of the Unpure', song.orig_title)

    def test_incorrect_track_number(self):
        song_path = "//music/A Tribe Called Quest/The Low End Theory/03 - A Tribe Called Quest - Rap Promoter.mp3"
        song = Song(song_path)
        self.assertEqual('a tribe called quest', song.artist)
        self.assertEqual('A Tribe Called Quest', song.orig_artist)

        self.assertEqual('low end theory', song.album)
        self.assertEqual('The Low End Theory', song.orig_album)

        self.assertEqual('03', song.track)
        self.assertEqual('03', song.orig_track)

        self.assertEqual('rap promoter', song.title)
        self.assertEqual('Rap Promoter', song.orig_title)
