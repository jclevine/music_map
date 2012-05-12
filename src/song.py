import re
import logging
from music_map_exceptions import UnparseableSongError
from util import string_utils


# TODO: !2 Figure out a way to organize and iterate over all regexes to figure
# out which format it is
# TODO: !3 Move to common place for all projects to use.
class Song(object):

    # TODO: !3 Use named subgroups [http://docs.python.org/library/re.html#re.MatchObject.groupdict]
    # TODO: !2 Gotta be a better way to define these regexes. Use music_root(s), for instance.
    # TODO: !3 Name regexes better and give examples.
    # TODO: !2 Doublecheck order of regexes so that more specific ones come before the more general ones.
#    MUSIC_REGEXES = {'SPECIFIC_BEETHOVEN_REGEX': r"/media/Backup1/([^/]+)/([^/]+)/(\d+)_[^_]+_(.*)\.mp3",
#                     'OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE': r"//music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- (.*)\.mp3",
#                     'OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE': r"//music/([^/]+)/([^/]+)/(\d+)[^-]+- (.*)\.mp3",
#                     # Special for stupid Man or Astroman files.
#                     'MOAM_REGEX': r"/media/Backup1/([^/]+)/([^/]+)/(\d+)[^-]+- Man or Astro-man- - (.*)\.mp3",
#                     'BACKUP_1_REGEX_WITH_ARTIST_IN_FILE': r"/media/Backup1/([^/]+)/([^/]+)/(\d+)[^-]+- [^-]+- (.*)\.mp3",
#                     'BACKUP_1_REGEX_WITH_ARTIST_PARAENTHESIZED': r"/media/Backup1/Done\./([^/]+)/([^/]+)/[^-]+ - (\d+)[^-]+- (.*)\.mp3",
#                     'BACKUP_1_REGEX_IN_DONE': r"/media/Backup1/Done\./([^/]+)/([^/]+)/(\d+)[^-]+- [^-]+- (.*)\.mp3",
#                     'BACKUP_1_REGEX_IN_DONE_PERIOD_TRACK': r"/media/Backup1/Done\./([^/]+)/([^/]+)/(\d+)\.(.*)\.mp3",
#                     'BACKUP_1_REGEX_IN_DONE_PERIOD_SPACE_TRACK': r"/media/Backup1/Done\./([^/]+)/([^/]+)/(\d+) (.*)\.mp3",
#                     'BACKUP_1_REGEX_TRACK_UNDERSCORE': r"/media/Backup1/([^/]+)/([^/]+)/(\d+)[^_]+_(.*)\.mp3",
#                     'BACKUP_1_REGEX_IN_DONE_MIX_CD': r"/media/Backup1/Done\./([^/]+)/([^/]+)/(\d+) - [^-]+- (.*)\.mp3",
#                     'BACKUP_1_REGEX_TRACK_SPACE': r"/media/Backup1/([^/]+)/([^/]+)/(\d+) [^-]+- (.*)\.mp3",
#                     # I think this one has to be last since it's the most relaxed regex
#                     'BACKUP_1_REGEX_TRACK_TITLE': r"/media/Backup1/([^/]+)/([^/]+)/(\d+) - (.*)\.mp3",
#                     'BACKUP_2_REGEX': r"/media/Backup2/high_quality_music/([^/]+)/([^/]+)/(\d+)\.(.*)\.mp3",
#                     'BACKUP_2_DONE_REGEX': r"/media/Backup2/high_quality_music/Done\./([^/]+)/([^/]+)/(\d+)\.(.*)\.mp3",
#                     'BACKUP_2_DONE_REGEX_ARTIST_ALBUM_TRACK_TITLE': r"/media/Backup2/high_quality_music/Done\./([^/]+)/([^/]+)/[^-]+-[^-]+- (\d+) - (.*)\.mp3",
#                     'BACKUP_2_DONE_REGEX_TRACK_TITLE': r"/media/Backup2/high_quality_music/Done\./([^/]+)/([^/]+)/(\d+) - (.*)\.mp3",
#                     'BACKUP_2_REGEX_TRACK_TITLE_ARTIST_TITLE': r"/media/Backup2/high_quality_music/([^/]+)/([^/]+)/(\d+) - [^-]+- (.*)\.mp3",
#                     'BACKUP_2_REGEX_TRACK_TITLE': r"/media/Backup2/high_quality_music/([^/]+)/([^/]+)/(\d+) (.*)\.mp3",
#                     'BACKUP_2_DONE REGEX_TRACK_TITLE': r"/media/Backup2/high_quality_music/Done\./([^/]+)/([^/]+)/(\d+)-(.*)\.mp3",
#                     'BACKUP_2_DONE REGEX_TRACK_SPACE_TITLE': r"/media/Backup2/high_quality_music/Done\./([^/]+)/([^/]+)/(\d+) (.*)\.mp3",
#
#                     # //<microSD1>/music/Eno/Here Come the Warm Jets/03 - Brian Eno - Baby's On Fire.mp3
#                     'SANSA_CARD_MUSIC': r"//<microSD1>/music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- (.*)\.mp3",
#
#                     # //high_quality_music/Belle_and_Sebastian/Dear Catastrophe Waitress/05.Belle_&_Sebastian.Asleep_On_A_Sunbeam.mp3
#                     'SANSA_HQM': r"//high_quality_music/([^/]+)/([^/]+)/(\d+)\.[^.]+\.(.*)\.mp3",
#
#                     # //<microSD1>/music/Bright Eyes/Fevers & Mirrors/09 The Center of the World.mp3
#                     'SANSA_CARD_MUSIC_WITHOUT_DASH': r"//<microSD1>/music/([^/]+)/([^/]+)/(\d+) (.*)\.mp3"
#                     }
    MUSIC_REGEXES = {'ROOT/ARTIST/ALBUM/TRACK - ARTIST - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) - [^-]+- (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK.TITLE': r"{root}/([^/]+)/([^/]+)/(\d+)\.([^.]+)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK_ARTIST_TITLE': r"{root}/([^/]+)/([^/]+)/(\d+)_[^_]+_(.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK - ARTIST_WITH_ONE_DASH - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) - [^-]+-[^-]+- (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) ([^-]+)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) - ([^-]+)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK ARTIST - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) [^-]+- ([^.]+)\.mp3",
                     'ROOT/ARTIST/ALBUM/(ARTIST) - TRACK - TITLE': r"{root}/([^/]+)/([^/]+)/\([^)]+\) - (\d+) - (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK - ARTIST_WITH_2_DASHES - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) - [^-]+-[^-]+-[^-]+- (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK TITLE_WITH_ONE_DASH': r"{root}/([^/]+)/([^/]+)/(\d+) ([^-]+-[\S^.])\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK - DASHED_ARTIST - TITLE': r"{root}/([^/]+)/([^/]+)/(\d+) - \S+ - (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/ARTIST - ALBUM - TRACK - TITLE': r"{root}/([^/]+)/([^/]+)/[^-]+- [^-]+- (\d+) - (.*)\.mp3",
                     'ROOT/ARTIST/ALBUM/TRACK-TITLE': r"{root}/([^/]+)/([^/]+)/(\d+)-(.*)\.mp3",
                     'ROOT/Sonic_Youth/ALBUM/TRACK TITLE_WITH_DASH': r"{root}/(Sonic_Youth)/([^/]+)/(\d+) ([^-]+-[^.]+)\.mp3",
                     "ROOT/Bonnie 'Prince' Billy/ALBUM/TRACK TITLE_WITH_DASH": r"{root}/(Bonnie 'Prince' Billy)/([^/]+)/(\d+) ([^-]+-[^.]+)\.mp3",
                     "ROOT/ARTIST/ALBUM/TRACK.ARTIST.TITLE": r"{root}/([^/]+)/([^/]+)/(\d+)\.[^.]+\.([^.]+)\.mp3"
                     }

    # TODO: !3 Throw more specific exceptions
    # TODO: !2 Have to_map function that will prepare song for insertion into table
    def __init__(self, song, music_roots):
        self._original = song

        # TODO: !2 Yet again, handle logging/exceptions better.
        # TODO: !2 Refactor this possibly.
        # Try each regex with all the possible roots and see if there's a match.
        matches = False
        for regex in Song.MUSIC_REGEXES.values():
            for music_root in music_roots:
                try:
                    matches = re.match(regex.format(root=music_root), song)
                    if matches:
                        self._music_root = music_root
                        break
                except AttributeError:  # When does this happen?
                    logger = logging.getLogger("music_map")
                    # logger.exception(ae)
                    logger.debug("Error parsing info out of '{0}'. Continuing."
                                       .format(song))
                    logging.getLogger("unparseable").error(song)
                    # TODO: !3 Manual way for a user to parse out the data?s
                except Exception as e:
                    logger = logging.getLogger("music_map")
                    logger.exception(e)
                    logger.error("Unknown error on '{0}'. Continuing."
                                 .format(song))
                    logging.getLogger("unparseable").error(song)
            if matches:
                break

        if not matches:
            raise UnparseableSongError(song)

        # Very special case for this stupid track.
        # TODO: !3 Have a query as to how to separate out an unparseable song.
        ss = string_utils.sanitize_string

        # TODO: !3 Some utility to grab regex matches into a dictionary?
        self._orig_artist = matches.group(1)
        self._artist_key = ss(self._orig_artist, remove_the=True, remove_and=True)

        self._orig_album = matches.group(2)
        self._album_key = ss(self._orig_album, remove_the=True, remove_and=True)

        self._orig_track = matches.group(3)
        self._track_key = ss(self._orig_track, remove_the=True, remove_and=True)

        self._orig_title = matches.group(4)
        self._title_key = ss(self._orig_title, remove_the=True, remove_and=True)

    @property
    def artist_key(self):
        return self._artist_key

    @property
    def album_key(self):
        return self._album_key

    @property
    def track_key(self):
        return self._track_key

    @property
    def title_key(self):
        return self._title_key

    @property
    def orig_artist(self):
        return self._orig_artist

    @property
    def orig_album(self):
        return self._orig_album

    @property
    def orig_track(self):
        return self._orig_track

    @property
    def orig_title(self):
        return self._orig_title

    @property
    def original(self):
        return self._original

    @property
    def music_root(self):
        return self._music_root

    def __repr__(self):
        return ("{artist} | {album} | {track} | {title}"
                .format(artist=self.artist_key,
                        album=self.album_key,
                        track=self.track_key,
                        title=self.title_key))
