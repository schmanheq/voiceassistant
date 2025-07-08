import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import Credentials


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=Credentials.spotify_client_id,
    client_secret=Credentials.spotify_client_secret
))


def search_track_id(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    if not results['tracks']['items']:
        print("No track found.")
        return None
    track = results['tracks']['items'][0]
    track_id= track['id']                
    return track_id


