import sys, os
import dbWorkers 
from config import *
import random, json

get_from_db = dbWorkers.get
put_in_db = dbWorkers.put
delete_in_db = dbWorkers.delete

_cache_ = {}


def insert(key, val):
    l = 0
    try:
        l = _cache_[key][1]
    except KeyError:
        l = 0
    _cache_[key] = [val, l+1]
    print json.dumps(_cache_)
    print "Inserting into the cache: key='%s' & value='%s'" % ( key, val)
    if len(_cache_)>MAX_CACHE_SIZE:
        k = min(_cache_, key=lambda k: _cache_[k][1]+\
                random.randint(0,MAX_CACHE_SIZE)) 
        print "Deleting from the cache: key='%s'" % k
        del _cache_[k]

def get(key, c_ip=None):
    try:
        val,t = _cache_[key]
        _cache_[key][1] = t+1  #the last used count
        dbWorkers.msg(0,'GET (from cache)', "key='%s' found" % key, c_ip)
        return 0, val
    except KeyError:
        status, val = dbWorkers.get(key, c_ip)
        if status==0:
            insert(key, val)
        return status, val

def put(key, val, c_ip):
    insert(key, val)
    return dbWorkers.put(key, val, c_ip)

def delete(key, c_ip):
    try:
        print "Deleting from cache"
        del _cache_[key]
    except KeyError:
        pass
    return dbWorkers.delete(key, c_ip)



