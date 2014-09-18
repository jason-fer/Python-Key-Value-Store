import client
import os,sys, timeit
import random
import time
from config import *
import string


inp_file_name = 'thesis.txt'

def get_rand_string(n=128):
    return ''.join(random.choice(string.ascii_uppercase + \
                                 string.ascii_lowercase + \
                                 string.digits + ' ') for _ in range(n))
    


def put_test(n=10000, n_key=128, n_val=128):
    f = open(inp_file_name)
    for i in xrange(n):
        # s = f.read(1000);
        # s.replace('\r', '')
        # s.replace('\n', '')
        # key = s[:128]
        # value = s[128:]
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, o_val = client.kv739_put(key, value)
        if r==-1:
            print "SERVER CRASHED CRASHED!!!!!"
            time.sleep(1)
        print i, r, o_val

def get_test(n=10000):
    f = open(inp_file_name)
    for i in xrange(n):
        # S = f.read(1000);
        # s.replace('\r', '')
        # s.replace('\n', '')
        # key = s[:128]
        # value = s[128:]
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_get(key, value)
        print r, val

def del_test(n=10000):
    f = open(inp_file_name)
    for i in xrange(n):
        # s = f.read(1000);
        # s.replace('\r', '')
        # s.replace('\n', '')
        # key = s[:128]
        # value = s[128:]
        key, value = get_rand_string(n_key), get_rand_string(n_val)
        r, val = client.kv739_delete(key, value)
        print r, val


def load_test(args):
    put_test(10000);
    pass

def UI(args):
    global url
    if len(args)>1:
        get_url(args[1])
    else:
        get_url()
        print url
    con = kv739_init(url)
    if con==-1:
        print "Connection refused!"
        exit(0);
    else:
        print "Connection successful!"
        
            
    while(1):
        cmd = raw_input("cmd: [G]et/[P]ut/[Q]uit/[D]elete: ")
        if cmd.upper() == 'G':
            key = raw_input( "Key: " )
            print "Key:", key 
            r, val = kv739_get(key)
            print "Code:", r
            print "Value:", val
        elif cmd.upper() == 'P':
            key = raw_input( "Key: " )
            print "Values:",
            value = sys.stdin.readline().strip()
            ret, o_val = kv739_put(key, value)
            if ret not in [0,1,-1]:
                print "Wrong return value:", ret
            elif ret == 0:
                print "Updated Key\nKey:", key 
                print "Old Value:", o_val
                print "New Value:", value
            else:
                print "Inserted Key\nKey:", key 
                print "New Value:", value
        elif cmd.upper() == 'D':
            key = raw_input( "Key: " )
            print "Key:", key 
            ret, o_val = kv739_delete(key)
            # delete the shit
            print "Code:", ret
            if ret == 200:
                print "O_Val:", o_val
        elif cmd.upper() == 'Q':
            print 
            exit(0)


if __name__ == "__main__":
    client.kv739_init(sys.argv[1])
    put_test(100)
    #UI(sys.argv)
		
	
