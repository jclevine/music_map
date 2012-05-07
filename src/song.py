import re
from music_map import MusicMap
import logging
from music_map_exceptions import UnparseableSongError


# TODO: !2 Figure out a way to organize and iterate over all regexes to figure
# out which format it is
class Song(object):

    # TODO: !3 Use named subgroups [http://docs.python.org/library/re.html#re.MatchObject.groupdict]
    MUSIC_REGEXES = {'OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE': r"//music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- (.*)\.mp3",
                     'OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE': r"//music/([^/]+)/([^/]+)/(\d+)[^-]+- (.*)\.mp3",
                     'BACKUP_1_REGEX_WITH_ARTIST_IN_FILE': r"\./media/Backup1/([^/]+)/([^/]+)/(\d+)[^-]+- [^-]+- (.*)\.mp3",
                     'BACKUP_1_REGEX_IN_DONE': r"\./media/Backup1/([^/]+)/([^/]+)/(\d+)[^-]+- [^-]+- (.*)\.mp3"}

    # TODO: !3 Throw more specific exceptions
    # TODO: !2 Have to_map function that will prepare song for insertion into table
    def __init__(self, song):
        self._original = song

        # TODO: !2 Yet again, handle logging/exceptions better.
        for regex in Song.MUSIC_REGEXES.values():
            try:
                matches = re.match(regex, song)

                if not matches:
                    continue
            except AttributeError as ae:  # When does this happen?
                logger = logging.getLogger("music_map")
                logger.exception(ae)
                logger.error("Error parsing info out of '{0}'. Continuing."
                                   .format(song))
                logging.getLogger("unparseable").error(song)
                # TODO: !3 Manual way for a user to parse out the data?s
            except Exception as e:
                logger = logging.getLogger("music_map")
                logger.exception(e)
                logger.error("Unknown error on '{0}'. Continuing."
                             .format(song))
                logging.getLogger("unparseable").error(song)

        if not matches:
            raise UnparseableSongError(song)

        # Very special case for this stupid track.
        # TODO: !3 Have a query as to how to separate out an unparseable song.
        ss = MusicMap.sanitize_string
        if '//music/Ludwig Van Beethoven/Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84/04_Ludwig Van Beethoven_Egmont Overture, Op. 84.mp3' in song:
            self._artist = ss('Ludwig Van Beethoven')
            self._album = ss('Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84')
            self._track = ss('04')
            self._title = ss('Egmont Overture, Op. 84')
        else:
            # TODO: !3 Some utility to grab regex matches to a dictionary?
            self._orig_artist = matches.group(1)
            self._artist = ss(self._orig_artist, remove_the=True, remove_and=True)

            self._orig_album = matches.group(2)
            self._album = ss(self._orig_album)

            self._orig_track = matches.group(3)
            self._track = ss(self._orig_track)

            self._orig_title = matches.group(4)
            self._title = ss(self._orig_title)

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def track(self):
        return self._track

    @property
    def title(self):
        return self._title

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

    def __repr__(self, *args, **kwargs):
        return ("{artist} - {album} - {track} {title} | {orig_artist} - {orig_album} - {orig_track} {orig_title}"
                .format(artist=self.artist,
                        album=self.album,
                        track=self.track,
                        title=self.title,
                        orig_artist=self.artist,
                        orig_album=self.album,
                        orig_track=self.track,
                        orig_title=self.title))
