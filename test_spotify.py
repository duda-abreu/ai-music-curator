import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurações do cliente Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2720b05d29404b55a21d2319ddf01526",
                                                            client_secret="92774db7814043b6b1922a4878b383c1"))

# Testar a busca de uma música
result = sp.search(q="Popular", type='track', limit=1)
tracks = result['tracks']['items']
if tracks:
    track = tracks[0]
    print(f"Title: {track['name']}, Artist: {track['artists'][0]['name']}, Album: {track['album']['name']}")
else:
    print("No tracks found.")