import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# API references
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
APP_REDIRECT_URI = "http://example.com"


class ConnectToSpotify:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=APP_REDIRECT_URI,
                cache_path="../.cache",
                scope=["playlist-modify-private", "playlist-read-private"],
            )
        )
        self.user_id = self.sp.current_user()["id"]
        self.tracks_ids = []

    def create_track_list(self, songs_list, artists_list) -> list:
        for i in range(100):
            sp_song_name = self.sp.search(
                q=f"track: {songs_list[i]} artist: {artists_list[i]}",
                limit=1,
                type="track",
            )["tracks"]["items"][0]["name"]
            sp_song_name = sp_song_name.strip().replace("’", "'")
            sp_artist_name = self.sp.search(
                q=f"track: {songs_list[i]} artist: {artists_list[i]}",
                limit=1,
                type="track",
            )["tracks"]["items"][0]["artists"][0]["name"]
            sp_artist_name.strip().replace("’", "'")
            songs_list[i] = songs_list[i].strip()
            artists_list[i] = artists_list[i].strip()
            if (
                songs_list[i] not in sp_song_name
                and artists_list[i] not in sp_artist_name
            ):
                # print(
                #     f"Instead of {artists_list[i]}: "
                #     f'"{songs_list[i]}", only {sp_artist_name}: '
                #     f'"{sp_song_name}" was found, not added to playlist'
                # )
                pass
            else:
                self.tracks_ids.append(
                    self.sp.search(
                        q=f"track: {songs_list[i]} artist: {artists_list[i]}",
                        limit=1,
                        type="track",
                    )["tracks"]["items"][0]["id"]
                )
                # print(
                #     f"For {artists_list[i]}: "
                #     f'"{songs_list[i]}", found {sp_artist_name}: '
                #     f'"{sp_song_name}" and added to playlist'
                # )
        return self.tracks_ids

    def create_playlist(self, date_input):
        self.sp.user_playlist_create(user=self.user_id,
                                     name=date_input,
                                     public=False)
        if self.sp.user_playlists(user=self.user_id
                                  )["items"][0]["name"] == date_input:
            playlist_id = self.sp.user_playlists(user=self.user_id
                                                 )["items"][0]["id"]
            self.sp.playlist_add_items(playlist_id=playlist_id,
                                       items=self.tracks_ids)

