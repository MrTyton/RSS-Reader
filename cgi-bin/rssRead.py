import cgitb
import pickle
import RSSItem
from functions import *
cgitb.enable()

lock = getFileLock("cgi-bin", "rssItems.pkl")
items = loadItems("cgi-bin")
current = None
for i,x in enumerate(items):
    if not x.isRead():
        current = x
        items[i].read = True
        break
dumpItems("cgi-bin", items)
lock.release()


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers


if current is not None:
    print """<html><title>Redirecting</title><head><script type="text/javascript"><!--
function Redirect()
{
    window.location="%s";
}

//--></script>
<body onLoad="setTimeout('Redirect()', 2000)">Redirecting to <a href="%s">%s</s></body></html>""" % (current.link, current.link, current.name)
else:
    print """<html><title>Nothing Here><head></head><body>Nothing else for you to read. Try again later.</body></html>"""