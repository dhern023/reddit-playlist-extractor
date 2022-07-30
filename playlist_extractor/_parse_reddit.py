list_regex_replies = [
    r"\[.+\d+ children\)",
    r"\[.+\d+ child\)",
    r"permalink.+\d+ replies\)",
    r"load.+\d+ replies\)",
    r"load.+\d+ reply\)",
]

list_regex_non_ascii = [
    "\xe2\x80\x99",
]

list_strings = [
    "permalink embed save parent report give award reply",
    "permalink embed save parent report give award reply",
    "permalink embed save report give award reply",
    "\\xe2\\x80\\x99",
    "\xe2\x80\x99"
]

# Generic =========================================================================================

def extract_reddit_comments(url, instance_reddit):
    submission = instance_reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    return submission.comments.list()

def extract_comment_tree(instance_comment):
    if "all" in instance_comment.body.lower(): # root comment
        return instance_comment.submission.comments.list()
    return list(instance_comment.submission.comments)

def extract_comment_bodies(list_comments):
    list_strings = []
    for instance_comment in list_comments:
        if not hasattr(instance_comment, "body"):
            continue
        list_strings.append(instance_comment.body)
    
    return list_strings