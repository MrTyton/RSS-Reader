import cgitb
import pickle
from lockfile import FileLock
import RSSItem
#cgitb.enable()

def getFileLock(location, filename):
    lock = FileLock("%s/%s" % (location, filename))
    while not lock.i_am_locking():
        try:
            lock.acquire(timeout=60)
        except LockTimeout:
            lock.break_lock()
            lock.acquire()
    return lock

def loadItems(location):
    with open("%s/rssItems.pkl" % location, "r") as fp:
        items = pickle.load(fp)
    return items

def dumpItems(location, items):
    with open("%s/rssItems.pkl" % location, "w") as fp:
        pickle.dump(items, fp)
    return
lock = FileLock("./rssItems.pkl")
lock.break_lock()
lock = FileLock("./feeds.txt")
lock.break_lock()
lock = getFileLock(".", "rssItems.pkl")
items = loadItems(".")
current = None
for i,x in enumerate(items):
    if not x.isRead():
        current = x
        items[i].read = True
        break
dumpItems(".", items)
lock.release()


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers


if current is not None:
    print """<html><title>Redirecting</title><head><script type="text/javascript"><!--
function Redirect()
{
    window.location="%s";
}

//-->
<body onLoad="setTimeout('Redirect()', 2000)">Redirecting to <a href="%s">%s</s></body></html>""" % (current.link, current.name, current.link)
else:
    print """<html><title>Nothing Here><head></head><body>Nothing else for you to read. Try again later.</body></html>"""