import urllib2
import json
import os, sys
import urllib
import requests 
from config import *
import client

def get_url(l_url=None):
	global url
	if url: return
	if not l_url:
		l_url = raw_input("\nServer:  <IP>:<port>\n")
	# check ip_port format
	if l_url.startswith('http'):
		l_url = "http://%s" % ( l_url )
        url = l_url

url = None
def UI(args):
	global url
	if len(args)>1:
		get_url(args[1])
	else:
		get_url()
	print url
	con = client.kv739_init(url)
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
			r, val = client.kv739_get(key)
			print "Code:", r
			print "Value:", val
		elif cmd.upper() == 'P':
			key = raw_input( "Key: " )
			print "Values:",
			value = sys.stdin.readline().strip()
			ret, o_val = client.kv739_put(key, value)
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
			ret, o_val = client.kv739_delete(key)
			# delete the shit
			print "Code:", ret
			if ret == 200:
				print "O_Val:", o_val
		elif cmd.upper() == 'Q':
			print 
			exit(0)

if __name__ == "__main__":
	UI(sys.argv)
