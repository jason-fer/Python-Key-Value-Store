import os,sys, timeit
sys.path.append(os.getcwd())

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


def put_test(n=10000, s_key=128, s_val=128, IP=None, **kwargs):
    global msgAppend
    for i in xrange(n):
        key, value = get_rand_string(s_key), get_rand_string(s_val)
        t1=time.time()
        r, o_val = put(key, value)
        t2=time.time()
        if r==-1:
            testName="put_n-%d_k-%d_v-%d" % (n, s_key, s_val)
            msg(1, opType, msgAppend+"Server crashed. Test="+testName+" n="+str(i), "localhost", "test")
            time.sleep(1)
        else:
            t="{0:.6f}".format(t2-t1)
            perfResultObj.write(getTime()+",put,localhost,"+serverUrl+","+str(n)+","+str(s_key)+","+str(s_val)+","+str(s_key+s_val)+","+str(t)+"\n")

def get_test(n=10000, s_key=128, s_val=128, IP=None):
    for i in xrange(n):
        key, value = get_rand_string(s_key), get_rand_string(s_val)
        t1=time.time()
        r, val = get(key)
        t2=time.time()
        if r==-1:
            testName="get_n-"+str(n)+"_k-"+str(s_key)+"_v-"+str(s_val)  
            msg(1, opType, msgAppend+"Server crashed. Test="+testName+" k="+key, "localhost", "test")
            time.sleep(1)
        else:
            t="{0:.6f}".format(t2-t1)
            perfResultObj.write(getTime()+",get,localhost,"+serverUrl+","+str(n)+","+str(s_key)+","+str(s_val)+","+str(s_key+s_val)+","+str(t)+"\n")

def delete_test(n=10000, s_key=128, s_val=128, IP=None):
    for i in xrange(n):
        key, value = get_rand_string(s_key), get_rand_string(s_val)
        t1=time.time()
        r, val = delete(key)
        t2=time.time()
        if r==-1:
            testName="del_n-"+str(n)+"_k-"+str(s_key)+"_v-"+str(s_val)  
            msg(1, opType, msgAppend+"Server crashed. Test="+testName+" n="+str(i), "localhost", "test")
            time.sleep(1)
        else:
            t="{0:.6f}".format(t2-t1)
            perfResultObj.write(getTime()+",del,localhost,"+serverUrl+","+str(n)+","+str(s_key)+","+str(s_val)+","+str(s_key+s_val)+","+str(t)+"\n")

def wrapper(args):
    func, arg = args[0], args[1:]
    return func(*arg)

def throughput_test(func, n=10000, s_key=128, s_val=128, IP=None):
    from multiprocessing  import Pool
    pool_cnt = 20
    p = Pool(pool_cnt)
    per_pool_n = n/pool_cnt
    p.map(wrapper, [(func, 
                     per_pool_n,
                     s_key,
                     s_val,
                     IP) for x in xrange(pool_cnt)])
    
if __name__ == "__main__":
    NUM_OF_TRIALS=2
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
    #num = [1,2,4,8,16,32,64,128,256,516,1024]
    #k_size = [1,64,128]
    #v_size = [1,1024,2048]
    num = [2000]
    k_size = [1,32,64,96,128]
    v_size = [1,516,1024,1540,2048]

    msgAppend="["+serverUrl+"] "
    for x in range(1,NUM_OF_TRIALS+1):
        msg(0, opType, msgAppend+"Starting Trial #"+str(x), myIP, "test")
        for n in num:
             print "=="*30
             print("TRIAL: "+str(x)+" ... N="+str(n))
             for k,v in zip(k_size, v_size):
                 #for v in v_size:
                 for t in call:
                     try:
                         testName="throughput_test(%s_test, %d, %d, %d)" %(t, n, k, v)
                         testFileName=logParentDir+"/"+t+"_n-"+str(n)+"_k-"+str(k)+"_v-"+str(v)+".perf" 
                         msg(0, opType, msgAppend+"Starting test: "+testName, myIP, "test")
                             #cProfile.run(testName) #,testFileName)
                         tm = timeit.timeit(stmt=testName, number=1, 
                                            setup='from __main__ import get_test, put_test, delete_test, throughput_test ')
                             #perfResultObj.write(getTime()+","+t+","+myIP+","+serverUrl+","+str(n)+","+str(k)+","+str(v)+","+str(tm)+","+str(tm/n)+"\n")
                         print testName, tm
                         #msg(0, opType, msgAppend+"Test completed: "+testName, myIP, "test")
                         #msg(0, opType, msgAppend+"Time taken: "+testName+": " + str(tm), myIP, "test")
                         #print('.')
                     except KeyError:
                         msg(1, opType, msgAppend+"Unexcepted failure with test: "+testName, myIP, "test")
