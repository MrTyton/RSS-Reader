from RSSItem import Item
import feedparser
from future import Future
import pickle
from lockfile import FileLock
from time import sleep
from functions import *

def getFeeds(hit_list):
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    feeds = [future_obj() for future_obj in future_calls]
    return feeds

def parseFeed(feed):
    return [Item(x) for x in feed["items"]]


def loadFeeds(location):
    lock = getFileLock(location, "feeds.txt")
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    lock.release()
    return [x.replace("\n", "") for x in data]

def update(location, feedItems):
    lock = getFileLock(location, "rssItems.pkl")
    items = loadItems(location)
    for x in feedItems:
        if x not in items and not x.isOld():
            items.append(x)
    items.sort()
    dumpItems(location, items)
    lock.release()
    return
    
def stripOld(location):
    lock = getFileLock(".", "rssItems.pkl")
    items = loadItems(".")
    items = [x for x in items if (not x.isOld() and x.isRead())]
    dumpItems(".", items)
    lock.release()
    return

def main():
    i = 0
    lock = FileLock("./rssItems.pkl")
    lock.break_lock()
    lock = FileLock("./feeds.txt")
    lock.break_lock()
    #feeds = loadFeeds(".")
    #print "Doing initial load of: %s" % feeds
    #feeds = getFeeds(feeds)
    #for x in feeds:
    #    temp = parseFeed(x)
    #    update(".", temp)
    while(True):
        stripOld(".")
        feeds = loadFeeds(".")
        for x in feeds:
            print "--------\nWorking on %s" % x
            current = getFeeds([x])[0]
            feedItems = parseFeed(current)
            update(".", feedItems)
            print "Finished updating %s" % x 
            sleep(300 / len(feeds))
        
if __name__ == "__main__":
    main()
            
