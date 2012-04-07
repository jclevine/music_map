#!/usr/bin/python3.1

from optparse import OptionParser
import logging
import os
import re


class MusicMap(object):


    OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE = r"//music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- ([^\.]+)\.mp3"
    OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE_WITH_PERIODS = r"//music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- (.*)\.mp3"
    OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE = r"//music/([^/]+)/([^/]+)/(\d+)[^-]+- ([^\.]+)\.mp3"



    def __init__(self):
        self.parse_options()
        self._handle_logging(self._debug)
        self._logger.debug("Playlist location: {0}".format(self._playlist_loc))
        self._validate()
        self._song_set = self._build_song_set()
        self._music_map = self._build_music_map()


    def parse_options(self):
        parser = OptionParser()
        parser.add_option("-p", "--playlist", dest="playlist_loc",
                           help="Location of the playlist you want to make a " \
                                "map for.", metavar="PLAYLIST")
        parser.add_option("-d", "--debug", action="store_true", dest="debug",
                           help="Set this flag if you want logging " \
                                "to be set to debug.", default=False)

        options = parser.parse_args()[0]
        self._playlist_loc = os.path.abspath(options.playlist_loc)
        self._debug = options.debug
#        self._playlist_1 = os.path.join( self._playlists_dir, options.playlist_1 )

    # TODO: !3 Logging ini file?
    def _handle_logging(self, debug):
        self._logger = logging.getLogger("music_map")

        self._logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("music_map.log", mode='w')
        file_handler.setLevel(logging.DEBUG)
        if debug:
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.INFO)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)


    def _validate(self):
        try:
            open(self._playlist_loc)
        except IOError as ioe:
            self._logger.exception(ioe)
            exit("The playlist you wanted to map does not exist: {0}".format(self._playlist_loc))
        self._logger.info("Using the playlist '{0}'.".format(self._playlist_loc))

    def _build_song_set(self):
        playlist = open(self._playlist_loc, 'r')
        songs = set(playlist)
        self._logger.debug("{0} of songs in playlist.".format(len(songs)))
        return songs

    def _build_music_map(self):
        for song in self._song_set:
            # TODO: !3 Better place to define regexes?
            # TODO: !3 Some utility to grab regex matches to a dictionary?
            try:
                matches = re.match(self.OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE, song)
                if not matches:
                    matches = re.match(self.OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE, song)
                self._logger.debug("Artist: {artist}{line_sep}" \
                                   "Album: {album}{line_sep}" \
                                   "Track #: {track}{line_sep}" \
                                   "Title: {title}{line_sep}{line_sep}"
                                   .format(artist=matches.group(1),
                                           album=matches.group(2),
                                           track=matches.group(3),
                                           title=matches.group(4),
                                           line_sep=os.linesep))
            except Exception as e:
                self._logger.exception(e)
                exit("Error parsing info out of '{0}'".format(song))
        return {}

def main():
    music_map = MusicMap()


if __name__ == "__main__":
    main()
