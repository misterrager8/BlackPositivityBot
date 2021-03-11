import datetime
import random

import praw

from modules.db import QuoteDB

db = QuoteDB()


def format_quote():
    """
    Format a random Quote for the thread

    Returns:
        str: random Quote formatted for the thread
    """
    random_quote = random.choice(db.get_all_unused())
    random_quote.mark_used()
    return '"{}", {}'.format(random_quote.quote_text, random_quote.author)


def post_thread():
    """
    Create a thread in subreddit
    """
    right_now = datetime.datetime.now()
    title = "Black Positivity Quote - " + right_now.strftime("%m/%d/%Y")
    post_content = format_quote()
    reddit.subreddit("GoodBlackNews").submit(title, selftext=post_content)
    print('"{}" submission created'.format(title))


if __name__ == "__main__":
    reddit = praw.Reddit("bot1")

    # post_thread()
    # print(format_quote())
