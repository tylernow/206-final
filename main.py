import requests
import json
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Function to retrieve the spotify id and api key
def load_spotify_credentials(filepath='spotify_credentials.txt'):
    credentials = {}
    with open(filepath, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key.strip()] = value.strip()
    return credentials


# Step 1: Authenticate using Client Credentials Flow
creds = load_spotify_credentials()
client_id = creds.get('client_id')
client_secret = creds.get('client_secret')

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Step 2: Get track info by ID (example: "3n3Ppam7vgaVa1iaRUc9Lp" is a valid track ID for Eminem's "Lose Yourself")
track_id = '3n3Ppam7vgaVa1iaRUc9Lp'
track = sp.track(track_id)

# Step 3: Print info
print("Track Name:", track['name'])
print("Artist:", track['artists'][0]['name'])
print("Album:", track['album']['name'])
print("Duration (ms):", track['duration_ms'])