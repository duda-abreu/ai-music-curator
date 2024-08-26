# scripts/spotify_api.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurações do cliente Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2720b05d29404b55a21d2319ddf01526",
                                                           client_secret="92774db7814043b6b1922a4878b383c1"))

def get_track_info(track_id):
    track = sp.track(track_id)
    return {
        "titulo": track["name"],
        "artista": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "genero": sp.artist(track["artists"][0]["id"])["genres"]
    }

def search_tracks(query):
    results = sp.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']
    return [{
        "id": track["id"],
        "titulo": track["name"],
        "artista": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "genero": sp.artist(track["artists"][0]["id"])["genres"]
    } for track in tracks]
