import os,sys, timeit
sys.path.insert(0,'../')
import client
import random
import time
from config import *
import string
import cProfile
import logger

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
        r, o_val = client.kv739_put(key, value)
        if r==-1:
            print "SERVER CRASHED CRASHED!!!!!"
            time.sleep(1)
        i#print i, r, o_val

def get_test(n=10000, n_key=128, n_val=128):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_get(key, value)
        print r, val

def del_test(n=10000, n_key=128, n_val=128):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_delete(key, value)
        print r, val


def load_test(args):
    put_test(10000);
    pass

if __name__ == "__main__":
    client.kv739_init(sys.argv[1])
    logParentDir = 'log'
    if not os.path.isdir(logParentDir):
        print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|creating log dir")
        try:
            os.makedirs(logParentDir)
            print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log folder created: " + logParentDir)
        except:
            print(getTime() + "|ERROR|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log  folder could not be created at " + logParentDir)

    call = ['put']
    num = [10]
    k_size = [100]
    v_size = [100]
    for n in num:
        for k in k_size:
             for v in v_size:
                 for t in call:
                     try:
                         testName=t+"_test("+str(n)+","+str(k)+","+str(v)+")"
                         testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(k)+"_v-"+str(v)+".perf"
                         msg(0, opType, "Starting test: "+testName, myIP, "test")
                         cProfile.run(testName,testFileName)
                         msg(0, opType, "Test completed: "+testName, myIP, "test")
                     except:
                         msg(1, opType, "Unexcepted failure with test: "+testName, myIP, "test")
