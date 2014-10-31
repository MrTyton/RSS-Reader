import datetime
from datetime import date, timedelta

class Item:
    date = datetime.date(9999, 1, 1)
    isRead = False
    old = False
    link = ""
    name = ""
    
    def __lt__(self, other):
        if self.isRead == False and other.isRead == True:
            return True
        if self.isRead == True and other.isRead == False:
            return False
        if self.date < other.date:
            return True
        if self.date == other.date:
            return self.name < other.name
        return False
    
    def __gt__(self, other):
        return not (self < other or self == other)
    
    def __eq__(self, other):
        return self.date == other.date and self.link == other.link
    
    def __leq__(self, other):
        return self < other or self == other
    
    def __geq__(self, other):
        return self > other or self == other
    
    def isOld(self):
        self.old = (self.date() - date.today()) > timedelta(7)
        return self.old
    
    def __init__(self, information):
        if "date_parsed" in information.keys():
            self.date = date(information["date_parsed"])
        self.name = information["title"].encode('utf8')
        self.link = information["link"].encode('utf8')

    def get_is_read(self):
        return self.__isRead

    def get_link(self):
        return self.__link


    def get_name(self):
        return self.__name

    def set_is_read(self, value):
        self.__isRead = value
        
    def __str__(self):
        return "%s %s %s %r" % (self.name, self.link, str(self.date), self.isRead)
    


    