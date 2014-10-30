import datetime
from datetime import date, timedelta

class Item:
    date = datetime.date(9999, 1, 1)
    isRead = False
    isOld = False
    link = ""
    name = ""
    
    def __lt__(self, other):
        return (self.isRead == False and other.isRead == True) or self.date < other.date
    
    def __gt__(self, other):
        return (self.isRead == True and other.isRead == False) or self.date > other.date
    
    def __eq__(self, other):
        return self.date == other.date and self.link == other.link
    
    def __leq__(self, other):
        return self < other or self == other
    
    def __geq__(self, other):
        return self > other or self == other
    
    def isOld(self):
        return (self.date() - date.today()) > timedelta(7)
    
    def __init__(self, information):
        if "date_parsed" in information.keys():
            self.date = date(information["date_parsed"])
        self.name = information["title"]
        self.link = information["link"]
        