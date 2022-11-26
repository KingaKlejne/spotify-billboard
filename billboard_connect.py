import requests
from bs4 import BeautifulSoup


class ConnectToBillboard(BeautifulSoup):
    def __init__(self, date_input):
        super().__init__()
        URL = f"https://www.billboard.com/charts/hot-100/{date_input}"
        response = requests.get(URL)
        webpage = response.text
        soup = BeautifulSoup(webpage, "html.parser")
        self.songs = soup.select(selector="li h3", class_="c-title")
        self.artists = soup.select(selector="li span", class_="c-label")
        self.songs_list = []
        self.artists_list = []

    def get_songs(self):
        for song in self.songs[:100]:
            self.songs_list.append(song.getText().strip())
        return self.songs_list

    def get_artists(self):
        for artist in self.artists[13:]:
            if len(artist.getText().strip()) > 2 and (
                "Expand" not in artist.getText().strip()
                and "Follow" not in artist.getText().strip()
                and "NEW" not in artist.getText().strip()
                and "100" not in artist.getText().strip()
            ):
                self.artists_list.append(artist.getText().strip())
        return self.artists_list
