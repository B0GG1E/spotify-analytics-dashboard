import sqlite3

connection = sqlite3.connect("spotify_data.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS artists(id TEXT PRIMARY KEY, name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS albums(id TEXT PRIMARY KEY, name TEXT, release_date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tracks(id TEXT PRIMARY KEY, name TEXT, duration_ms INTEGER, album_id TEXT, FOREIGN KEY (album_id) REFERENCES albums(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS track_artists(track_id TEXT, artist_id TEXT, FOREIGN KEY (track_id) REFERENCES tracks(id), FOREIGN KEY (artist_id) REFERENCES artists(id), PRIMARY KEY (track_id, artist_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time_range TEXT, UNIQUE (date, time_range))")
cursor.execute("CREATE TABLE IF NOT EXISTS snapshot_tracks(snapshot_id INTEGER, track_id TEXT, rank INTEGER, PRIMARY KEY (snapshot_id, track_id), FOREIGN KEY (snapshot_id) REFERENCES snapshots(id), FOREIGN KEY (track_id) REFERENCES tracks(id))")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

def insert_artist(cursor, artist_id, name):
    cursor.execute("INSERT OR IGNORE INTO artists (id, name) VALUES (?, ?)", (artist_id, name))

def insert_album(cursor, album_id, name, release_date):
    cursor.execute("INSERT OR IGNORE INTO albums (id, name, release_date) VALUES (?, ?, ?)", (album_id, name, release_date))

def insert_track(cursor, track_id, name, duration_ms, album_id):
    cursor.execute("INSERT OR IGNORE INTO tracks (id, name, duration_ms, album_id) VALUES (?, ?, ?, ?)", (track_id, name, duration_ms, album_id))

def insert_track_artists(cursor, track_id, artists):
    """artists should be a list of artist dictionaries, each with an 'id' key, from the Spotipy API."""
    for artist in artists:
        artist_id = artist["id"]
        cursor.execute("INSERT OR IGNORE INTO track_artists (track_id, artist_id) VALUES (?, ?)", (track_id, artist_id))

def insert_snapshot(connection, cursor, date, time_range):
    cursor.execute("INSERT OR IGNORE INTO snapshots (date, time_range) VALUES (?, ?)", (date, time_range))
    connection.commit()
    cursor.execute("SELECT id FROM snapshots WHERE date = ? and time_range = ?", (date, time_range))
    snapshot_id = cursor.fetchone()[0]
    return snapshot_id

def insert_snapshot_tracks(connection, cursor, snapshot_id, tracks):
    """tracks should be a list of track dictionaries from the Spotipy API."""
    for rank, track in enumerate(tracks, start=1):
        track_id = track["id"]
        cursor.execute("INSERT OR IGNORE INTO snapshot_tracks (snapshot_id, track_id, rank) VALUES (?, ?, ?)", (snapshot_id, track_id, rank))