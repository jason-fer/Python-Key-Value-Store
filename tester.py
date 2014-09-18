import client
import os,sys, timeit
import random
import time
from config import *
import string


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
        print i, r, o_val

def get_test(n=10000):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_get(key, value)
        print r, val

def del_test(n=10000):
    for i in xrange(n):
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_delete(key, value)
        print r, val


def load_test(args):
    put_test(10000);
    pass

if __name__ == "__main__":
    client.kv739_init(sys.argv[1])
    put_test(100)
    #UI(sys.argv)
		
	
