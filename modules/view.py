import random

import praw
from flask import Flask, render_template

from modules.db import QuoteDB
from modules.model import Post

app = Flask(__name__)
reddit = praw.Reddit("bot1")

all_quotes = QuoteDB().get_all()
all_posts = []
for i in reddit.subreddit("GoodBlackNews").new(limit=25):
    _ = Post(i.title, i.url)
    all_posts.append(_)

random_quote = random.choice(all_quotes)


@app.route("/")
def index():
    return render_template("index.html", quote=random_quote)


@app.route("/quotes")
def quotes():
    return render_template("quotes.html", all_quotes=all_quotes)


@app.route("/posts")
def posts():
    return render_template("posts.html", all_posts=all_posts)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
