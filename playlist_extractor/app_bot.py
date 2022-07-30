
import datetime

import _app
import _bot_reddit
import _parse_reddit
import extract_titles
import spotify_playlist

# Bot Code ========================================================================================

def construct_message(instance_comment, dict_types):

    item_type = _app.extract_list_type(instance_comment)

    # Failed for any reason
    if item_type not in dict_types.keys():
        return _app.contruct_messaged_failed(reason = "", is_supported = False)

    string_name = _app.construct_playlist_name(instance_comment)
    list_comments = _parse_reddit.extract_comment_tree(instance_comment)
    list_bodies = _parse_reddit.extract_comment_bodies(list_comments)

    if item_type == "song":
        list_items = extract_titles.extract_song_titles(list_bodies)
        if not list_items:
            return _app.contruct_messaged_failed(reason = "empty", is_supported = True)
        else:
            # TODO: BROKEN: construct an instance
            return spotify_playlist.create_playlist_spotify(string_name, list_items)
    elif item_type in ["movie", "show", "game"]:
        return _app.contruct_messaged_failed(reason = "todo", is_supported = True)

