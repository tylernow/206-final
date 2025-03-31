import sqlite3

DB_NAME = 'music_data.sqlite'

def create_music_db():
    """Create SQLite tables for songs, albums, artists, and top tracks if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create Albums table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            release_date TEXT
        )
    ''')

    # Create Artists table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Create Songs table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rank INTEGER UNIQUE,
            popularity INTEGER,
            album_id INTEGER,
            FOREIGN KEY (album_id) REFERENCES Albums(id)
        )
    ''')

    # Create ArtistTopTracks table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ArtistTopTracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER,
            track_name TEXT,
            rank INTEGER,
            FOREIGN KEY (artist_id) REFERENCES Artists(id)
        )
    ''')

    conn.commit()
    conn.close()

def song_rank_exists(rank):
    """
    Check if a song with a given Billboard rank already exists in the database.

    Args:
        rank (int): Billboard song ranking.

    Returns:
        bool: True if the rank exists in the Songs table, False otherwise.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Songs WHERE rank = ?", (rank,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def insert_album(name, release_date):
    """
    Insert an album into the Albums table.

    Args:
        name (str): Album name.
        release_date (str): Album release date.

    Returns:
        int: ID of the inserted or existing album.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO Albums (name, release_date) VALUES (?, ?)', (name, release_date))
    conn.commit()
    cur.execute('SELECT id FROM Albums WHERE name = ?', (name,))
    album_id = cur.fetchone()[0]
    conn.close()
    return album_id

def insert_artist(name):
    """
    Insert an artist into the Artists table.

    Args:
        name (str): Artist name.

    Returns:
        int: ID of the inserted or existing artist.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO Artists (name) VALUES (?)', (name,))
    conn.commit()
    cur.execute('SELECT id FROM Artists WHERE name = ?', (name,))
    artist_id = cur.fetchone()[0]
    conn.close()
    return artist_id

def insert_song(name, rank, popularity, album_id):
    """
    Insert a song into the Songs table.

    Args:
        name (str): Song name.
        rank (int): Billboard rank.
        popularity (int): Spotify popularity score.
        album_id (int): FK to Albums table.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT OR IGNORE INTO Songs (name, rank, popularity, album_id)
        VALUES (?, ?, ?, ?)
    ''', (name, rank, popularity, album_id))
    conn.commit()
    conn.close()

def insert_artist_top_tracks(artist_id, track_list):
    """
    Insert a list of top tracks for an artist.

    Args:
        artist_id (int): FK to Artists table.
        track_list (list): List of track names (max 5).
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for idx, track_name in enumerate(track_list):
        cur.execute('''
            INSERT OR IGNORE INTO ArtistTopTracks (artist_id, track_name, rank)
            VALUES (?, ?, ?)
        ''', (artist_id, track_name, idx + 1))
    conn.commit()
    conn.close()
