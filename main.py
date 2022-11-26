import re

from billboard_connect import ConnectToBillboard
from spotify_connect import ConnectToSpotify

# Input from user
date_input = input(
    "Which year do you want to travel to? "
    "Type the date in this format YYYY-MM-DD: "
)


# Check if input has correct format
def check_date(date: str):
    regex = r'(?:1958|1959|19[6-9][0-9]|20[01][0-9]|2022)' \
            r'-(?:0[1-9]|1[012])-(?:0[1-9]|[12][0-9]|3[01])'
    date_match = re.compile(regex).match
    return date_match(date) is not None


if not check_date(date_input):
    print("Wrong format of date provided!")

else:
    bi = ConnectToBillboard(date_input)
    sp = ConnectToSpotify()
    sp.create_track_list(bi.get_songs(), bi.get_artists())
    sp.create_playlist(date_input)
