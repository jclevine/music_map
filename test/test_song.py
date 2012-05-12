import unittest
from song import Song


class SongTest(unittest.TestCase):

    def test_regular_song_parse(self):
        song_path = "./media/Backup1/Christian Death/Jesus Points the Bones at You/01 - Christian Death - Believers of the Unpure.mp3"
        song = Song(song_path)
        self.assertEqual('christian death', song.artist)
        self.assertEqual('Christian Death', song.orig_artist)

        self.assertEqual('jesus points bones at you', song.album)
        self.assertEqual('Jesus Points the Bones at You', song.orig_album)

        self.assertEqual('01', song.track)
        self.assertEqual('01', song.orig_track)

        self.assertEqual('believers of unpure', song.title)
        self.assertEqual('Believers of the Unpure', song.orig_title)

    def test_incorrect_track_number(self):
        song_path = "./media/Backup1/Done./A_Tribe_Called_Quest/The Low End Theory/10.Everything_Is_Fair.mp3"
        song = Song(song_path)
        self.assertEqual('a tribe called quest', song.artist)
        self.assertEqual('A_Tribe_Called_Quest', song.orig_artist)

        self.assertEqual('low end theory', song.album)
        self.assertEqual('The Low End Theory', song.orig_album)

        self.assertEqual('10', song.track)
        self.assertEqual('10', song.orig_track)

        self.assertEqual('everything is fair', song.title)
        self.assertEqual('Everything_Is_Fair', song.orig_title)

    def test_complicated_specific_path(self):
        song_path = "./media/Backup1/Ludwig Van Beethoven/Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84/03_Ludwig Van Beethoven_Symphony No. 5 in C minor, Op. 67- Allegro Allegro.mp3"
        song = Song(song_path)
        self.assertEqual('ludwig van beethoven', song.artist)
        self.assertEqual('Ludwig Van Beethoven', song.orig_artist)

        self.assertEqual('symphony no 5 in c minor, op 67 egmont overture, op84', song.album)
        self.assertEqual('Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84', song.orig_album)

        self.assertEqual('03', song.track)
        self.assertEqual('03', song.orig_track)

        self.assertEqual('symphony no 5 in c minor, op 67 allegro allegro', song.title)
        self.assertEqual('Symphony No. 5 in C minor, Op. 67- Allegro Allegro', song.orig_title)
