import urllib2
import json
import os, sys
import urllib
import requests 

url = None

def kv739_init(_url):
	global url

	pos = _url.find('http')
	if pos == -1:
		url = "http://%s" %_url
	else:
		url = _url
        return 0
	try:
		urllib2.urlopen(url)
		return 0 # success
	except urllib2.HTTPError, e:
		if e.code==500:
			return 0 # ignore this issue?
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
                else:
                        return -1, "WTF!!!!"
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
	enc_data = urllib.urlencode(data)
	try:
		d = requests.delete(url, data={'key' : key})
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


