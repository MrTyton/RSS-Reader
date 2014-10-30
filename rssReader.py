from RSSItem import Item
import feedparser
from future import Future
import pickle

def getFeeds(hit_list):
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    feeds = [future_obj() for future_obj in future_calls]
    return feeds

def parseFeed(feed):
    return [Item(x) for x in feed["items"]]

def loadFeeds(location):
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    return [x.replace("\n", "") for x in data]

def update():
    feeds = loadFeeds(".")
    feeds = getFeeds(feeds)
    items = []
    feedItems = parseFeed(feeds[0])
    for x in feedItems:
        if x not in items:
            items.append(x)
    items.sort()
    for x in items: print x
    
update()
 