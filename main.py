import requests
import spotipy
from bs4 import BeautifulSoup
import os
import re
from spotipy.oauth2 import SpotifyOAuth

# Input from user
date_input = input(
    "Which year do you want to travel to? "
    "Type the date in this format YYYY-MM-DD: "
)

# Check if input has correct format
regex = r'(?:1958|1959|19[6-9][0-9]|20[01][0-9]|2022)' \
        r'-(?:0[1-9]|1[012])-(?:0[1-9]|[12][0-9]|3[01])'
date_match = re.compile(regex).match

if date_match(date_input) is None:
    print("Wrong format of date provided!")

else:
    # API references
    SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
    APP_REDIRECT_URI = "http://example.com"
    URL = f"https://www.billboard.com/charts/hot-100/{date_input}"

    # List of songs and artists from billboard site
    response = requests.get(URL)
    webpage = response.text
    soup = BeautifulSoup(webpage, "html.parser")
    songs = soup.select(selector="li h3", class_="c-title")
    songs_list = [song.getText().strip() for song in songs[:100]]
    artists = soup.select(selector="li span", class_="c-label")
    artists_list = [
        artist.getText().strip()
        for artist in artists[13:]
        if len(artist.getText().strip()) > 2 and (
           "Expand" not in artist.getText().strip() and
           "Follow" not in artist.getText().strip() and
           "NEW" not in artist.getText().strip() and
           "100" not in artist.getText().strip()
        )]

    # Spotify credentials
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=APP_REDIRECT_URI,
            cache_path=".cache",
            scope=["playlist-modify-private", "playlist-read-private"],
        )
    )

    user_id = sp.current_user()["id"]

    # Manual Checks
    # song = "Living In Danger"
    # artist = "Ace Of Base"
    # print(sp.search(q=f"track: {song} artist: {artist}",
    #                 limit=1, type="track")["tracks"][
    #         "items"][0]["name"])
    # print(sp.search(q=f"track: {song} artist: {artist}",
    #                 limit=1, type="track")["tracks"][
    #         "items"][0]["artists"][0]["name"])
    # print(sp.search(q=f"track: {song} artist: {artist}",
    #                 limit=1, type="track")["tracks"][
    #         "items"][0]["id"])

    # List for Track IDs
    # tracks_ids = [sp.search(q=f"{song} {year}",
    #                         limit=1, type="track")["tracks"][
    #                   "items"][0]["id"]
    #               for song in songs_list]

    tracks_ids = []
    for i in range(100):
        sp_song_name = sp.search(
            q=f"track: {songs_list[i]} artist: {artists_list[i]}",
            limit=1, type="track"
        )["tracks"]["items"][0]["name"]
        sp_song_name = sp_song_name.strip().replace("’", "'")
        sp_artist_name = sp.search(
            q=f"track: {songs_list[i]} artist: {artists_list[i]}",
            limit=1, type="track"
        )["tracks"]["items"][0]["artists"][0]["name"]
        sp_artist_name.strip().replace("’", "'")
        songs_list[i] = songs_list[i].strip()
        artists_list[i] = artists_list[i].strip()
        if songs_list[i] not in sp_song_name and \
                artists_list[i] not in sp_artist_name:
            print(
                f'Instead of {artists_list[i]}: '
                f'"{songs_list[i]}", only {sp_artist_name}: '
                f'"{sp_song_name}" was found, not added to playlist'
            )
        else:
            tracks_ids.append(
                sp.search(
                    q=f"track: {songs_list[i]} artist: {artists_list[i]}",
                    limit=1,
                    type="track",
                )["tracks"]["items"][0]["id"]
            )
            print(
                f'For {artists_list[i]}: '
                f'"{songs_list[i]}", found {sp_artist_name}: '
                f'"{sp_song_name}" and added to playlist'
            )

    # Spotify Playlist creation
    sp.user_playlist_create(user=user_id, name=date_input, public=False)
    if sp.user_playlists(user=user_id)["items"][0]["name"] == date_input:
        playlist_id = sp.user_playlists(user=user_id)["items"][0]["id"]
        sp.playlist_add_items(playlist_id=playlist_id, items=tracks_ids)
