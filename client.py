import urllib2
import json
import os, sys
import urllib
import requests 
from config import *

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

def kv739_init(_url):
        get_url(_url)
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
		return -1, ''
	elif ret.status_code == 200:
		r = json.loads(ret.content)
		try:
			old_value = r['old_value']
			return 0, old_value
		except KeyError:
			print "Failure!!!"
			return -1, ''
	elif ret.status_code == 201:
		return 1, old_value
	else:
		print "Failure!!!"
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
			value = r.get('old_value', '')
			return 0, value
		elif d.status_code == 500:
			return -1, "ERROR!"
	except requests.ConnectionError, e:
		return -1, "ERROR: %s" % e.error


