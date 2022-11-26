from billboard_connect import ConnectToBillboard
from spotify_connect import ConnectToSpotify
from user_input import get_input, check_date

date = get_input()
if not check_date(date):
    print("Wrong format of date provided!")

else:
    bi = ConnectToBillboard(date)
    sp = ConnectToSpotify()
    sp.create_track_list(bi.get_songs(), bi.get_artists())
    sp.create_playlist(date)
