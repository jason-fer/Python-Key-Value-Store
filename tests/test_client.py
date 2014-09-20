#test any client, including our own.
import urllib2, json, os, sys, urllib, unittest, string, random, requests
sys.path.append("..")
import client

kv739_init = client.kv739_init #url
kv739_get = client.kv739_get #key
kv739_put = client.kv739_put #key, value
kv739_delete = client.kv739_delete #key

def random_string(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def get_url(url=None):
  if not url:
    url = raw_input("\nServer:  <IP>:<port>\n")
  # check ip_port format
  if not url.startswith('http'):
    url = "http://%s" % ( url )
  return url

def test_get(url, tc):
  print '\nChecking a get with a blank key'
  rs, error = kv739_get('')
  tc.assertEqual(rs, -1)

  print '\nChecking a get with a key over 128 bytes'
  rs, error = kv739_get(random_string(129))
  tc.assertEqual(rs, -1)

def check_last_put(tc, key, value):
    # print 'Confirm we can kv739_get() the value we just put()'
    rs, ret_val = kv739_get(key)
    tc.assertEqual(ret_val, value)
    tc.assertEqual(rs, 0)

def test_put(url, tc):

  count = 0
  maxCount = 50
  print '\nRunning '+ str(maxCount * 6) +' random key and value updates'
  while count < maxCount:
    # first group of tests
    
    # print '\nChecking a random key and value'
    key = random_string(20)
    value = random_string(200)
    rs, ret_val = kv739_put(key, value)
    tc.assertNotEqual(rs, -1)
    check_last_put(tc, key, value)

    # print 'Confirm we can update the value we just put()'
    value = random_string(200)
    rs, ret_val = kv739_put(key, value)
    tc.assertEqual(rs, 0) # the key should exist
    check_last_put(tc, key, value)

    # second group of tests
    # print '\nChecking a max length key and value'
    key = random_string(128)
    value = random_string(2048)
    rs, ret_val = kv739_put(key, value)
    tc.assertNotEqual(rs, -1)
    check_last_put(tc, key, value)

    # print 'Confirm we can update the value we just put()'
    value = random_string(2048)
    rs, ret_val = kv739_put(key, value)
    tc.assertEqual(rs, 0) # the key should exist
    check_last_put(tc, key, value)

    count += 1

  # third group of tests
  print '\nChecking a key that is too big'
  key = random_string(129)
  value = random_string(2047)
  rs, ret_val = kv739_put(key, value)
  tc.assertEqual(rs, -1)

  print '\nChecking a val that is too big'
  key = random_string(127)
  value = random_string(2049)
  rs, ret_val = kv739_put(key, value)
  tc.assertEqual(rs, -1)

  print '\nChecking an empty key'
  key = ''
  value = random_string(2047)
  rs, ret_val = kv739_put(key, value)
  tc.assertEqual(rs, -1)

  print '\nChecking an empty val'
  key = random_string(127)
  value = ''
  rs, ret_val = kv739_put(key, value)
  tc.assertEqual(rs, -1)
  return True

def UI(args):
  if len(args)>1:
    url = get_url(args[1])
  else:
    url = get_url()

  print '\n+-------------------------------+'
  print 'init server: kv739_init(' + url + ')'
  print '+-------------------------------+'

  tc = unittest.TestCase('__init__')
  tc.assertEqual(0, kv739_init(url));

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
    
  
