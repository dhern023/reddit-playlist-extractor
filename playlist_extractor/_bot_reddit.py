import praw

class RedditBotInterface:
    """
    Generic RedditBot class
        Can check if called
        Can private message
        Can comment on subreddit threads
    """
    def __init__(
        self, 
        string_username_bot, 
        string_botname_full, 
        string_source, 
        list_subreddits_bot_friendly = ["music", "stonerrock", "techno"]
        ):

        self.instance_reddit = None
        self.string_username_bot = string_username_bot
        self.subreddits_bot_friendly = list_subreddits_bot_friendly
        self.string_version = "0.0.0" # extract version from github release

        self.instance_reddit = self.construct_instance_reddit(
            string_botname_full, string_source)

    def construct_instance_reddit(self, string_botname_full, string_source = "???"):
        """
        TODO: Version should be extracted from the github releases URL
        # TODO: Verify connection via praw
        Note: Username and Password not required to access public comments
        """
        user_agent = f"{string_botname_full} v{self.string_version}. Source at {string_source}"
        # user_agent = f"Comment Extraction (by {string_botname_full})"
        instance_reddit = praw.Reddit(
            user_agent=user_agent,
            username=self.string_username_bot
        )

        return instance_reddit

    def check_bot_called(self, string):
        if f"{self.string_username_bot}!" in string.lower():
            return True
        return False

    def send_private_message(self, instance_comment, subject, body):
        """ Markdown doesn't work with PRAW """
        user = instance_comment.author
        self.instance_reddit.redditor(user.name).message(subject, body)

        return

    def call_reply(self, instance_comment, string):
        """ TODO: Check if all went well """
        instance_comment.reply(string)

        return

    def post_comment(self, instance_comment, string):

        if instance_comment.subreddit in self.subreddits_bot_friendly:  # bots can comment
            self.call_reply(instance_comment, string)
        else:
            self.send_private_message(instance_comment, string)
            self.call_reply(instance_comment, string)  # post link to list
        return