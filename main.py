from resources.billboard_connect import ConnectToBillboard
from resources.spotify_connect import ConnectToSpotify
from resources.user_input import check_date, get_input

date = get_input()
if not check_date(date):
    print("Wrong format of date provided!")

else:
    bi = ConnectToBillboard(date)
    sp = ConnectToSpotify()
    sp.create_track_list(bi.get_songs(), bi.get_artists())
    sp.create_playlist(date)
