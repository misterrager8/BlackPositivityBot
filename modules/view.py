import random

import praw
from flask import render_template, request

from modules.db import QuoteDB
from modules.model import Post, Quote, app

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


@app.route("/quotes", methods=["POST", "GET"])
def quotes():
    if request.method == "POST":
        quote_text = request.form["quote_text"]
        author = request.form["author"]

        b = Quote(quote_text, author)
        b.add()

    return render_template("quotes.html", all_quotes=all_quotes)


@app.route("/posts")
def posts():
    return render_template("posts.html", all_posts=all_posts)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
