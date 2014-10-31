import datetime
from datetime import date, timedelta

class Item:
    dateadded = datetime.date(9999, 1, 1)
    read = False
    old = False
    link = ""
    name = ""
    
    def __lt__(self, other):
        if self.read == False and other.read == True:
            return True
        if self.read == True and other.read == False:
            return False
        if self.dateadded < other.dateadded:
            return True
        if self.dateadded == other.dateadded:
            return self.name < other.name
        return False
    
    def __gt__(self, other):
        return not (self < other or self == other)
    
    def __eq__(self, other):
        return self.dateadded == other.dateadded and self.link == other.link
    
    def __leq__(self, other):
        return self < other or self == other
    
    def __geq__(self, other):
        return self > other or self == other
    
    def isOld(self):
        self.old = (date.today() - self.dateadded) > timedelta(7)
        return self.old
    
    def isRead(self):
        return self.read
    
    def __init__(self, information):
        if "date_parsed" in information.keys():
            self.dateadded = date(information["date_parsed"])
        self.name = information["title"].encode('utf8')
        self.link = information["link"].encode('utf8')

    def get_link(self):
        return self.__link


    def get_name(self):
        return self.__name

        
    def __str__(self):
        return "%s %s %s %r" % (self.name, self.link, str(self.dateadded), self.read)
    


    