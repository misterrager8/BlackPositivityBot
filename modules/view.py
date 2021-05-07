import praw
from flask import render_template, request, url_for, redirect
from sqlalchemy import func

from modules.db import QuoteDB
from modules.model import Post, Quote, app

reddit = praw.Reddit("bot1")
qdb = QuoteDB()


@app.route("/")
def index():
    random_quote = qdb.get_all().order_by(func.random()).first()
    return render_template("index.html", quote=random_quote)


@app.route("/quotes", methods=["POST", "GET"])
def quotes():
    return render_template("quotes.html", quotes=qdb.get_all())


@app.route("/delete_quote")
def delete_quote():
    id_ = request.args.get("id_")
    quote_: Quote = qdb.find_by_id(id_)
    qdb.remove(quote_)

    return redirect(url_for("quotes"))


@app.route("/search", methods=["POST"])
def search_quotes():
    search_term = request.form["search_term"]
    _ = qdb.get_all().filter(Quote.quote_text.ilike(f"%{search_term}%"))

    return render_template("quotes.html", quotes=_)


@app.route("/add", methods=["POST"])
def add_quote():
    quote_text = request.form["quote_text"]
    author = request.form["author"]
    qdb.add(Quote(quote_text, author))

    return render_template("quotes.html", quotes=qdb.get_all())


@app.route("/posts")
def posts():
    return render_template("posts.html", all_posts=all_posts)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
