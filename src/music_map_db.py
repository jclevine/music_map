import sqlite3


if __name__ == "__main__":
    db = sqlite3.connect('music_map')

    c = db.cursor()

    #===========================================================================
    # SONG TABLE
    # A table of all the unique individual songs
    # (with standardized sanitized names) that you know about
    #===========================================================================
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

    #===========================================================================
    # MUSIC MAP TABLE
    # A table that maps a song to what it actually looks like in a particular location
    #===========================================================================
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
             ADD CONSTRAINTS u_loc UNIQUE (song_id
                                         , location
                                         , artist
                                         , album
                                         , track
                                         , title)
              """)

    # Index for finding a particular song in a location. Often used to see
    # if a particular song is already inserted for a location.
    c.execute("""CREATE INDEX song_loc_idx
                           ON music_map (song_id
                                       , location)
              """)

    # Index for deleting all songs for a location
    c.execute("""CREATE INDEX location_idx
                           ON music_map (location)
              """)

    #===========================================================================
    # TAG TABLE
    # Maps a song to a tag
    #===========================================================================
    c.execute("""CREATE TABLE music_tag (music_tag_id INTEGER PRIMARY KEY
                                       , song_id      INTEGER
                                       , tag          VARCHAR2(50)
                                       , FOREIGN KEY(song_id) REFERENCES song(song_id))
              """)

    # Only only one row per tag-song. However, a song can have many tags.
    c.execute("""ALTER TABLE music_tag
             ADD CONSTRAINTS u_tag UNIQUE (song_id
                                         , tag)
              """)

    # Index for finding all songs for a tag
    c.execute("""CREATE INDEX tag_idx
                           ON music_tag (tag)
              """)

    # Index for finding all tags for a song
    c.execute("""CREATE INDEX tag_idx
                           ON music_tag (song_id)
              """)

    #===========================================================================
    # RATINGS TABLE
    # Maps a song to a rating
    #===========================================================================
    c.execute("""CREATE TABLE music_rating (music_rating_id INTEGER PRIMARY KEY
                                          , song_id         INTEGER
                                          , rating          INTEGER              -- 1 = never. 2 = sometimes. 3 = always.
                                          , FOREIGN KEY(song_id) REFERENCES song(song_id))
              """)

    # Only only one rating per song.
    c.execute("""ALTER TABLE music_rating
             ADD CONSTRAINTS u_rating UNIQUE (song_id)
              """)

    # Index for finding all songs for a rating
    c.execute("""CREATE INDEX rating_idx
                           ON music_tag (rating)
              """)
