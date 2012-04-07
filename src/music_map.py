#!/usr/bin/python3.1

from optparse import OptionParser
import logging
import os


class MusicMap(object):
   
    def __init__(self):        
        self.parse_options()
        self._handle_logging( self._debug )
        self._logger.debug( "Playlist location: {0}".format(self.playlist_loc))
        self._validate()
        
        
    def parse_options(self):
        parser = OptionParser()
        parser.add_option("-p", "--playlist", dest="playlist_loc",
                           help="Location of the playlist you want to make a " \
                                "map for.", metavar="PLAYLIST")
        parser.add_option("-d", "--debug", action="store_true", dest="debug", 
                           help="Set this flag if you want logging " \
                                "to be set to debug.", default=False)

        options = parser.parse_args()[0]
        self.playlist_loc = os.path.abspath(options.playlist_loc)
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
            open(self.playlist_loc)
        except IOError as ioe:
            self._logger.exception(ioe)
            exit("The playlist you wanted to map does not exist: {0}".format(self.playlist_loc))
        self._logger.info("Using the playlist '{0}'.".format(self.playlist_loc))
    
def main():
    music_map = MusicMap()

        
if __name__ == "__main__":
    main()