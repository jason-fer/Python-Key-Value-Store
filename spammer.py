import urllib2
import json
import os, sys
import urllib
import requests 
import time
import datetime
import string
import random

# current time for logging
def getTime():
	ts = time.time()
	dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S:%f')
	return dt


url = None
def get_url(l_url=None):
	global url
	if url: return
	if not l_url:
		l_url = raw_input("\nServer:  <IP>:<port>\n")
	# check ip_port format
	if not l_url.startswith('http'):
		l_url = "http://%s" % ( l_url )
	url = l_url


def kv739_init(url):
	try:
		urllib2.urlopen(url)
		return 0 # success
	except urllib2.HTTPError, e:
		if e.code==500:
			return 0
	except urllib2.URLError, e:
		print('URLError', e.args)
	return -1 # failure

def kv739_get(key):
	data = {'key' : key}
	url_values = urllib.urlencode(data)
	full_url = '%s?%s' % (url, url_values)
	try:
		d = requests.get(full_url)
		if d.status_code == 404:
			return 1, None # the key does not exist
		elif d.status_code == 200:
			r = json.loads(d.content)
			value = r.get('value', '')
			return 0, value
		elif d.status_code == 500:
			return -1, "ERROR!" 
	except requests.ConnectionError, e:
		return -1, "ERROR: %s" % e.error


def kv739_put(key, value):
	data = {'key' : key, 'value': value}
	enc_data = urllib.urlencode(data)
	ret = requests.put(url, data);
	old_value = ''			
	if ret.status_code == 500:
		return -1
	elif ret.status_code == 200:
		r = json.loads(ret.content)
		try:
			old_value = r['old_value']
			return 0, old_value
		except KeyError:
			print "What the fuck server. Bitch/Son of a bitch!! "
			return -1, ''
	elif ret.status_code == 201:
		return 1, old_value
	else:
		print "WTF!!!"
		return -1, old_value

def kv739_delete(key):
	data = {'key' : key}
	url_values = urllib.urlencode(data)
	full_url = '%s?%s' % (url, url_values)
	try:
		d = requests.delete(full_url)
		if d.status_code == 404:
			return 1, None # the key does not exist
		elif d.status_code == 200:
			r = json.loads(d.content)
			value = r.get('value', '')
			return 0, value
		elif d.status_code == 500:
			return -1, "ERROR!"
	except requests.ConnectionError, e:
		return -1, "ERROR: %s" % e.error
	
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
	k = 0
	while (1):
		k = k + 1
		value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
		value = 'value_inserted_by_SRG_THE_GREAT: >>> ... ' + value + '...' + str(k) + '...PS:Saikat is the best Fantasy Football Player!!!'
		key = 'SRG_THE_GREAT@' + getTime()
		key = k
		ret, o_val = kv739_put(key, value)
		if ret not in [0, 1]:
			print "error"
		elif ret == 0:
			print "Updated key\nKey:", key
			print "Old Value:", o_val
			print "New Value:", value
		else:
			print "Inserted key\Key:", key
			print "New Value:", value
		if k % 5000 == 0:
			print "Done Inserting 1000 values"
			exit(0)



if __name__ == "__main__":
	UI(sys.argv)
		
	
