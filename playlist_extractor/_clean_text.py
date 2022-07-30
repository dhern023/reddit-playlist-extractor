import re
import unicodedata

def normalize_non_ascii(string):
    string_p  = (
        unicodedata
        .normalize('NFKD', string)
        .encode('ascii', 'ignore')
        .decode("utf-8")
    )
    return string_p

def clean_non_ascii(string, replacement = ''):
    return re.sub(r"[^\\x00-\\x7F]", replacement, string)

def clean_white_space(string, replacement = ' '):
    return re.sub(r"\s+", replacement, string)
