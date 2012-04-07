#!/usr/bin/python3.1

from optparse import OptionParser
import logging
import os
import re
from collections import defaultdict
import unicodedata


class MusicMap(object):


    OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE = r"//music/([^/]+)/([^/]+)/(\d+)[^-]+-[^-]+- (.*)\.mp3"
    OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE = r"//music/([^/]+)/([^/]+)/(\d+)[^-]+- (.*)\.mp3"


    def __init__(self):
        self._parse_options()
        self._handle_logging(self._debug)
        self._logger.debug("Playlist location: {0}".format(self._playlist_loc))
        self._validate()
        self._song_set = self._build_song_set()
        self._music_map = self._build_music_map()
        self._all_tracks = self._all_tracks()
        self._index = -1


    def _parse_options(self):
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

        # TODO: !3 Factory for logs?
        self._unparseable = logging.getLogger("unparseable")
        self._unparseable.setLevel(logging.DEBUG)
        unparseable_handler = logging.FileHandler("unparseable.log", mode="w")
        unparseable_handler.setLevel(logging.DEBUG)
        self._unparseable.addHandler(unparseable_handler)

        self._unknown_error = logging.getLogger("unknown_error")
        self._unknown_error.setLevel(logging.DEBUG)
        unknow_error_handler = logging.FileHandler("unknown_error.log", mode="w")
        unknow_error_handler.setLevel(logging.DEBUG)
        self._unknown_error.addHandler(unknow_error_handler)

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
        music_map = defaultdict(dict)
        for song in self._song_set:
            # TODO: !3 Better place to define regexes?
            # TODO: !3 Some utility to grab regex matches to a dictionary?
            try:
                matches = re.match(self.OLD_IPOD_REGEX_WITH_ARTIST_IN_FILE, song)
                if not matches:
                    matches = re.match(self.OLD_IPOD_REGEX_WITHOUT_ARTIST_IN_FILE, song)

                artist = MusicMap.sanitize_string(matches.group(1),
                                                  remove_the=True,
                                                  remove_and=True)
                album = MusicMap.sanitize_string(matches.group(2))
                track = MusicMap.sanitize_string(matches.group(3))
                title = MusicMap.sanitize_string(matches.group(4))

                self._logger.debug("Artist: {artist}{line_sep}" \
                                   "Album: {album}{line_sep}" \
                                   "Track #: {track}{line_sep}" \
                                   "Title: {title}{line_sep}{line_sep}"
                                   .format(artist=artist,
                                           album=album,
                                           track=track,
                                           title=title,
                                           line_sep=os.linesep))

                music_map[artist].setdefault(album, {})
                #music_map[artist][album].setdefault(track, str)
                music_map[artist][album][track] = title
                #musicalbum
                #music_map[artist][track].setdefault(album, [])
                #music_map[artist][album][track].append((track, title))

            except AttributeError as ae:
                self._logger.exception(ae)
                self._logger.error("Error parsing info out of '{0}'. Continuing.".format(song))
                self._unparseable.error(song)
                # TODO: !3 Manual way for a user to parse out the data?s
            except Exception as e:
                self._logger.exception(e)
                self._logger.error("Unknown error on '{0}'. Continuing.".format(song))
                self._unparseable.error(song)

        return music_map

    # TODO: !3 Put into a utility function somewhere.
    @staticmethod
    def sanitize_string(s):
        s = s.lower()
        s = s.replace("_", " ")
        s = s.replace(".", "")
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
        return s

    def find(self, artist, album, track):
        ss = MusicMap.sanitize_string
        return self._music_map[ss(artist)][ss(album)][ss(track)]


    def __iter__(self):
        return self


    def __next__(self):
        self._index = self._index + 1
        if self._index >= len(self._all_tracks):
            raise StopIteration
        else:
            return self._all_tracks[self._index]


    def items(self):
        """
        A generator of all the tracks, returning each as a map with each 
        'part' of the track: artist, album, track, and title.
        """
        for artist, albums in self._music_map.items():
            for album, tracks in albums.items():
                for track, title in tracks.items():
                    yield {'artist': artist,
                           'album': album,
                           'track': track,
                           'title': title}

    def _all_tracks(self):
        return [track for track in self.items()]


def main():
    music_map = MusicMap()
    for track in music_map:
        print(track)


if __name__ == "__main__":
    main()
