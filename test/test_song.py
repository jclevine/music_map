import unittest
from song import Song


class SongTest(unittest.TestCase):

    def test_parse_track_dash_artist_dash_title(self):
        song_path = "/media/Backup1/Christian Death/Jesus Points the Bones at You/01 - Christian Death - Believers of the Unpure.mp3"
        song = Song(song_path, ['/media/Backup1'])
        self.assertEqual('christian death', song.artist_key)
        self.assertEqual('Christian Death', song.orig_artist)

        self.assertEqual('jesus points bones at you', song.album_key)
        self.assertEqual('Jesus Points the Bones at You', song.orig_album)

        self.assertEqual('01', song.track_key)
        self.assertEqual('01', song.orig_track)

        self.assertEqual('believers of unpure', song.title_key)
        self.assertEqual('Believers of the Unpure', song.orig_title)

    def test_parse_track_dot_title(self):
        song_path = "/media/Backup1/Done./A_Tribe_Called_Quest/The Low End Theory/10.Everything_Is_Fair.mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('a tribe called quest', song.artist_key)
        self.assertEqual('A_Tribe_Called_Quest', song.orig_artist)

        self.assertEqual('low end theory', song.album_key)
        self.assertEqual('The Low End Theory', song.orig_album)

        self.assertEqual('10', song.track_key)
        self.assertEqual('10', song.orig_track)

        self.assertEqual('everything is fair', song.title_key)
        self.assertEqual('Everything_Is_Fair', song.orig_title)

    def test_parse_complicated_specific_path(self):
        song_path = "/media/Backup1/Ludwig Van Beethoven/Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84/03_Ludwig Van Beethoven_Symphony No. 5 in C minor, Op. 67- Allegro Allegro.mp3"
        song = Song(song_path, ['/media/Backup1'])
        self.assertEqual('ludwig van beethoven', song.artist_key)
        self.assertEqual('Ludwig Van Beethoven', song.orig_artist)

        self.assertEqual('symphony no 5 in c minor, op 67 egmont overture, op84', song.album_key)
        self.assertEqual('Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84', song.orig_album)

        self.assertEqual('03', song.track_key)
        self.assertEqual('03', song.orig_track)

        self.assertEqual('symphony no 5 in c minor, op 67 allegro allegro', song.title_key)
        self.assertEqual('Symphony No. 5 in C minor, Op. 67- Allegro Allegro', song.orig_title)

    def test_parse_artist_with_dash(self):
        song_path = "/media/Backup1/Man or Astro-man/Unknown/14 - Man or Astro-man - Track 14.mp3"
        song = Song(song_path, ['/media/Backup1'])
        self.assertEqual('man or astro man', song.artist_key)
        self.assertEqual('Man or Astro-man', song.orig_artist)

        self.assertEqual('unknown', song.album_key)
        self.assertEqual('Unknown', song.orig_album)

        self.assertEqual('14', song.track_key)
        self.assertEqual('14', song.orig_track)

        self.assertEqual('track 14', song.title_key)
        self.assertEqual('Track 14', song.orig_title)

    def test_parse_track_space_title(self):
        song_path = "/media/Backup1/Done./Chuck Berry/The Anthology/35 Bye Bye Johnny.mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('chuck berry', song.artist_key)
        self.assertEqual('Chuck Berry', song.orig_artist)

        self.assertEqual('anthology', song.album_key)
        self.assertEqual('The Anthology', song.orig_album)

        self.assertEqual('35', song.track_key)
        self.assertEqual('35', song.orig_track)

        self.assertEqual('bye bye johnny', song.title_key)
        self.assertEqual('Bye Bye Johnny', song.orig_title)

    def test_parse_track_dash_title(self):
        song_path = "/media/Backup1/Patti Smith/Radio Ethopia/02 - Ain't It Strange.mp3"
        song = Song(song_path, ['/media/Backup1'])
        self.assertEqual('patti smith', song.artist_key)
        self.assertEqual('Patti Smith', song.orig_artist)

        self.assertEqual('radio ethopia', song.album_key)
        self.assertEqual('Radio Ethopia', song.orig_album)

        self.assertEqual('02', song.track_key)
        self.assertEqual('02', song.orig_track)

        self.assertEqual("ain't it strange", song.title_key)
        self.assertEqual("Ain't It Strange", song.orig_title)
