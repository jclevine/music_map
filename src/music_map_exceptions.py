class UnparseableSongError(Exception):
    def __init__(self, unparseable_song):
        self._unparseable_song = unparseable_song

    def __str__(self):
        return repr(self._unparseable_song)
