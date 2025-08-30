import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Define Credentials

CLIENT_ID = 'f7a3da5585f94d0ea3d1d453b0296d0f'
CLIENT_SECRET = 'e1cc363ba74b44e19326e70a3c3b9b71'
REDIRECT_URI = 'http://localhost:8080'

SCOPE = 'user-library-read user-top-read playlist-read-private'


sp=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= CLIENT_ID, client_secret= CLIENT_SECRET, redirect_uri= REDIRECT_URI, scope= SCOPE))

# Fetch user's top tracks

def get_top_tracks(sp,
time_range='medium_term', limit=10):
    results = sp.current_user_top_tracks(time_range = time_range, limit=limit)
    return [track['name'] for track in 
results['items']]

# Fetch user's top artists

def get_top_artists(sp,
time_range='medium_term', limit=10):
    results= sp.current_user_top_artists(time_range = time_range, limit=limit)
    return [artist['name'] for artist in 
results['items']]

# Fetch Audio features

def get_track_features(sp,track_id):
    features = sp.audio_features([track_id])
    return features[0] if features else None

#Example usage

top_tracks = get_top_tracks(sp)
top_artists = get_top_artists(sp)

print("Top Tracks:", top_tracks)
print("Top Artists:", top_artists)

























































