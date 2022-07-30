import fuzzywuzzy
import logging
import spotipy

class SpotifyPlaylist:
    """
    User should use only constructor
    and call create_playlist_url method    
    """
    def __init__(self, cid, csec):
        self.instance_spotify = None
        self.sp_un = "374oo3vji0f3aexvb4l423n63" # ???
        self.playlist_domain = "open.spotify.com/playlist/"

        self.instance_spotify = self.create_instance_spotify(cid, csec)

    def create_instance_spotify(self, cid, csec):
        """ Calls the Spotify Credentials to construct a Spotify API instance """
        sp_uri = "http://localhost:8080"
        sp_scope = "playlist-modify-private,playlist-modify-public"
        # sp_cache = '.spotipyoauthcache'

        auth_mgr = spotipy.SpotifyOAuth(cid, csec, sp_uri, None, sp_scope, None, self.sp_un)
        instance_spotify = spotipy.Spotify(auth_manager=auth_mgr)

        return instance_spotify
    
    # Searches ====================================================================================

    def find_id_song(self, string):
        """
        Returns track id as string via the best match
        Defaults returns empty string
        """
        best_value = float('-inf')
        best_index = None
        dict_results = self.instance_spotify.search(q=string, limit=5, type="track")
        if 0 < dict_results["tracks"]["total"]:

            for index_track in range(len(dict_results["tracks"]["items"])):
                string_title = dict_results['tracks']['items'][index_track]['name']
                string_artist = dict_results['tracks']['items'][index_track]['artists'][0]['name']
                match = fuzzywuzzy.fuzz.token_set_ratio(string_title + " " + string_artist, string)
                if best_value < match:  # closer match on title/artist
                    best_value = match
                    best_index = index_track

        if 0 < best_value:
            return dict_results['tracks']['items'][best_index]['id']

        return ""

    def extract_ids_songs(self, list_string_songs):
        list_ids = []
        for string_song in list_string_songs:
            if string_song:
                string_id_track = self.find_id_song(string_song)
                if string_id_track:
                    list_ids.append(string_id_track)

        return list(set(list_ids)) # remove duplicates

    # Playlists ===================================================================================

    def get_playlist_id(self, string):
        dict_playlists = self.instance_spotify.user_playlists(self.sp_un)
        for playlist in dict_playlists["items"]:
            if playlist["name"] == string:
                return playlist['id']

        return ""

    def post_spotify_playlist(self, string_name, string_description):
        """
        Creates a Spotify playlist and yields the id 
        TODO: Check if exists and check if successfully created
        """
        response = self.instance_spotify.user_playlist_create(
            self.sp_un, 
            string_name, 
            public=True, 
            description=string_description
        )
        logging.debug(response)
        string_id_playlist = self.get_playlist_id(string_name)

        return string_id_playlist

    def populate_playlist(self, string_id_playlist, list_string_ids, batch_size = 100):
        """
        Populate a playlist based on track ids
        """
        for i in range(0, len(list_string_ids), batch_size):
            self.instance_spotify.playlist_add_items(string_id_playlist, list_string_ids[i:i+batch_size])

    def create_playlist_url(self, list_songs, string_name, string_description):
        """ 
        Public URL to access on open.spotify.com
        """
        list_ids_track = self.extract_ids_songs(list_songs)
        if not list_ids_track:
            return ""

        # API max is 100 per call
        string_id_playlist = self.post_spotify_playlist(string_name, string_description)
        self.populate_playlist(string_id_playlist, list_ids_track, 99)
        
        return self.playlist_domain + string_id_playlist

    # STDOUT ======================================================================================

    def markdown_message(self, url):
        return f"[Spotify playlist]({url}) of song(s) in this comment thread."


# Usage ===========================================================================================
def create_playlist_spotify(instance_playlist, string_name, list_items, tag = ""):
    url_playlist = instance_playlist.create_playlist_url(
        list_items,
        string_name,
        f"Playlist from songs extracted from {tag}"
    )
    if not url_playlist:
        return "Playlist is empty"

    return instance_playlist.markdown_message(url_playlist)