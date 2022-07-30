"""
Give it a reddit URL and out comes the list of songs
"""
import click
import logging
import requests_html
import pathlib
# import praw

logging.basicConfig(filename="cli.log", level = logging.INFO)

import _app
import _clean_text
import spotify_playlist
import _parse_reddit
import extract_titles

@click.group(chain=True)
def cli():
    pass

@cli.command()
@click.option('--spotify-user', prompt=True)
@click.option('--spotify-password', prompt=True)
def get_playlist_instance(spotify_user, spotify_password):
    return spotify_playlist.SpotifyPlaylist(spotify_user, spotify_password)

def convert_url_to_old_reddit(url):
    index_subreddit = url.find("/r/")
    return "https://old.reddit.com" + url[index_subreddit:]

@cli.command()
@click.option('--url', help="Reddit URL", prompt=True)
def get_url(url):
    return convert_url_to_old_reddit(url)
    # return url



def export_list(fname, iterable):
    with open(fname, 'w') as file:
        for i in iterable:
            line = _clean_text.normalize_non_ascii(i)
            file.write(line + "\n")

def import_list(fname):
    list_lines = []
    with open(fname, 'r') as file:
        for line in file:
            list_lines.append(line)

    return list_lines

def extract_bodies_via_raw_html():
    session = requests_html.HTMLSession()
    url = get_url(standalone_mode=False)
    response = session.get(url)
    while not response.ok:
        url = get_url(standalone_mode=False)
        response = session.get(url)

    list_elements = list(set([element for element in response.html.find('div') if 'thing' in str(element)]))
    list_bodies = [element.text for element in list_elements ]

    return list_bodies, url

def extract_bodies_via_api():
    user_agent = f"Comment Extraction (by PlaylistExtractor)"
    instance_reddit = praw.Reddit(
        user_agent=user_agent,
        username="PlaylistExtractor"
    )

    list_bodies = _parse_reddit.extract_reddit_comments(url, instance_reddit)
    while not list_bodies:
        url = get_url(standalone_mode=False)
        list_bodies = _parse_reddit.extract_reddit_comments(url, instance_reddit)

    return list_bodies, url

if __name__ == "__main__":

    dir_out = pathlib.Path.cwd() / 'out'
    dir_out.mkdir(exist_ok=True, parents=True)

    # list_bodies, url = extract_bodies_via_api()
    list_bodies, url = extract_bodies_via_raw_html()

    fname_bodies = dir_out / 'bodies.txt'
    list_bodies = import_list(fname_bodies)
    export_list(fname_bodies, list_bodies)

    list_songs = extract_titles.extract_song_titles(list_bodies)
    fname_songs = dir_out / 'songs.txt'
    export_list(fname_songs, list_songs)

    # string_name = _app.construct_playlist_name()
    # instance_playlist = get_playlist_instance(standalone_mode=False)
    # messsage = spotify_playlist.create_playlist_spotify(instance_playlist, string_name, list_songs, tag = url)