"""
database.py

This module handles all database interactions for the music data project.
It uses SQLite to create and manage four normalized tables:
Songs, Albums, Artists, and ArtistTopTracks.

Key Responsibilities:
- Create database schema
- Check for existing records
- Insert new albums, artists, songs, and artist top tracks

Database file: music_data.sqlite
"""
import sqlite3

DB_NAME = 'music_data.sqlite'

def create_music_db():
    """
    Initializes the SQLite database schema.

    Creates four tables:
    - Albums: id, name, release_date
    - Artists: id, name
    - Songs: id, name, rank, popularity, album_id
    - ArtistTopTracks: id, artist_id, track_name, rank

    If the tables already exist, this function does nothing.
    """
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
    Inserts a song into the Songs table if not already present.

    Args:
        name (str): Song name
        rank (int): Billboard rank
        popularity (int): Spotify popularity score
        album_id (int): Foreign key referencing the Albums table

    Returns:
        None
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
    Inserts a list of top tracks for an artist into the ArtistTopTracks table.

    Args:
        artist_id (int): Foreign key referencing the Artists table
        track_list (list of str): List of top track names (max 5)

    Returns:
        None
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
