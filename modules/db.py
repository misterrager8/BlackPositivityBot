import csv
import MySQLdb

import modules.models


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
            quote_x = modules.models.Quote(result[1], result[2], result[3], result[4])
            return quote_x
        except MySQLdb.Error as e:
            print(e)

    def add_quote(self, new_quote):
        sql = "INSERT INTO quotes (quotetext, author, hasbeenused, dateadded) VALUES ('%s', '%s', '%d', '%s')" % (
            new_quote.quote_text, new_quote.author, new_quote.has_been_used, new_quote.date_added)
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
            quote_x = modules.models.Quote(row[1], row[2], row[3], row[4])
            quotes_list.append(quote_x)

        return quotes_list

    def view_unused_quotes(self):
        quotes_list = []
        sql = "SELECT * FROM quotes WHERE hasbeenused = False"

        for row in self.db_read(sql):
            quote_x = modules.models.Quote(row[1], row[2], row[3], row[4])
            quotes_list.append(quote_x)

        return quotes_list

    def view_used_quotes(self):
        quotes_list = []
        sql = "SELECT * FROM quotes WHERE hasbeenused = True"

        for row in self.db_read(sql):
            quote_x = modules.models.Quote(row[1], row[2], row[3], row[4])
            quotes_list.append(quote_x)

        return quotes_list

    def import_quotes(self):
        imported = []
        with open("input.csv") as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                csv_quote = modules.models.Quote(row[0], row[1])
                imported.append(csv_quote)

        print(str(len(imported)) + " quote(s) found.")
        for item in imported:
            item.tostring()

        answer = input("Add these quotes? ")
        if answer == "Y" or answer == "y":
            for item in imported:
                self.add_quote(item)
