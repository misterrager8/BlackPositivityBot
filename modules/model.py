import datetime


class Quote:
    def __init__(self,
                 quote_text: str,
                 author: str,
                 has_been_used: bool = False,
                 date_added: str = datetime.datetime.now().strftime("%Y-%m-%d")):
        self.quote_text = quote_text
        self.author = author
        self.has_been_used = has_been_used
        self.date_added = date_added

    def tostring(self):
        print(self.quote_text,
              self.author,
              self.date_added)
