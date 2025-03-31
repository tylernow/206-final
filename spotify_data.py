import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Load Spotify credentials
def load_spotify_credentials(filepath='spotify_credentials.txt'):
    credentials = {}
    with open(filepath, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key.strip()] = value.strip()
    return credentials

# Initialize Spotify client
def get_spotify_client():
    creds = load_spotify_credentials()
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=creds.get('client_id'),
        client_secret=creds.get('client_secret')
    ))

# Get Spotify data for top Billboard songs
def fetch_spotify_data(billboard_data, limit=25):
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
