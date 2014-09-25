'''Client classes'''

import requests 
from hash_ring import HashRing

# Confirm this with Jason and Brandon
GET_codes = {200:0, 404:1, 500:-1}
PUT_codes = {200:0, 201:1, 500:-1}
DEL_codes = {200:0, 404:1, 500:-1}

servers = [
	'127.0.0.1:5000',
	'127.0.0.1:5001',
]

class Client: 
	"""Abstract base client class."""
	def get(self, key):
		r = requests.get('%s/?key=%s' % (self.base_url(key), key))
		if r.status_code == 500:
			raise Exception('Error during GET : ' + str(r.json().get('errors')))
		ret = (GET_codes[r.status_code], r.json().get('value'))
		return ret

	def put(self, key, value):
		payload = {'key':key, 'value':value}
		r = requests.put(self.base_url(key), data=payload)
		if r.status_code == 500:
			raise Exception('Error during PUT : ' + str(r.json().get('errors')))
		ret = (PUT_codes[r.status_code], r.json().get('old_value'))
		return ret

	def delete(self, key):
		payload = {'key':key}
		r = requests.delete(self.base_url(key), data=payload)
		if r.status_code == 500:
			raise Exception('Error during DELETE : ' + str(r.json().get('errors')))
		ret = (DEL_codes[r.status_code], r.json().get('old_value'))
		return ret

class SingleServerClient(Client): 
	"""Client that connects to a single server"""
	def __init__(self, address='127.0.0.1:5000'):
		self.address = address

	#################### PRIVATE FUNCTIONS ####################
	def base_url(self, key):
		return 'http://%s' % self.address

class MultiserverClient(Client): 
	"""Client that connects to multiple servers"""
	def __init__(self, servers=servers):
		self.servers = servers
		self.ring = HashRing(servers)

	#################### PRIVATE FUNCTIONS ####################
	def base_url(self, key):
		server = self.ring.get_node(key)
		# print "Using server ", server, " for key ", key
		return 'http://%s' % (server)


