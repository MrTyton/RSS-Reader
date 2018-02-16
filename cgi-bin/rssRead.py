#!/usr/bin/env python

from functions import *

lock = getFileLock("/tmp", "rssItems.pkl")
items = loadItems("../private/")
current = None
for i, x in enumerate(items):
    if not x.isRead():
        current = x
        items[i].read = True
        break
dumpItems("../private/", items)

if current:
    print current.link
    print current.name
else:
    print -1
    print -1
lock.release()
