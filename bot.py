import datetime
import random

import praw

from modules.db import QuoteDB


def format_quote():
    db = QuoteDB()
    random_quote = random.choice(db.view_unused_quotes())
    db.mark_used(random_quote.quoteid)
    return '"{}", {}'.format(random_quote.quotetext, random_quote.author)


# create a thread in subreddit
def post_thread():
    right_now = datetime.datetime.now()
    title = "Black Positivity Quote - " + right_now.strftime("%m/%d/%Y")
    post_content = format_quote()
    reddit.subreddit("GoodBlackNews").submit(title, selftext=post_content)
    print('"{}" submission created'.format(title))


if __name__ == "__main__":
    reddit = praw.Reddit("bot1")

    # post_thread()
    # print(format_quote())

    # QuoteDB().add_quote(QuoteObject("test quote", "test author"))
    # QuoteDB().delete_quote(10)
    # QuoteDB().delete_all_quotes()

    # for i in QuoteDB().view_all_quotes(): i.tostring()
    # for i in QuoteDB().view_unused_quotes(): i.tostring()
    # for i in QuoteDB().view_used_quotes(): i.tostring()

    # QuoteDB().import_quotes()
    # QuoteDB().get_quote_by_id(5).tostring()
    # QuoteDB().mark_used(5)
    # QuoteDB().mark_unused(5)
    # QuoteDB().mark_all_used()
    # QuoteDB().mark_all_unused()
