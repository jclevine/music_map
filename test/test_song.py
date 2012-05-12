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

    def test_parse_track_space_artist_dash_title(self):
        song_path = "/media/Backup1/Done./Andrea Chivers/Finally, Andrea made you a CD/18 Johnny Cash - Big River.mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('andrea chivers', song.artist_key)
        self.assertEqual('Andrea Chivers', song.orig_artist)

        self.assertEqual('finally, andrea made you a cd', song.album_key)
        self.assertEqual('Finally, Andrea made you a CD', song.orig_album)

        self.assertEqual('18', song.track_key)
        self.assertEqual('18', song.orig_track)

        self.assertEqual("big river", song.title_key)
        self.assertEqual("Big River", song.orig_title)

    def test_parse_parentheses_artist_track_title(self):
        song_path = "/media/Backup1/Done./Bob Dylan/Nashville Skyline/(Bob Dylan) - 07 - One More Night.mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('bob dylan', song.artist_key)
        self.assertEqual('Bob Dylan', song.orig_artist)

        self.assertEqual('nashville skyline', song.album_key)
        self.assertEqual('Nashville Skyline', song.orig_album)

        self.assertEqual('07', song.track_key)
        self.assertEqual('07', song.orig_track)

        self.assertEqual("one more night", song.title_key)
        self.assertEqual("One More Night", song.orig_title)

    def test_parse_artist_with_2_dashes(self):
        song_path = "/media/Backup1/Done./Buck-O-Nine/Songs in the Key of Bree/10 - Buck-O-Nine - She's Fat.mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('buck o nine', song.artist_key)
        self.assertEqual('Buck-O-Nine', song.orig_artist)

        self.assertEqual('songs in key of bree', song.album_key)
        self.assertEqual('Songs in the Key of Bree', song.orig_album)

        self.assertEqual('10', song.track_key)
        self.assertEqual('10', song.orig_track)

        self.assertEqual("she's fat", song.title_key)
        self.assertEqual("She's Fat", song.orig_title)

    def test_parse_track_space_title_with_dash(self):
        song_path = "/media/Backup1/Done./Chuck Berry/The Anthology/41 Nadine (Is It You-).mp3"
        song = Song(song_path, ['/media/Backup1/Done.'])
        self.assertEqual('chuck berry', song.artist_key)
        self.assertEqual('Chuck Berry', song.orig_artist)

        self.assertEqual('anthology', song.album_key)
        self.assertEqual('The Anthology', song.orig_album)

        self.assertEqual('41', song.track_key)
        self.assertEqual('41', song.orig_track)

        self.assertEqual("nadine is it you", song.title_key)
        self.assertEqual("Nadine (Is It You-)", song.orig_title)

    def test_parse_track_space_dash_space_dashed_artist_space_dash_title(self):
        song_path = "/media/Backup1/Various Artists/Critical Mass, Vol. 3/09 - -wumpscut- - Deliverance.mp3"
        song = Song(song_path, ['/media/Backup1'])
        self.assertEqual('various artists', song.artist_key)
        self.assertEqual('Various Artists', song.orig_artist)

        self.assertEqual('critical mass, vol 3', song.album_key)
        self.assertEqual('Critical Mass, Vol. 3', song.orig_album)

        self.assertEqual('09', song.track_key)
        self.assertEqual('09', song.orig_track)

        self.assertEqual("deliverance", song.title_key)
        self.assertEqual("Deliverance", song.orig_title)

    def test_parse_artist_dash_album_dash_track_dash_title(self):
        song_path = "/media/Backup2/high_quality_music/Done./Bob_Dylan/The Basement Tapes/Bob Dylan & The Band - The Basement Tapes - 08 - Bessie Smith.mp3"
        song = Song(song_path, ['/media/Backup2/high_quality_music/Done.'])
        self.assertEqual('bob dylan', song.artist_key)
        self.assertEqual('Bob_Dylan', song.orig_artist)

        self.assertEqual('basement tapes', song.album_key)
        self.assertEqual('The Basement Tapes', song.orig_album)

        self.assertEqual('08', song.track_key)
        self.assertEqual('08', song.orig_track)

        self.assertEqual("bessie smith", song.title_key)
        self.assertEqual("Bessie Smith", song.orig_title)

    def test_parse_track_no_space_dash_title(self):
        song_path = "/media/Backup2/high_quality_music/Done./Brian Eno/music for airports/04-2_2 (9.38).mp3"
        song = Song(song_path, ['/media/Backup2/high_quality_music/Done.'])
        self.assertEqual('brian eno', song.artist_key)
        self.assertEqual('Brian Eno', song.orig_artist)

        self.assertEqual('music for airports', song.album_key)
        self.assertEqual('music for airports', song.orig_album)

        self.assertEqual('04', song.track_key)
        self.assertEqual('04', song.orig_track)

        self.assertEqual("2 2 938", song.title_key)
        self.assertEqual("2_2 (9.38)", song.orig_title)
