"""
spotify_data.py

This module connects to the Spotify Web API using Spotipy and gathers metadata
for Billboard songs and artists.

Key Functions:
- Load Spotify API credentials from a file
- Authenticate with Spotify using Client Credentials Flow
- Fetch metadata for Billboard songs (album info, popularity)
- Fetch top 5 tracks for each unique artist
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Load Spotify credentials
def load_spotify_credentials(filepath='spotify_credentials.txt'):
    """
    Loads Spotify API credentials from a local text file.

    Args:
        filepath (str): Path to the file containing 'client_id' and 'client_secret'

    Returns:
        dict: A dictionary with Spotify credentials
    """
    credentials = {}
    with open(filepath, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key.strip()] = value.strip()
    return credentials

def get_spotify_client():
    """
     Authenticates with the Spotify API and returns a Spotipy client.

    Uses Client Credentials Flow.

    Returns:
        spotipy.Spotify: Authenticated Spotify API client
    """
    creds = load_spotify_credentials()
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=creds.get('client_id'),
        client_secret=creds.get('client_secret')
    ))

def fetch_spotify_data(billboard_data, limit=25):
    """
    Queries Spotify for song metadata and artist top tracks.

    Args:
        billboard_data (dict): Dictionary of Billboard song names and info (ranking, artists)
        limit (int): Max number of songs to process (default: 25)

    Returns:
        tuple:
            song_db (dict): Maps rank to Spotify metadata for each song
            artist_db (dict): Maps artist name to a list of their top 5 tracks
    """
    sp = get_spotify_client()
    song_db = {}
    artist_db = {}
    seen_artists = set()

    count = 0
    for song_name, info in billboard_data.items():
        if count >= limit:
            break

        ranking = info['ranking']
        artists = info['artists']
        query = f"{song_name} {artists[0]}"
        result = sp.search(q=query, type='track', limit=1)

        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            song_db[ranking] = {
                'song_name': song_name,
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'album_release_date': track['album']['release_date'],
                'popularity': track['popularity']
            }

            for artist in track['artists']:
                artist_name = artist['name']
                artist_id = artist['id']

                if artist_name not in seen_artists:
                    seen_artists.add(artist_name)
                    top_tracks = sp.artist_top_tracks(artist_id)['tracks'][:5]
                    artist_db[artist_name] = [t['name'] for t in top_tracks]

        count += 1
        time.sleep(0.1)

    return song_db, artist_db
