import urllib2
import json
import os, sys
import urllib
import time
import datetime
import string
import random


# current time for logging
def getTime():
        ts = time.time()
        dt=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S:%f')
        return dt


def get_url(url=None):
	if not url:
		url = raw_input("\nServer:  <IP>:<port>\n")
	# check ip_port format
	if not url.startswith('http'):
		url = "http://%s" % ( url )
	return url;

def send( url, data=None ):
	try:
		if data:
			d = urllib2.urlopen(url, data)
		else:
			d = urllib2.urlopen(url)
		j = json.loads(d.read())
		#print "SRG D-",d
		#print "\n>>>> Server's response:", j
		return j
	except urllib2.HTTPError as e:
		print e.code
		print e.read()

	
def get(key, url=None):
	if not url:
		get_url(url);
	data = {'key' : key}
	url_values = urllib.urlencode(data)
	full_url = '%s?%s' % (url, url_values)
	ret = send(full_url)
	#print "URL: ",full_url
	return ret.get('value',  '')

def put(key, value, url=None):
	if not url:
		get_url(url);
	data = {'key' : key, 'value': value}
	enc_data = urllib.urlencode(data)
	#req = urllib2.Request(url, enc_data)
	print url
	ret = send(url, enc_data);
	return ret.get('old_value',''), ret.get('return', 0)


def UI(args):
	if len(args)>1:
		url = get_url(args[1])
	else:
		url = get_url()
	print url

	while(1):
		cmd = raw_input("cmd: [G]et/[P]ut/[Q]uit: ")
		if cmd.upper() == 'G':
			key = raw_input( "Key: " )
			print "Key:", key 
			print "Value:", get(key, url)
		elif cmd.upper() == 'P':
			key = raw_input( "Key: " )
			print "Values:",
			value = sys.stdin.readline()
			o_val, ret = put(key, value, url)
			if ret not in [0,1]:
				print "Wrong return value:", ret
			elif ret == 0:
				print "Updated Key\nKey:", key 
				print "Old Value:", o_val
				print "New Value:", value
			else:
				print "Inserted Key\nKey:", key 
				print "New Value:", value
		elif cmd.upper() == 'Q':
			print 
			exit(0)
def srgUI(args):	
        if len(args)>1:
                url = get_url(args[1])
        else:
                url = get_url()
        print url
	k=0	
	while(1):
		k=k+1
		value=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
		value='value_inserted_by_SRG_THE_GREAT: >>> ... '+value+'...'+str(k)+'...PS:Saikat is the best Fantasy Football Player!!!'
		key='SRG_THE_GREAT@'+getTime()
                #key=k
		o_val, ret = put(key,value,url)
		if ret not in [0,1]:
			print "error"
		elif ret == 0:
			print "Updated key\nKey:",key
			print "Old Value:", o_val
			print "New Value:", value
		else:
			print "Inserted key\Key:", key
			print "New Value:", value
		if k%1000==0:
			print "Done Inserting 1000 values"
			exit(0)
			

if __name__ == "__main__":
	srgUI(sys.argv)
		
	
