import datetime
import os

import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text, Integer, Boolean

app = Flask(__name__)

dotenv.load_dotenv()

db_host = os.getenv("host")
db_user = os.getenv("user")
db_pass = os.getenv("passwd")
db_name = os.getenv("db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Quote(db.Model):
    __tablename__ = "quotes"

    quote_text = Column(Text)
    author = Column(Text)
    has_been_used = Column(Boolean)
    date_added = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 quote_text: str,
                 author: str,
                 has_been_used: bool = False,
                 date_added: str = datetime.datetime.now().strftime("%Y-%m-%d")):
        """
        Create Quote object

        Args:
            quote_text(str): Text of the quote
            author(str): Author of the quote
            has_been_used(bool): has the Quote been posted already?
            date_added(str): Date the Quote was added to the DB
        """
        self.quote_text = quote_text
        self.author = author
        self.has_been_used = has_been_used
        self.date_added = date_added

    def add(self):
        """
        Add Quote to DB
        """
        db.session.add(self)
        db.session.commit()

    def mark_used(self):
        """
        Mark Quote 'used'
        """
        self.has_been_used = True
        db.session.commit()

    def mark_unused(self):
        """
        Mark Quote 'unused'
        """
        self.has_been_used = False
        db.session.commit()

    def remove(self):
        """
        Delete Quote from DB
        """
        db.session.remove(self)
        db.session.commit()

    def to_string(self):
        print(self.quote_text,
              self.author,
              self.date_added,
              self.has_been_used)


class Post(db.Model):
    __tablename__ = "gbn_posts"

    id = Column(Integer, primary_key=True)

    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url


db.create_all()
