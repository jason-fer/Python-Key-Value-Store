#only for testing our own server 
#more robust tests that check more data than the client is able to return
#these tests wont work right vs someone else's server.
import urllib2, json, os, sys, urllib, unittest, string, random, requests

def random_string(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_url(url=None):
	if not url:
		url = raw_input("\nServer:  <IP>:<port>\n")
	# check ip_port format
	if not url.startswith('http'):
		url = "http://%s" % ( url )
	return url

def send(url, data=None ):
	try:
		if data:
			opener = urllib2.build_opener(urllib2.HTTPHandler)
			request = urllib2.Request(url, data=data)
			request.add_header('Content-Type', 'application/x-www-form-urlencoded ')
			request.get_method = lambda: 'PUT'
			d = opener.open(request)
			j = json.loads(d.read())
		else:
			d = urllib2.urlopen(url)
			j = json.loads(d.read())

		# print ">>>> Server's response:", j
		return j
	except urllib2.HTTPError as e:
		# print e.read()
		return e.code

def get(key, url=None):
	if not url:
		get_url(url)
	data = {'key' : key}
	url_values = urllib.urlencode(data)
	full_url = '%s?%s' % (url, url_values)
	return send(full_url)

def put(key, value, url=None):
	if not url:
		get_url(url)
	data = {'key' : key, 'value': value}
	enc_data = urllib.urlencode(data)
	return send(url, enc_data)

def test_has_property(rs, tc, prop):
	if rs.get(prop) == None:
		return False

	return True

def test_has_right_val(rs, tc, prop, val):
	should_equal = rs.get(prop)
	if should_equal == None:
		return False

	# print 'Does val:' + should_equal + '\n==\n' + val
	return should_equal == val

def test_has_error(rs, tc, should):
	status = rs.get('return')

	if should:
		tc.assertEqual(status, -1)
		return True
	else:
		if status == 0 or status == 1:
			return True
		else:
			return False

def test_get(url, tc):
	print '\nChecking to see get result has a key'
	rs = get('1', url)
	test_has_property(rs, tc, 'key')

	print '\nChecking a get with a blank key'
	rs = get('', url)
	tc.assertEqual(rs, 500)

	print '\nChecking a get with a key over 128 bytes'
	rs = get(random_string(129), url)
	tc.assertEqual(rs, 500)

def test_put(url, tc):

	count = 0
	maxCount = 3
	print '\nRunning '+ str(maxCount * 6) +' random key and value updates'
	while count < maxCount:
		# first group of tests
		# print '\nChecking a random key and value'
		key = random_string(20)
		value = random_string(200)
		rs = put(key, value, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		# print 'Confirm we can get() the value we just put()'
		rs = get(key, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		# print 'Confirm we can update the value we just put()'
		value = random_string(200)
		rs = put(key, value, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		# second group of tests
		# print '\nChecking a max length key and value'
		key = random_string(128)
		value = random_string(2048)
		rs = put(key, value, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		# print 'Confirm we can get() the value we just put()'
		rs = get(key, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		# print 'Confirm we can update the value we just put()'
		value = random_string(2048)
		rs = put(key, value, url)
		tc.assertTrue(test_has_right_val(rs, tc, 'value', value))

		count += 1

	# third group of tests
	print '\nChecking a key that is too big'
	key = random_string(129)
	value = random_string(2047)
	rs = put(key, value, url)
	tc.assertEqual(rs, 500)
	# tc.assertTrue(test_has_error(rs, tc, True))

	print '\nChecking a val that is too big'
	key = random_string(127)
	value = random_string(2049)
	rs = put(key, value, url)
	tc.assertEqual(rs, 500)
	# tc.assertTrue(test_has_error(rs, tc, True))

	print '\nChecking an empty key'
	key = ''
	value = random_string(2047)
	rs = put(key, value, url)
	tc.assertEqual(rs, 500)
	# tc.assertTrue(test_has_error(rs, tc, True))

	print '\nChecking an empty val'
	key = random_string(127)
	value = ''
	rs = put(key, value, url)
	tc.assertEqual(rs, 500)
	# tc.assertTrue(test_has_error(rs, tc, True))
	return True

def UI(args):
	if len(args)>1:
		url = get_url(args[1])
	else:
		url = get_url()
	print "server url:" +url

	tc = unittest.TestCase('__init__')

	print '\n+-------------------------------+'
	print '>>>> Run get() tests!!!!!! <<<<'
	print '+-------------------------------+'

	test_get(url, tc)

	print '\n+-------------------------------+'
	print '>>>> Run put() tests!!!!!! <<<<'
	print '+-------------------------------+'

	test_put(url, tc)

	print '\n>>>> All tests pass!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <<<<\n'
	## try HTTP delete / put (both should throw errors)
	
	exit(0)

if __name__ == "__main__":
	UI(sys.argv)
		
	
