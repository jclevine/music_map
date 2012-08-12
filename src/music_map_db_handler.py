# TODO: !2 Add exception handling/logging
# TODO: !2 Try using with statements to handle rollback/commit.
import logging


class MusicMapDBHandler(object):

    def __init__(self, cursor):
        self._cursor = cursor

    def insert_song(self, song):
        new_song_id = None
        if not self._song_in_song_table(song):
            query = """
                    INSERT INTO song
                              ( artist_key
                              , album_key
                              , track_key
                              , title_key)
                         VALUES
                              ( ?
                              , ?
                              , ?
                              , ?
                              )
                   """
            values = (song.artist_key,
                      song.album_key,
                      song.track_key,
                      song.title_key)

            # TODO: !2 Catch exception in case the insert fails. We'll want to
            # just keep going, if it's possible.
            try:
                self._cursor.execute(query, values)
                new_song_id = self._cursor.lastrowid
            except Exception as e:
                msg = "Error inserting song ({0}) into DB: {1}".format(song, e)
                logging.getLogger('unknown_error').error(msg)
                return
        else:
            logging.getLogger('music_map').info("Song already in DB: {0}".format(song))

        # If one has been inserted, we need to populate the other tables, as well.
        if new_song_id:
            self._insert_into_music_map(new_song_id, song)

    def _song_in_song_table(self, song):
        query = """
                SELECT COUNT(*)
                  FROM song s
                 WHERE s.artist_key = ?
                   AND s.album_key  = ?
                   AND s.track_key  = ?
                   AND s.title_key  = ?
                """
        values = (song.artist_key,
                  song.album_key,
                  song.track_key,
                  song.title_key)
        rs = self._cursor.execute(query, values)
        num_rows = rs.fetchone()[0]
        return num_rows == 1

    def _insert_into_music_map(self, new_song_id, song):
        try:
            query = """
                    INSERT INTO music_map
                              ( song_id
                              , location
                              , artist
                              , album
                              , track
                              , title
                              , full_path
                              )
                         VALUES
                              ( ?
                              , ?
                              , ?
                              , ?
                              , ?
                              , ?
                              , ?
                              )
                    """
            values = (new_song_id,
                      unicode(song.music_root),
                      unicode(song.orig_artist),
                      unicode(song.orig_album),
                      unicode(song.orig_track),
                      unicode(song.orig_title),
                      unicode(song.original))


            # TODO: !2 Catch exception in case the insert fails. We'll want to
            # just keep going, if it's possible.
            self._cursor.execute(query, values)
        except Exception as e:
            try:
                values = (new_song_id,
                          song.music_root.decode('latin-1'),
                          song.orig_artist.decode('latin-1'),
                          song.orig_album.decode('latin-1'),
                          song.orig_track.decode('latin-1'),
                          song.orig_title.decode('latin-1'),
                          song.original.decode('latin-1'))
                self._cursor.execute(query, values)
            except Exception as e:  # pragma: no cover
                logging.getLogger('unknown_error').exception(e)  # pragma: no cover
                logging.getLogger('unknown_error').error('Error inserting song into music_map table: {0}'.format(song))  # pragma: no cover

    def close(self):
        self._cursor.close()
