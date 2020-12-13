import csv
import datetime
import random

import MySQLdb
import praw


class QuoteObject:
    def __init__(self, quotetext, author, hasbeenused=False, dateadded=datetime.datetime.now().strftime("%Y-%m-%d"),
                 quoteid=None):
        self.quotetext = quotetext
        self.author = author
        self.hasbeenused = hasbeenused
        self.dateadded = dateadded
        self.quoteid = quoteid

    def tostring(self):
        print(self.quoteid,
              self.quotetext,
              self.author,
              bool(self.hasbeenused),
              self.dateadded)


class QuoteDB:
    def __init__(self):
        pass

    @classmethod
    def db_write(cls, query):
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(query)
            db.commit()
        except MySQLdb.Error as e:
            print(e)

        db.close()

    @classmethod
    def db_read(cls, query):
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(query)
            return cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)

    @classmethod
    def get_quote_by_id(cls, quote_id):
        sql = "SELECT * FROM quotes WHERE quoteID = '%d'" % quote_id
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            quote_x = QuoteObject(result[1], result[2], result[3], result[4], result[0])
            return quote_x
        except MySQLdb.Error as e:
            print(e)

    def add_quote(self, new_quote):
        sql = "INSERT INTO quotes (quotetext, author, hasbeenused, dateadded) VALUES ('%s', '%s', '%d', '%s')" % (
            new_quote.quotetext, new_quote.author, new_quote.hasbeenused, new_quote.dateadded)
        self.db_write(sql)
        print("Added.")

    def delete_quote(self, quote_id):
        sql = "DELETE FROM quotes WHERE quoteID = '%d'" % quote_id
        self.db_write(sql)
        print("Deleted.")

    def delete_all_quotes(self):
        sql = "TRUNCATE TABLE quotes"
        self.db_write(sql)
        print("All deleted.")

    def mark_used(self, quote_id):
        sql = "UPDATE quotes SET hasbeenused = True WHERE quoteID = '%d'" % quote_id
        self.db_write(sql)
        print("Marked 'used'.")

    def mark_unused(self, quote_id):
        sql = "UPDATE quotes SET hasbeenused = False WHERE quoteID = '%d'" % quote_id
        self.db_write(sql)
        print("Marked 'unused'.")

    def mark_all_used(self):
        sql = "UPDATE quotes SET hasbeenused = True"
        self.db_write(sql)
        print("All marked 'used'.")

    def mark_all_unused(self):
        sql = "UPDATE quotes SET hasbeenused = False"
        self.db_write(sql)
        print("All marked 'unused'.")

    def view_all_quotes(self):
        quotes_list = []
        sql = "SELECT * FROM quotes"

        for row in self.db_read(sql):
            quote_x = QuoteObject(row[1], row[2], row[3], row[4], row[0])
            quotes_list.append(quote_x)

        return quotes_list

    def view_unused_quotes(self):
        quotes_list = []
        sql = "SELECT * FROM quotes WHERE hasbeenused = False"

        for row in self.db_read(sql):
            quote_x = QuoteObject(row[1], row[2], row[3], row[4], row[0])
            quotes_list.append(quote_x)

        return quotes_list

    def view_used_quotes(self):
        quotes_list = []
        sql = "SELECT * FROM quotes WHERE hasbeenused = True"

        for row in self.db_read(sql):
            quote_x = QuoteObject(row[1], row[2], row[3], row[4], row[0])
            quotes_list.append(quote_x)

        return quotes_list

    def import_quotes(self):
        imported = []
        with open("input.csv") as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                csv_quote = QuoteObject(row[0], row[1])
                imported.append(csv_quote)

        print(str(len(imported)) + " quote(s) found.")
        for item in imported:
            item.tostring()

        answer = input("Add these quotes? ")
        if answer == "Y" or answer == "y":
            for item in imported:
                self.add_quote(item)


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
