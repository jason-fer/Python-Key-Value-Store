import os,sys, timeit
sys.path.insert(0,'../')
import client
import dbWorkers
import random
import time
from config import *
import string
import cProfile
import logger
import timeit

PERF_TEST_SERVER=False

if PERF_TEST_SERVER:
    get=dbWorkers.get
    put=dbWorkers.put
    delete=dbWorkers.delete
    init=dbWorkers.startConnection
else:
     get=client.kv739_get
     put=client.kv739_put
     delete=client.kv739_delete
     init=client.kv739_init

msg=logger.msg
getTime=logger.getTime
getDate=logger.getDate
logFileObj=logger.logFileObj

myIP = "localhost:perf_test"
opType = "PERF"

def get_rand_string(n=128):
    return ''.join(random.choice(string.ascii_uppercase + \
                                 string.ascii_lowercase + \
                                 string.digits + ' ') for _ in range(n))


def put_test(n=10000, n_key=128, n_val=128):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, o_val = put(key, value)
        if r==-1:
            print "SERVER CRASHED CRASHED!!!!!"
            time.sleep(1)
        #print i, r, o_val

def get_test(n=10000, n_key=128, n_val=128):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = get(key)
        #print r, val

def delete_test(n=10000, n_key=128, n_val=128):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = delete(key)
        #print r, val


def load_test(args):
    put_test(10000);
    pass

if __name__ == "__main__":
    serverUrl=sys.argv[1]
    #client.kv739_init(serverUrl)
    init(serverUrl)
    logParentDir = 'log'
    if not os.path.isdir(logParentDir):
        print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|creating log dir")
        try:
            os.makedirs(logParentDir)
            print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log folder created: " + logParentDir)
        except:
            print(getTime() + "|ERROR|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log  folder could not be created at " + logParentDir)

    call = ['get','put','delete']
    num = [1]
    k_size = [10]
    v_size = [10]
    msgAppend="["+serverUrl+"] "
    for n in num:
        for k in k_size:
             for v in v_size:
                 for t in call:
                     try:
                         testName=t+"_test("+str(n)+","+str(k)+","+str(v)+")"
                         testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(k)+"_v-"+str(v)+"__"+getTime()+".perf"
                         testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(k)+"_v-"+str(v)+".perf" 
                         msg(0, opType, msgAppend+"Starting test: "+testName, myIP, "test")
                         #cProfile.run(testName) #,testFileName)
                         t = timeit.timeit(stmt=testName, number=1, setup='from __main__ import get_test, put_test, delete_test')
			 msg(0, opType, msgAppend+"Test completed: "+testName, myIP, "test")
                         msg(0, opType, msgAppend+"Time taken: "+testName+": " + str(t), myIP, "test")
                     except:
                         msg(1, opType, msgAppend+"Unexcepted failure with test: "+testName, myIP, "test")
