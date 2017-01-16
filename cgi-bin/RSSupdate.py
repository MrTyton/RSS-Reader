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
from subprocess import check_output, STDOUT
import datetime
import os
import sys
import re

url_ignores = re.compile('(?P<url>.*?),(?P<filters>.*)')

hasher = []



def getFeeds(hit_list):
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    feeds = [future_obj() for future_obj in future_calls]
    return feeds

def parseFeed(feed):
    return [Item(x) for x in feed["items"]]


def loadFeeds(location):
    lock = getFileLock("/tmp", "feeds.txt")
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    lock.release()
    return [x.replace("\n", "") for x in data]

def update(location, feedItems, ignored):
    global hasher
    toadd = []
    for x in feedItems:
        if x.isOld() or any(filth in x.name for filth in ignored):
            continue
        if x not in hasher:
            toadd.append(x)
            hasher.append(x)
            try:
                res = check_output('echo "RSS;{};rss" | bash /home/joshua/Scripts/Notifications/message.sh'.format(x.name), shell=True,stderr=STDOUT)
            except:
                pass
    if toadd != []:
        hasher.sort()
        lock = getFileLock("/tmp", "rssItems.pkl")
        items = loadItems(location)
        items.extend(toadd)
        items.sort()
        dumpItems(location, items)
        lock.release()
    return
    
def stripOld(location):
    lock = getFileLock("/tmp", "rssItems.pkl")
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
    socket.setdefaulttimeout(30)
    stripOld(".")
    lock = getFileLock("/tmp", "rssItems.pkl")
    global hasher
    hasher = loadItems(".")
    lock.release()
    counter = 1
    while(True):
        if counter % 43200 == 0: stripOld(".")
        counter += 1
        feeds = loadFeeds(".")
        for x in feeds:
            print "--------\nWorking on %s" % x
            try:
                regex = url_ignores.search(x)
                if regex:
                    info_dict = regex.groupdict()
                    url = info_dict['url']
                    ignores = [q.strip() for q in info_dict['filters'].split(",")]
                else:
                    url = x
                    ignores = []
                current = getFeeds([url])[0]
                feedItems = parseFeed(current)
                update(".", feedItems, ignores)
                print "Finished updating %s" % x 
            
            except Exception as e:
				print "Skipped %s" % x
				with open("debug.txt", "ab") as fp:
					fp.write("{}: Broke with {} : {}\n".format(datetime.datetime.now().strftime("%B %d, %Y %I:%M%p"),x, e))
            sleep(120. / len(feeds))
        
        
if __name__ == "__main__":
    main()
            
