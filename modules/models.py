from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Date

from modules import db


class Quote(db.Model):
    __tablename__ = "quotes"

    quote_text = Column(Text)
    author = Column(Text)
    has_been_used = Column(Boolean, default=False)
    date_added = Column(DateTime)
    date_used = Column(Date)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Quote, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.quote_text,
                          self.author)


class Admin(db.Model, UserMixin):
    __tablename__ = "admins"

    username = Column(Text)
    password = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.username


class Article(db.Model):
    __tablename__ = "articles"

    url = Column(Text)
    title = Column(Text)
    source = Column(Text)
    date_posted = Column(DateTime)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Article, self).__init__(**kwargs)

    def get_source(self):
        if self.source == "AfroTech":
            return [self.source, "#23C7B4"]
        elif self.source == "Because Of Them We Can":
            return [self.source, "black"]
        elif self.source == "Face2Face Africa":
            return [self.source, "#BEAB40"]
        elif self.source == "The Grio":
            return [self.source, "#0E6C83"]
        else:
            return [self.source, "orange"]

    def __str__(self):
        return "%s,%s" % (self.title, self.url)


db.create_all()
