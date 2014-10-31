from lockfile import FileLock
import pickle
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