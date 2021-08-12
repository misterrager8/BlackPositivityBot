from datetime import datetime, date

import praw
from flask import render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from modules import app, db, login_manager
from modules.crawler import Crawler
from modules.models import Quote, Admin, Article

reddit = praw.Reddit("bot1")

crwlr = Crawler
articles_ = crwlr.afrotech() + \
            crwlr.becauseofthemwecan() + \
            crwlr.face2faceafrica() + \
            crwlr.thegrio()


@login_manager.user_loader
def load_user(admin_id):
    return db.session.query(Admin).get(int(admin_id))


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_: Admin = db.session.query(Admin).filter_by(username=username).first()
        if user_ and check_password_hash(generate_password_hash(user_.password), password):
            login_user(user_)
            return redirect(request.referrer)
        else:
            return "Login failed."


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.referrer)


@app.route("/")
def index():
    return render_template("index.html",
                           qotd=db.session.query(Quote).filter(Quote.date_used == date.today()).first(),
                           latest=db.session.query(Article).order_by(text("date_posted desc")).all()[:5])


@app.route("/quotes", methods=["POST", "GET"])
def quotes():
    return render_template("quotes.html", quotes=db.session.query(Quote).order_by(text("date_added desc")).all())


@app.route("/quote_delete")
@login_required
def quote_delete():
    id_ = request.args.get("id_")
    quote_: Quote = db.session.query(Quote).get(id_)
    db.session.delete(quote_)
    db.session.commit()

    return redirect(url_for("quotes"))


@app.route("/quote_search", methods=["POST"])
def quote_search():
    search_term = request.form["search_term"]
    _ = db.session.query(Quote).filter(Quote.quote_text.ilike(f"%{search_term}%"))

    return render_template("quotes.html", quotes=_)


@app.route("/quote_create", methods=["POST"])
@login_required
def quote_create():
    db.session.add(Quote(quote_text=request.form["quote_text"],
                         author=request.form["author"],
                         date_added=datetime.now()))
    db.session.commit()

    return redirect(url_for("quotes"))


@app.route("/quote_update", methods=["POST"])
@login_required
def quote_update():
    id_: int = request.args.get("id_")
    quote_: Quote = db.session.query(Quote).get(id_)

    quote_.quote_text = request.form["quote_text"]
    quote_.author = request.form["author"]
    db.session.commit()

    return redirect(url_for("quotes"))


@app.route("/article_create", methods=["POST"])
@login_required
def article_create():
    _ = Article(url=request.form["url"],
                title=request.form["title"],
                source=request.form["source"],
                date_posted=datetime.now())

    db.session.add(_)
    db.session.commit()

    reddit.subreddit("GoodBlackNews").submit(title=_.title, url=_.url, send_replies=False)
    return redirect(url_for("news"))


@app.route("/news")
def news():
    return render_template("news.html", news_=db.session.query(Article).order_by(text("date_posted desc")).all())


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", articles_=articles_)


@app.route("/make_post")
@login_required
def make_post():
    url_ = request.args.get("url_")
    title_ = request.args.get("title_")
    source_ = request.args.get("source_")

    db.session.add(Article(url=url_, title=title_, source=source_, date_posted=datetime.now()))
    db.session.commit()

    reddit.subreddit("GoodBlackNews").submit(title=title_, url=url_, send_replies=False)
    return redirect(url_for("news"))


@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")
