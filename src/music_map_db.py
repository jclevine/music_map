import sqlite3


if __name__ == "__main__":
    db = sqlite3.connect('music_map')

    c = db.cursor()

    # A table of all the unique individual songs
    # (with standardized sanitized names) that you know about
    c.execute("""CREATE TABLE song (song_id     INTEGER       PRIMARY KEY
                                  , artist_key  VARCHAR2(200) NOT NULL    -- The unique key
                                  , album_key   VARCHAR2(500) NOT NULL
                                  , track_key   VARCHAR2(5)   NOT NULL
                                  , title_key   VARCHAR2(500) NOT NULL)
              """)

    # Only one song
    c.execute("""ALTER TABLE song
             ADD CONSTRAINTS u_song UNIQUE INDEX (artist_key
                                                , album_key
                                                , track_key
                                                , title_key)
              """)

    # Create music_map table
    c.execute("""CREATE TABLE music_map (music_map_id INTEGER       PRIMARY KEY
                                       , song_id      INTEGER
                                       , location     VARCHAR2(100) NOT NULL    -- Root location of all the songs.
                                       , artist       VARCHAR2(200) NOT NULL    -- What the artist actually looks like in that location
                                       , album        VARCHAR2(500) NOT NULL    -- What the album actually looks like in that location
                                       , track        VARCHAR2(5)   NOT NULL    -- What the track actually looks like in that location
                                       , title        VARCHAR2(500) NOT NULL    -- What the title actually looks like in that location
                                       , FOREIGN KEY(song_id) REFERENCES song(song_id))
              """)

    # Only one song in each location
    c.execute("""ALTER TABLE music_map
             ADD CONSTRAINTS u_loc UNIQUE (artist_key
                                         , album_key
                                         , track_key
                                         , title_key
                                         , location""")

    # Index for finding a particular song in a location. Often used to see
    # if a particular song is already inserted for a location.
    c.execute("""CREATE INDEX music_map_key_idx
                           ON music_map (artist_key
                                       , album_key
                                       , track_key
                                       , title_key
                                       , location)""")

    # Index for deleting all songs for a location
    c.execute("""CREATE INDEX location_idx
                           ON music_map (location)""")

    # Create tags table
    c.execute("""CREATE TABLE music_tag (music_tag_id INTEGER PRIMARY KEY
                                       , music_map_id)""")
