from RSSItem import Item
import feedparser
from future import Future
import pickle
from lockfile import FileLock
from time import sleep

def getFeeds(hit_list):
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    feeds = [future_obj() for future_obj in future_calls]
    return feeds

def parseFeed(feed):
    return [Item(x) for x in feed["items"]]

def getFileLock(location, filename):
    lock = FileLock("%s/%s" % (location, filename))
    while not lock.i_am_locking():
        try:
            lock.acquire(timeout=60)
        except LockTimeout:
            lock.break_lock()
            lock.acquire()
    return lock

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
        if x not in items:
            items.append(x)
    items.sort()
    dumpItems(location, items)
    lock.release()

def loadItems(location):
    with open("%s/rssItems.pkl" % location, "r") as fp:
        items = pickle.load(fp)
    return items

def dumpItems(location, items):
    with open("%s/rssItems.pkl" % location, "w") as fp:
        pickle.dump(items, fp)
    return

def main():
    i = 0
    lock = FileLock("./rssItems.pkl")
    lock.break_lock()
    lock = FileLock("./feeds.txt")
    lock.break_lock()
    feeds = loadFeeds(".")
    print "Doing initial load of: %s" % feeds
    feeds = getFeeds(feeds)
    for x in feeds:
        update(".", parseFeed(x))
    while(True):
        feeds = loadFeeds(".")
        for x in feeds:
            print "Working on %s" % x
            current = getFeeds([x])[0]
            feedItems = parseFeed(current)
            update(".", feedItems)
            sleep(20)
        
if __name__ == "__main__":
    main()
            
