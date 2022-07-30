import pytest
import extract_titles

cases_title_sequences = (
    ("John Walker Smith is currently in New York", extract_titles.criteria_title_case, False, ["John Walker Smith", "New York"]),
    ("John Walker Smith is currently in New York", extract_titles.criteria_title_case, True, ["John Walker Smith", "is currently in", "New York"]),
    ("Song Title by Song Artist", extract_titles.criteria_title_case, False, ["Song Title", "Song Artist"]),
    ("Song Title by Song Artist", extract_titles.criteria_title_case, True, ["Song Title", "by", "Song Artist"]),
    ("Song Title by Song Artist;Song Title by Song Artist;Song Title by Song Artist;", extract_titles.criteria_title_case, False, ["Song Title", "Song Artist;Song Title", "Song Artist;Song Title", "Song Artist;"]),
)

@pytest.mark.parametrize('string, key_criteria, keep_others, expected', cases_title_sequences)
def test_title_sequences(string, key_criteria, keep_others, expected):
    assert extract_titles.extract_sequences_via_criteria(string, key_criteria, keep_others) == expected

cases_quotes = (
    ("“Don’t You (Forget About Me)” - Simple Minds", True),
    ("“Dont You (Forget About Me)” - Simple Minds", True),
    ("Don’t You (Forget About Me) - Simple Minds", True),
    ("Dont You (Forget About Me) - Simple Minds", False),
    ("The Bruce Dickinson", False),
    ('"The Bruce Dickinson"', True),    
)

@pytest.mark.parametrize('string, expected', cases_quotes)
def test_check_quotes(string, expected):
    assert extract_titles.check_quotes(string) == expected

cases_candidate_title = (
    ("Blood On The Tracks is a masterpiece", True),
    ("No One's Gonna Love You More has been my jam since last Wednesday", True),
    ("listen to it every morning and it starts the day right", False),
)

@pytest.mark.parametrize('string, expected', cases_candidate_title)
def test_check_grammar_title(string, expected):
    assert extract_titles.check_grammar_title(string) == expected

cases_clean_youtube = (
    ("load more comments\xc2\xa0(1 reply)", ""),
    (" load more comments\xc2\xa0(1 reply)", ""),
    ("Let\xe2\x80\x99s", "Lets"),
    ("It\\xe2\\x80\\x99s", "Its"),
    ("[\xe2\x80\x93]ivumb 48 points49 points50 points 1 day ago\xc2\xa0(1 child)", ""),
    ("Don\xe2\x80\x99t Stop Believin\xe2\x80\x99", "Dont Stop Believin"),
    ("[\xe2\x80\x93]EllieC130 27690Answer Link2768 points2769 points2770 points 1 day ago3\xc2\xa0(227 children)\nSeason of The Witch by Donovan.", "Season of The Witch by Donovan."),
    ("I don\xe2\x80\x99t know.\npermalink\nembed\nsave\nreport\ngive award\nreply\n", "I dont know."),
    ("[\xe2\x80\x93] Blah Blah (14 children) RANDOM TEXT load more comments\xc2\xa0(14 replies)\n[\xe2\x80\x93] RANDOM TEXT (25 children)", "RANDOM TEXT"),
)

@pytest.mark.parametrize('string, expected', cases_clean_youtube)
def test_clean_string(string, expected):
    assert extract_titles.clean_string(string) == expected