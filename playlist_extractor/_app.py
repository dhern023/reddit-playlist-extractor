import datetime
import pathlib
import re

# Put in file
dict_types = {}
dict_types["song"] = ["song", "music", "audio"]
dict_types["movie"] = ["movie", "film"]
dict_types["show"] = ["show", "TV"]
dict_types["game"] = ["game"]

# Helpers =========================================================================================
def find_filepath(fname):
    """
    Hardcoded to looking in current working directory
    Defaults to empty string
    """
    list_files = pathlib.Path.cwd().glob('*')
    for file in list_files:
        if file.name == fname:
            return str(file)
    
    return ""

def check_substring(string, list_words):
    return any(keyword in string for keyword in list_words)

# Extraction ======================================================================================

def extract_match_first(regex, string):
    list_matches = re.findall(regex, string)
    if list_matches:
        return list_matches[0]
    return ""

def extract_list_type(instance_comment):
    bodytext = instance_comment.body.lower()
    for key, list_keywords in dict_types.items():
        if check_substring(bodytext, list_keywords):
            return key

    regex_in_brackets = r"(?<=\[).+(?=\])"
    match = extract_match_first(regex_in_brackets, bodytext)
    if match != "":
        return match

    bodytext = instance_comment.submission.title
    for key, list_keywords in dict_types.items():
        if check_substring(bodytext, list_keywords):
            return key

    return ""

# Playlists =======================================================================================

def create_playlist_imdb(string_name, list_items):
    return

def construct_playlist_name(instance_comment = None):
    if instance_comment:
        return f"Reddit Thread {instance_comment.submission.id} {datetime.datetime.today()}"
    return f"Reddit Parsed: {datetime.datetime.today()}"

def private_message_list(instance_bot, instance_comment, url):
    sub_url = instance_comment.submission.url
    subject = "Your {instance_bot.string_username_bot} results"
    body = f"""
        [Bot Reponse]
        Someone requested a list items from post:\n\t {sub_url}\n
        Here's your link!: {url}
        Note: DM'ing in case subreddit forbids bot activity.
    """
    instance_bot.send_private_message(instance_comment, subject, body)


def contruct_messaged_failed(reason, is_supported):

    if is_supported:
        if reason == "empty":
            return "Failed to find items"

        if reason == "todo":
            return "In development (stay tuned!)"

    return "No supported list type provided"