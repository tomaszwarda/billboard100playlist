import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/[DATE]/"
SPOTIFY_ID = "your-spotify-client-id"
SPOTIFY_SECRET = "your-spotify-client-secret"
URI = "http://example.com"
SPOTIFY_TOKEN = "your-token"
song_id_list = []
missing_songs = 0

date = input("Witch time you want to listen (YYYY-MM-DD)?\n")

URL = URL.replace("[DATE]", date)

site = BeautifulSoup(requests.get(url=URL).text, "html.parser")

song_titles = site.find_all(name="h3", class_="a-no-trucate", id="title-of-a-story")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URI,
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path=SPOTIFY_TOKEN
    )
)
user_id = sp.current_user()["id"]

for song in song_titles:
    song = song.text
    try:
        song_spotify = sp.search(q=f"track: {song}")
        song_spotify_id = song_spotify["tracks"]["items"][0]["uri"]
        song_id_list.append(song_spotify_id)
    except IndexError:
        print(f"no song on spotify called: {song}")
        missing_songs += 1

playlist = sp.user_playlist_create(user=user_id, name=f"{date} hits", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_id_list)

print(f"\n\nThere are {missing_songs} missing songs from 100.")
print(f'Your playlist "{date} hits" was added to spotify.')
