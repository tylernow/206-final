import requests
import json
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Step 1: Authenticate using Client Credentials Flow
client_id = '58db1577ac754cc1a5a796094e2533fc'
client_secret = 'd12af79769ef40e39875ca0614f893c3'

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