from RSSItem import Item
import feedparser
from future import Future
try:
	import cPickle as pickle
except:
	import pickle
from lockfile import FileLock
from time import sleep
from functions import *
import socket
from balloonNotify import balloon_tip

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
        if x.isOld():
            continue
        if x not in items:
            items.append(x)
            balloon_tip("New RSS Item", x.name)
    items.sort()
    dumpItems(location, items)
    lock.release()
    return
    
def stripOld(location):
    lock = getFileLock(".", "rssItems.pkl")
    items = loadItems(".")
    a = [x for x in items if (not x.isOld() and x.isRead())]
    dumpItems(".", a)
    lock.release()
    return

def main():
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
    socket.setdefaulttimeout(30)
    while(True):
        #stripOld(".")
        feeds = loadFeeds(".")
        for x in feeds:
            print "--------\nWorking on %s" % x
            try:
				current = getFeeds([x])[0]
				feedItems = parseFeed(current)
				update(".", feedItems)
				print "Finished updating %s" % x 
            
            except Exception as e:
				print "Skipped %s" % x
				with open("debug.txt", "ab") as fp:
					fp.write("Broke with %s : %s\n" % (x, str(e)))
            sleep(120. / len(feeds))
        
if __name__ == "__main__":
    main()
            
