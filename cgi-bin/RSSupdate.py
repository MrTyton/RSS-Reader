from RSSItem import Item
import feedparser
from multiprocessing import Pool, cpu_count

try:
	import cPickle as pickle
except:
	import pickle
    
    
from lockfile import FileLock
from time import sleep, time
from functions import *
import socket
import datetime
import os
import sys
import re

url_ignores = re.compile('(?P<url>.*?),(?P<filters>.*)')

hasher = []

def loadFeeds(location):
    lock = getFileLock("/tmp", "feeds.txt")
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    lock.release()
    return [x.replace("\n", "") for x in data]

def update(feedItems, ignored):
    return [x for x in feedItems if not (x.isOld() or any(filth in x.name for filth in ignored)) and x not in hasher]

def runner(x):
	try:
		regex = url_ignores.search(x)
		if regex:
			info_dict = regex.groupdict()
			url = info_dict['url']
			ignores = [q.strip() for q in info_dict['filters'].split(",")]
		else:
			url = x
			ignores = []
		current = feedparser.parse(x)
		feedItems = [Item(x) for x in current["items"]]
		return update(feedItems, ignores)
	except Exception as e:
		print "{} : Something broke with {}: {}".format(datetime.datetime.now().strftime("%B %d, %Y %I:%M%p"), x, e)
	
def main():
    socket.setdefaulttimeout(30)
    lock = getFileLock("/tmp", "rssItems.pkl")
    global hasher
    hasher = set(loadItems(".."))
    lock.release()
    feeds = loadFeeds("..")
        
    pooler = Pool()
    results = pooler.map(runner, feeds)
    results = [x for y in results for x in y]
    
    if results != []:
        lock = getFileLock("/tmp", "rssItems.pkl")
        items = loadItems("..")
        items.extend(results)
        items = [x for x in items if not (x.isOld() and x.isRead())]
        items.sort()
        dumpItems("..", items)
        lock.release()
    
        
if __name__ == "__main__":
    main()
            
