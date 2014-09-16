import urllib2
import json
import os, sys
import urllib
import requests 

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
			value = sys.stdin.readline()
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
	UI(sys.argv)
		
	
