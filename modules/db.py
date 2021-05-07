import csv

from modules.model import db, Quote


class QuoteDB:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        """
        Get all Quotes

        Returns:
            list: all Quotes
        """
        return db.session.query(Quote).all()

    @staticmethod
    def find_by_id(id_: int):
        return db.session.query(Quote).get(id_)

    @staticmethod
    def get_all_used():
        """
        Get all used Quotes

        Returns:
            list: used Quotes
        """
        return db.session.query(Quote).filter(Quote.has_been_used)

    @staticmethod
    def get_all_unused():
        """
        Get all unused Quotes

        Returns:
            list: unused Quotes
        """
        return db.session.query(Quote).filter(not Quote.has_been_used)

    @staticmethod
    def remove_all():
        """
        Delete all Quotes from DB
        """
        db.session.execute("TRUNCATE table quotes")
        db.session.commit()

    @staticmethod
    def mark_all(used: bool):
        """
        Mark all Quotes as 'used' or 'unused'
        """
        db.session.execute("UPDATE quotes SET has_been_used = %s" % used)
        db.session.commit()

    def import_quotes(self):
        """
        Import multiple Quotes from csv
        """
        imported = []
        with open("input.csv") as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                csv_quote = Quote(row[0], row[1])
                imported.append(csv_quote)

        print(str(len(imported)) + " quote(s) found.")
        for item in imported:
            print(str(item))

        answer = input("Add these quotes? ")
        if answer == "Y" or answer == "y":
            for item in imported:
                self.add(item)
