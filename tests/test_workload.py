#Simulate a workload that represents what a web-service workload might be
#in real life
# We think these may represent reasonable numbers for a real workload:
# 94% GET, 1% DELETE, 5% PUT (create / write)
# 90% of GETS will be requests that might possibly repeat, while 10% of GETs
# will be random / unexpected.
#For testing our client library as well as other client libraries.
import urllib2, json, os, sys, urllib, unittest, string, random

#sys.path.append(os.getcwd()+'/lib')
sys.path.append(os.getcwd() + '/CS739-project1/ArkoBrandonChaitan/')
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
    url = "http://%s" % (url)
  return url

def main(args):
  if len(args) > 1:
    url = get_url(args[1])
  else:
    url = get_url()

  print '\n+-------------------------------+'
  print 'init server: kv739_init(' + url + ')'
  print '+-------------------------------+'

  tc = unittest.TestCase('__init__')
  tc.assertEqual(0, kv739_init(url))

  print '\n+-------------------------------+'
  print '>>>> Run throughput tests!!!!!! <<<<'
  print '+-------------------------------+'

  key = random_string(100)
  value = random_string(400)
  rs, ret_val = kv739_put(key, value)
  tc.assertNotEqual(rs, -1)
  check_last_put(tc, key, value)


  print '\nChecking a get with a blank key'
  rs, error = kv739_get('')
  # -1 or 1 are OK, but 0 should never happen!
  tc.assertNotEqual(rs, 0)

  print '\nChecking a get with a key over 128 bytes'
  rs, error = kv739_get(random_string(129))
  tc.assertEqual(rs, -1)

  print '\n>>>> All tests pass!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <<<<\n'
  ## try HTTP delete / put (both should throw errors)
  exit(0)

if __name__ == "__main__":
  main(sys.argv)
    
  
