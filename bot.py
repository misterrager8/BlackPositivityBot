from datetime import datetime, date

import praw
from sqlalchemy import func

from modules import views, db
from modules.models import Quote


def format_quote():
    """
    Format a random Quote for the thread

    Returns:
        str: random Quote formatted for the thread
    """
    random_quote: Quote = db.session.query(Quote).filter(Quote.has_been_used == False).order_by(func.random()).first()
    random_quote.has_been_used = True
    random_quote.date_used = date.today()
    db.session.commit()
    return '"{}", {}'.format(random_quote.quote_text, random_quote.author)


def post_thread():
    """
    Create a thread in subreddit
    """
    right_now = datetime.now()
    title = "Black Positivity Quote - " + right_now.strftime("%m/%d/%Y")
    post_content = format_quote()
    praw.Reddit("bot1").subreddit("GoodBlackNews").submit(title, selftext=post_content)
    print('"{}" submission created'.format(title))


if __name__ == "__main__":
    views.app.run(debug=True)
