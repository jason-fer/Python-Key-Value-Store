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
perfResultObj=None

myIP = "localhost"
opType = "PERF"
msgAppend=""

def get_rand_string(n=128):
    return ''.join(random.choice(string.ascii_uppercase + \
                                 string.ascii_lowercase + \
                                 string.digits + ' ') for _ in range(n))


def put_test(n=10000, n_key=128, n_val=128, IP=None):
   global msgAppend
   for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, o_val = put(key, value)
        if r==-1:
            testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(n_key)+"_v-"+str(n_val)+".perf" 
            msg(0, opType, msgAppend+"Starting test: "+testName, "localhost", "test")
            print "SERVER CRASHED CRASHED!!!!!"
            time.sleep(1)

def get_test(n=10000, n_key=128, n_val=128, IP=None):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = get(key)

def delete_test(n=10000, n_key=128, n_val=128, IP=None):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = delete(key)


def load_test(args):
    put_test(10000);
    pass

if __name__ == "__main__":
    serverUrl=sys.argv[1]
    if PERF_TEST_SERVER:
        serverUrl="localhost"
    init(serverUrl)
    logParentDir = 'log'
    perfResFile=logParentDir+"/perf_result.csv"
    if not os.path.isdir(logParentDir):
        print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|creating log dir")
        try:
            os.makedirs(logParentDir)
            print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log folder created: " + logParentDir)
        except:
            print(getTime() + "|ERROR|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|log  folder could not be created at " + logParentDir)
    if not perfResultObj:
        if not os.path.exists(perfResFile):
            print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|creating daily log file: " + perfResFile)
            try:    
                perfResultObj = open(perfResFile, "a")
                print(getTime() + "|INFO|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|daily log file created: " + perfResFile)
            except: 
                print(getTime() + "|ERROR|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|daily log file " + perfResFile + " cannot be created!!!")
    try:
         perfResultObj = open(perfResFile, "a")
    except:
         print(getTime() + "|ERROR|" + str(os.getpid()) + "|" + myIP + "|" + opType + "|daily log file " + perfResFile + " cannot be accessed")

    call = ['get','put','delete']
    num = [1,2,4,8,16,32,64,128,256,516,1024]
    k_size = [1,64,128]
    v_size = [1,1024,2048]
    msgAppend="["+serverUrl+"] "
    for n in num:
        for k in k_size:
             for v in v_size:
                 for t in call:
                     try:
                         testName=t+"_test("+str(n)+","+str(k)+","+str(v)+")"
                         testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(k)+"_v-"+str(v)+".perf" 
                         msg(0, opType, msgAppend+"Starting test: "+testName, myIP, "test")
                         #cProfile.run(testName) #,testFileName)
                         tm = timeit.timeit(stmt=testName, number=1, setup='from __main__ import get_test, put_test, delete_test')
                         perfResultObj.write(getTime()+","+t+","+myIP+","+serverUrl+","+str(n)+","+str(k)+","+str(v)+","+str(tm)+","+str(tm/n)+"\n")
			 msg(0, opType, msgAppend+"Test completed: "+testName, myIP, "test")
                         msg(0, opType, msgAppend+"Time taken: "+testName+": " + str(tm), myIP, "test")
                     except:
                         msg(1, opType, msgAppend+"Unexcepted failure with test: "+testName, myIP, "test")
