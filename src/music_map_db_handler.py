# TODO: !1 Add exception handling/logging


class MusicMapDBHandler(object):

    def __init__(self, conn):
        self._conn = conn

    def insert_song(self, song, music_root):
        # TODO: !1 Figure out when/where to close cursors/connections.
        c = self._conn.cursor()
        if not self._song_in_song_db(c, song):
            query = """
                    INSERT INTO song
                              ( artist_key
                              , album_key
                              , track_key
                              , title_key)
                         VALUES ?
                              , ?
                              , ?
                              , ?
                              )
                   """
            values = (song.artist,
                      song.album,
                      song.track,
                      song.title)
            try:
                c.execute(query, values)
                new_song_id = c.lastrowid
            except Exception:
                self._conn.rollback()
            finally:
                c.close()
                self._conn.commit()

        # If one has been inserted, we need to populate the other tables, as well.
        if new_song_id:
            self._insert_into_music_map(new_song_id, song, music_root)

    def _song_in_cursor_db(self, c, song):
        query = """
                SELECT COUNT(*)
                  FROM song s
                 WHERE s.artist_key = ?
                   AND s.album_key  = ?
                   AND s.track_key  = ?
                   AND s.title_key  = ?
                """
        values = (song.artist,
                  song.album,
                  song.track,
                  song.title)
        rs = c.execute(query, values)
        return rs.fetchone() == 1

    def _insert_into_music_map(self, new_song_id, song, music_root):
        query = """
                INSERT INTO music_map
                          ( song_id
                          , location
                          , artist
                          , album
                          , track
                          , title
                          )
                     VALUES
                          ( ?
                          , ?
                          , ?
                          , ?
                          , ?
                          , ?
                          )
                """
        values = (new_song_id,
                  music_root,
                  song.orig_artist,
                  song.orig_album,
                  song.orig_track,
                  song.orig_title)

        c = self._conn.cursor()
        try:
            c.execute(query, values)
        except Exception:
            self._conn.rollback()
        finally:
            self._conn.commit()
