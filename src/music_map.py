#!/usr/bin/python3.1

# TODO: !3 Replace OptionParser with argparse.
# TODO: !2 Organize this mess's directory structure.
from optparse import OptionParser
import logging
import os
import sqlite3
import song as song_entity
from music_map_db_handler import MusicMapDBHandler
from music_map_exceptions import UnparseableSongError


class MusicMap(object):
    """
    Takes in a large file of where your music is located and :
    1. Inserts it into a song table so that we have a unique row to identity
       every song you own.
    2. Insert into a music_map table that maps the unique song id to the actual
       location of the song.
    """

    def __init__(self, *args):
        if not args:
            self._parse_options()  # pragma: no cover
        else:
            # TODO: !3 Put this in a function.
            kwargs = args[0]
            self._playlist_loc = kwargs['playlist_loc']
            self._music_roots = kwargs['music_roots']
            self._db_loc = kwargs['db_loc']
            self._debug = kwargs['debug']

        try:
            self._handle_logging(self._debug)
            self._logger.debug("Playlist location: {0}".format(self._playlist_loc))
            # TODO: !3 Bring this sql stuff into its own function
            self._conn = sqlite3.connect(self._db_loc)
            self._cursor = self._conn.cursor()
            self._cursor.execute('PRAGMA synchronous=OFF')
            self._cursor.execute('PRAGMA count_changes=OFF')
            self._cursor.execute('PRAGMA journal_mode=MEMORY')
            self._cursor.execute('PRAGMA temp_store=MEMORY')
            self._db_handler = MusicMapDBHandler(self._cursor)
            self._validate()
            self._song_set = self._build_song_set()
            self._music_map = self._build_music_map()
            self._conn.commit()
        finally:
            self._conn.rollback()
            self._conn.close()
            self._close_logging_handlers()

    def _parse_options(self):  # pragma: no cover
        parser = OptionParser()
        parser.add_option("-p", "--playlist", dest="playlist_loc",
                           help="Location of the playlist you want to make a " \
                                "map for.", metavar="PLAYLIST")
        parser.add_option("--music_roots", dest="music_roots_csv",
                          help="The csv of full paths to the root of the music trees " \
                               "inside the playlist. Do not include ending /.",
                               metavar="ROOT_PATHS_CSV")
        parser.add_option("-d", "--debug", action="store_true", dest="debug",
                           help="Set this flag if you want logging " \
                                "to be set to debug.", default=False)
        parser.add_option("--db", dest="db_loc", help="Location of the DB",
                          metavar="DB")

        options = parser.parse_args()[0]
        self._playlist_loc = os.path.abspath(options.playlist_loc)
        self._music_roots = options.music_roots_csv.split(',')
        self._db_loc = options.db_loc
        self._debug = options.debug

    # TODO: !3 Logging ini file?
    # TODO: !3 Define where the logs go. Location is sort of bad now.
    def _handle_logging(self, debug):
        self._logger = logging.getLogger("music_map")

        self._logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler("music_map.log", mode='w')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        if debug:
            console_handler.setLevel(logging.DEBUG)  # pragma: no cover
        else:
            console_handler.setLevel(logging.INFO)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

        # TODO: !3 Factory for logs?
        self._unparseable = logging.getLogger("unparseable")
        self._unparseable.setLevel(logging.DEBUG)
        unparseable_handler = logging.FileHandler("unparseable.log", mode="w")
        unparseable_handler.setLevel(logging.DEBUG)
        self._unparseable.addHandler(unparseable_handler)

        self._unknown_error = logging.getLogger("unknown_error")
        self._unknown_error.setLevel(logging.DEBUG)
        unknown_error_handler = logging.FileHandler("unknown_error.log", mode="w")
        unknown_error_handler.setLevel(logging.DEBUG)
        self._unknown_error.addHandler(unknown_error_handler)

    def _close_logging_handlers(self):
        for handler in self._logger.handlers:
            handler.close()
        for handler in self._unparseable.handlers:
            handler.close()
        for handler in self._unknown_error.handlers:
            handler.close()

    def _validate(self):
        try:
            open(self._playlist_loc)
        except IOError as ioe:
            self._logger.exception(ioe)
            exit("The playlist you wanted to map does not exist: {0}"
                 .format(self._playlist_loc))
        self._logger.info("Using the playlist '{0}'.".format(self._playlist_loc))

    def _build_song_set(self):
        playlist = open(self._playlist_loc, 'r')
        songs = set(playlist)
        self._logger.debug("{0} of songs in playlist.".format(len(songs)))
        return songs

    # TODO: !2 Handle exceptions consistently and with appropriate logging,
    # especially for unparseable stuff.
    # TODO: !2 Threading?
    def _build_music_map(self):
        num_songs = len(self._song_set)
        for i, song in enumerate(self._song_set):
            try:
                song_obj = song_entity.Song(song, self._music_roots)
            except UnparseableSongError:
                self._logger.debug("Error parsing info out of '{0}'. Continuing."
                                   .format(song))
                self._unparseable.error(song)
                continue
            finally:
                if i % 100 == 0 or i == num_songs - 1:
                    self._logger.info("{0}/{1}".format(i + 1, num_songs))

            self._db_handler.insert_song(song_obj)
        self._db_handler.close()


def main():
    MusicMap()  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    main()
