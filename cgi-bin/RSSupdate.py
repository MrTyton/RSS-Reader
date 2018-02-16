from RSSItem import Item
import feedparser
from multiprocessing import Pool
from lockfile import FileLock
from functions import *
import socket
import datetime
import re
import urllib2
from string import strip
import cfscrape

# mess with this later
url_ignores = re.compile('(?P<url>.*?),(?P<filters>.*)')


lock = getFileLock("/tmp", "rssItems.pkl")
hasher = set(loadItems(".."))
lock.release()


def loadFeeds(location):
    lock = getFileLock("/tmp", "feeds.txt")
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    lock.release()
    return map(strip, data)


def update(feedItems, ignored, includes):
    if not includes:
        return [
            x for x in feedItems if (
                x not in hasher and not x.isOld() and not any(
                    filth in x.name for filth in ignored))]
    else:
        return [
            x for x in feedItems if (
                any(
                    useful in x.name for useful in includes) and x not in hasher and not x.isOld() and not any(
                    filth in x.name for filth in ignored))]


def runner(x):
    try:
        regex = url_ignores.search(x)
        if regex:
            info_dict = regex.groupdict()
            url = info_dict['url']
            if ";" in info_dict['filters']:
                ig, inc = info_dict['filters'].split(';')
                ignores = set(filter(None, map(strip, ig.split(","))))
                includes = set(filter(None, map(strip, inc.split(";"))))
            else:
                ignores = set(
                    filter(
                        None, map(
                            strip, info_dict['filters'].split(","))))
                includes = set()
        else:
            url = x
            ignores = set()
            includes = set()
        try:
            current = feedparser.parse(url)
            if not current.entries and current.bozo == 1:
                if "undefined entity" in str(current.bozo_exception):
                    with urllib2.urlopen(url) as req:
                        datum = req.read()
                        datum = datum.decode("utf-8", "ignore")
                        current = feedparser.parse(datum)
        except urllib2.HTTPError as err:
            if err.code == 403:
                scraper = cfscrape.create_scraper()
                data = scraper.get(url)
                current = feedparser.parse(data.content)
            else:
                raise
        feedItems = map(Item, current["items"])
        return update(feedItems, ignores, includes)
    except Exception as e:
        print "{} : Something broke with {}: {}".format(datetime.datetime.now().strftime("%B %d, %Y %I:%M%p"), x, e)
        return []


def main():
    socket.setdefaulttimeout(30)
    feeds = loadFeeds("..")
    pooler = Pool()
    results = pooler.map(runner, feeds)
    results = [x for y in results for x in y]

    if results:
        lock = getFileLock("/tmp", "rssItems.pkl")
        items = loadItems("..")
        items.extend(results)
        items = sorted([x for x in items if not x.isOld() or not x.isRead()])
        dumpItems("..", items)
        lock.release()


if __name__ == "__main__":
    main()
