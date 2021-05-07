import datetime

import praw
from sqlalchemy import func

from modules.db import QuoteDB
from modules.model import Quote

db = QuoteDB()


def format_quote():
    """
    Format a random Quote for the thread

    Returns:
        str: random Quote formatted for the thread
    """
    random_quote: Quote = db.get_all().filter(Quote.has_been_used is False).order_by(func.random()).first()
    random_quote.mark(used=True)
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
