"""
main.py

This script serves as the primary entry point for populating the `music_data.sqlite` database
with song and artist information from the Billboard Hot 100 and Spotify API.

Steps:
1. Initializes the database if it doesn't exist.
2. Scrapes the Billboard Hot 100 chart for the top 100 songs.
3. Filters out songs already present in the database.
4. Fetches Spotify metadata for each new song.
5. Adds new songs, albums, artists, and top tracks into the SQLite database.
6. Limits the total number of new songs to 25 and top artist tracks to 25 per run.

To populate the full Top 100, run this script multiple times.
"""

from billboard import top_hundred_songs
from spotify_data import fetch_spotify_data
from database import (
    create_music_db,
    insert_album,
    insert_artist,
    insert_song,
    insert_artist_top_tracks,
    song_rank_exists
)

# Step 1: Initialize the database and create tables (non-destructive)
create_music_db()


# Step 2: Get Billboard Top 100 songs
billboard_data = top_hundred_songs()

# Step 3: Filter out songs already in the database
unprocessed_data = {}
for name, info in billboard_data.items():
    if not song_rank_exists(info['ranking']):
        unprocessed_data[name] = info
    if len(unprocessed_data) == 25:
        break

if not unprocessed_data:
    print("✅ All 100 songs have already been processed.")
    exit()

# Step 3: Get Spotify data for the next 25 unprocessed songs
song_db, artist_db = fetch_spotify_data(unprocessed_data, limit=25)


# Step 5: Insert song and artist data into the database
new_songs_added = 0
max_top_tracks = 25
top_tracks_added = 0

for rank, song in song_db.items():
    # Only insert if this song rank isn't already in the database
    if not song_rank_exists(rank):
        album_id = insert_album(song['album'], song['album_release_date'])
        insert_song(song['song_name'], rank, song['popularity'], album_id)
        new_songs_added += 1

        for artist_name in song['artists']:
            artist_id = insert_artist(artist_name)

            # Only insert top tracks if limit hasn't been reached
            if artist_name in artist_db and top_tracks_added < max_top_tracks:
                remaining = max_top_tracks - top_tracks_added
                trimmed_tracks = artist_db[artist_name][:remaining]
                insert_artist_top_tracks(artist_id, trimmed_tracks)
                top_tracks_added += len(trimmed_tracks)

            if top_tracks_added >= max_top_tracks:
                break
    if top_tracks_added >= max_top_tracks:
        break

print(f"\n✅ Successfully processed and inserted {new_songs_added} new songs and {top_tracks_added} artist top tracks into the database.\n")
