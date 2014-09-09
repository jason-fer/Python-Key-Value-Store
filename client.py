import urllib2
import json
import os, sys
import urllib

def get_url():
	ip_port = raw_input("Server:  <IP>:<port>\n")
	# check ip_port format
	return ip_port;

def send( url, data=None ):
	try:
		if data:
			d = urllib2.urlopen(url, data)
		else:
			d = urllib2.urlopen(url)
		return json.loads(d.read())
	except urllib2.HTTPError as e:
		print e.code
		print e.read()

	
def get(key, url=None):
	if not url:
		get_url();
	data = {'key' : key}
	url_values = urllib.urlencode(data)
	full_url = 'http://%s?%s' % (url, url_values)
	print full_url
	ret = send(full_url)
	return ret.get('value',  '')

def put(key, value, url=None):
	if not url:
		get_url();
	data = {'key' : key, 'value': value}
	enc_data = urllib.urlencode(data)
	#req = urllib2.Request(url, enc_data)
	ret = send(url, enc_data);
	return ret.get('old_value',''), ret.get('return', 0)


def UI(args):
	if len(args)>1:
		url = args[1]
	else:
		url = get_url()
		
	if not url.startswith('http'):
		url = "http://%s" % ( url )

	while(1):
		cmd = raw_input("cmd: [G]et/[P]ut: ")
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
				

if __name__ == "__main__":
	UI(sys.argv)
		
	
