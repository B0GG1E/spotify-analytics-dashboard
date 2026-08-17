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
