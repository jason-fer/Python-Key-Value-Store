import random
import unittest
from client import *

global_server = 'localhost:5000' #'twostep.cs.wisc.edu:5000'
NUM_TEST_OPS = 100

class TestClientInterface(unittest.TestCase):
	def setUp(self):
		kv739_init(global_server, print_errors=False)

	def test_initialize(self):
		host, port = global_server.split(':')
		wrong_host = '%s:%d' % ('nonexistent', int(port))
		status = kv739_init(wrong_host)
		self.assertEquals(status, -1)
		wrong_port = '%s:%d' % (host, int(port)+1024)
		status = kv739_init(wrong_port)
		self.assertEquals(status, -1)

	def test_sanitycheck_key(self):
		invalid_keys = ('', 'a' * MAX_KEY_LENGTH + 'b', 'a[b', 'a]b', 'a[b]')
		for key in invalid_keys:
			self.assertRaises(InputKeyError, sanitycheck_key, key)
		for key in invalid_keys:
			status, val = kv739_get(key)
			self.assertEquals(status, -1, 'Invalid key "%s" did not cause return value -1.' % (key,))
			status, val = kv739_put(key,'dummy')
			self.assertEquals(status, -1, 'Invalid key "%s" did not cause return value -1.' % (key,))
			status, val = kv739_delete(key)
			self.assertEquals(status, -1, 'Invalid key "%s" did not cause return value -1.' % (key,))

	def test_sanitycheck_value(self):
		invalid_values = ('', 'a' * MAX_VALUE_LENGTH + 'b', 'a[b', 'a]b', 'a[b]')
		for value in invalid_values:
			self.assertRaises(InputValueError, sanitycheck_value, value)
		for key in invalid_values:
			status, val = kv739_put('dummy',value)
			self.assertEquals(status, -1, 'Invalid value "%s" did not cause return value -1.' % (value,))

	def test_operations(self):
		random.seed(2)
		for _ in xrange(NUM_TEST_OPS):
		  key   = str(random.randint(0,9)) * random.randint(1,MAX_KEY_LENGTH)
		  value = str(random.randint(0,9)) * random.randint(1,MAX_VALUE_LENGTH)
		  new_value = 'new_' + value
		  new_value = new_value[:MAX_VALUE_LENGTH]		#truncate to max_length

		  kv739_delete(key)

		  status, old_val = kv739_put(key, value)
		  self.assertEqual(status, 0)

		  status, old_val = kv739_put(key, new_value)
		  self.assertEqual(status, 1)
		  self.assertEqual(old_val, value)

		  status, val = kv739_get(key)
		  self.assertEqual(status, 0)
		  self.assertEqual(val, new_value)

		  status, old_val = kv739_delete(key)
		  self.assertEqual(status, 0)
		  self.assertEqual(old_val, new_value)

		  status, val = kv739_get(key)
		  self.assertEqual(status, 1)

		  status, old_val = kv739_delete(key)
		  self.assertEqual(status, 0)

def run_test():
	unittest.main()

if __name__ == "__main__":
	run_test()