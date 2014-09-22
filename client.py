import urllib2
import json
import os, sys
import urllib
from config import *

url = None

def kv739_init(_url):
	global url

	pos = _url.find('http')
	if pos == -1:
		url = "http://%s" %_url
	else:
		url = _url

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
		r = urllib2.urlopen(full_url)
		content = r.read()
		status_code = r.getcode()
		if status_code == 404:
			return 1, None # the key does not exist
		elif status_code == 200:
			r = json.loads(content)
			value = r.get('value', '')
			return 0, value
		elif status_code == 500:
			return -1, "ERROR!" 
	except urllib2.HTTPError as e:
		# print e.read()
		return -1, "ERROR: %s" % e.code

def kv739_put(key, value):
	data = {'key' : key, 'value': value}
	status_code, content = http_put(url, data);
	if status_code == 500:
		return -1, ''
	elif status_code == 200:
		try:
			old_value = content['old_value']
			return 0, old_value
		except KeyError:
			print "Failure!!!"
			return -1, ''
	elif status_code == 201:
		return 1, ''
	else:
		print "Failure!!!"
		return -1, old_value

def kv739_delete(key):
	data = {'key' : key}
	try:
		status_code, content = http_delete(url, data)
		if status_code == 404:
			return 1, '' # the key does not exist
		elif status_code == 200:
			value = content.get('old_value', '')
			return 0, value
		elif status_code == 500:
			return -1, "ERROR!"
	except urllib2.HTTPError as e:
		# print e.read()
		return -1, "ERROR: %s" % e.code

def http_put(url, data):
	return send_request(url, 'PUT', data)

def http_delete(url, data):
	return send_request(url, 'DELETE', data)

def send_request(url, method, data):
	try:
		#Special formatting for PUT & DELETE HTTP request packet
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(url, data=urllib.urlencode(data))
		request.add_header('Content-Type', 'application/x-www-form-urlencoded')
		request.get_method = lambda: method
		response = opener.open(request)

		#decipher the response
		http_body = response.read()
		content = json.loads(http_body)
		status_code = response.getcode()
	except urllib2.HTTPError as e:
		content = e.read()
		status_code = e.code
	return status_code, content

