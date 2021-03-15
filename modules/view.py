import random

import praw
from flask import Flask, render_template

from modules.db import QuoteDB

app = Flask(__name__)

all_quotes = QuoteDB().get_all()
random_quote = random.choice(all_quotes)
reddit = praw.Reddit("bot1")


@app.route("/")
def index():
    return render_template("index.html", quote=random_quote)


@app.route("/quotes")
def quotes():
    return render_template("quotes.html")


@app.route("/posts")
def posts():
    return render_template("posts.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
