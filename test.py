import unittest
from spotify_connect import ConnectToSpotify
from billboard_connect import ConnectToBillboard
from user_input import check_date
from reference_lists import tracks_ids_list, songs_name_list, artists_name_list


class TestInputs(unittest.TestCase):
    def test_date_format(self):
        self.assertEqual(check_date("2022-11-26"), True)
        self.assertEqual(check_date("2022"), False)
        self.assertEqual(check_date("abc"), False)
        self.assertEqual(check_date("1"), False)
        self.assertEqual(check_date("12"), False)


class TestBillboardConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[INFO] Setting up Billboard Connection...")
        cls.bi = ConnectToBillboard("2022-11-26")
        cls.expected_songs = cls.bi.get_songs()
        cls.expected_artists = cls.bi.get_artists()

    def test_get_songs(self):
        self.assertEqual(type(songs_name_list), type(self.expected_songs))
        self.assertCountEqual(songs_name_list, self.expected_songs)
        self.assertListEqual(songs_name_list, self.expected_songs)

    def test_get_artists(self):
        self.assertEqual(type(artists_name_list), type(self.expected_artists))
        self.assertCountEqual(artists_name_list, self.expected_artists)
        self.assertListEqual(artists_name_list, self.expected_artists)


class TestSpotifyConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[INFO] Setting up Spotify Connection...")
        cls.sp = ConnectToSpotify()
        cls.bi = ConnectToBillboard("2022-11-26")
        cls.expected_tracks_ids = cls.sp.create_track_list(
            cls.bi.get_songs(), cls.bi.get_artists()
        )

    def test_spotify_connection(self):
        self.assertEqual(type(self.expected_tracks_ids), type(tracks_ids_list))
        self.assertEqual(self.expected_tracks_ids, tracks_ids_list)
        self.assertEqual(type(self.expected_tracks_ids), list)

