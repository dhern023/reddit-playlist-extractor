import itertools
import logging
import re

from transformers import LONGFORMER_PRETRAINED_MODEL_ARCHIVE_LIST

import _clean_text
import _parse_reddit
import _parse_youtube

# Helpers =========================================================================================

def count_chars_capital(string):
    return sum(map(str.isupper, string))

def criteria_title_case(string):
    return string[0].isupper()

def criteria_within_quotes(string):
    regex_quotes = r"(?<=\“).*(?=\”)"
    return len(re.findall(regex_quotes, string)) > 0

def extract_sequences_via_criteria(string, key_criteria, keep_others = False):
    """
    Groups based on the given key_criteria
    key_criteria must be single-valued and return bool
    Keeps non key groups as an option
    e.g.,
    lambda x: x[0].isUpper()
    "Song TItle by Song Artist" -> ["Song Title", "by", "Song Artist"]
    """
    list_sequences = []
    for key, group in itertools.groupby(string.split(), key_criteria):
        if key:
            sequence = ' '.join(list(group))
            list_sequences.append(sequence)
        elif not key and keep_others:
            sequence = ' '.join(list(group))
            list_sequences.append(sequence)

    return list_sequences

def check_grammar_title(string):
    """
    TODO: Weird function name
    Song Title - Song Artist
    Song Title by Song Artist
    """
    list_triggers = ["-", "by", "from", "is so", "is a", "is my", "has been my", ":"]
    string_p = string.lower()
    return any(trigger in string_p for trigger in list_triggers)

def check_quotes(string):
    list_triggers = ["“", "’", "”", '"']
    return any(trigger in string for trigger in list_triggers)

def clean_string(string):
    string_p = string[::]

    string_p = string_p.replace("\\n", "\n")

    for _ in _parse_reddit.list_regex_replies:
        string_p = re.sub(_, " ", string_p)

    for _ in _parse_reddit.list_regex_non_ascii:
        string_p = re.sub(_, "", string_p)

    for _ in _parse_reddit.list_strings:
        string_p = string_p.replace(_, " ")

    string_p = _clean_text.normalize_non_ascii(string_p)

    return string_p.strip()

def extract_title_from_grammar(string, keep_others = True):
    list_sequences = extract_sequences_via_criteria(
        string,
        criteria_title_case,
        keep_others=keep_others)
    string_title = " ".join(list_sequences)
    logging.debug(f"Grammar: {string} : {string_title}")

    return string_title

def extract_title_from_quotes(string):
    list_sequences = extract_sequences_via_criteria(
        string,
        criteria_within_quotes,
        keep_others=True)
    string_title = " ".join(list_sequences)
    logging.debug(f"Quotes: {string} : {string_title}")

    return string_title

def extract_song_titles_in_line(string):
    list_titles = []

    if check_grammar_title(string):
        title = extract_title_from_grammar(string)
        list_titles.append(title)

    # Song title in quotes
    if check_quotes(string):
        title = extract_title_from_quotes(string)
        list_titles.append(title)

        # String artist might be missed
        if check_grammar_title(title):
            title = extract_title_from_grammar(title, keep_others=False)
            list_titles.append(title)
        
    return list_titles

def extract_titles_from_youtube(string):
    list_urls = _parse_youtube.extractor.find_urls(string.replace("\n", " "))
    list_urls_youtube = _parse_youtube.extract_youtube_urls(list_urls)
    list_youtube_titles = _parse_youtube.extract_youtube_titles(list_urls_youtube)

    return list_youtube_titles

def extract_song_titles(list_strings_raw):
    list_titles = []

    # Extract from youtube
    string_all = " ".join(list_strings_raw)
    string_all_p = clean_string(string_all)

    list_titles_youtube = extract_titles_from_youtube(string_all_p)
    list_titles.extend(list_titles_youtube)

    for text in string_all_p.splitlines():

        if not text.strip():
            continue

        # Usual song name & artist format
        list_sequences = extract_sequences_via_criteria(
            text,
            criteria_title_case,
            keep_others=False
        )
        for sequence in list_sequences:
            if sequence.strip() and 1 < count_chars_capital(sequence.strip()):
                logging.debug(f"TitleCase: {sequence}")
                list_titles.append(sequence)

        list_split_lines = re.split("[;,.]", text) # multiple listings
        for line in list_split_lines:
            if not line.strip():
                continue

            logging.debug(f"Raw: {line}")
            list_titles_line = extract_song_titles_in_line(line)
            list_titles.extend(list_titles_line)

    list_titles = sorted(set(list_titles))

    return list_titles

if __name__ == "__main__":
    s = "I don\xe2\x80\x99t know.\npermalink\nembed\nsave\nreport\ngive award\nreply\n"
    clean_string(s)