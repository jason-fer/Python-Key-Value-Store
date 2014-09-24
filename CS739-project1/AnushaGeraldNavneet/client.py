from client_class import SingleServerClient, MultiserverClient
from sanitychecks import *
from requests.exceptions import ConnectionError
import string

# global client object 
global_client = SingleServerClient()

global_PRINT_ERRORS = True

def catch_errors(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except (InputKeyError, InputValueError) as e:
			if global_PRINT_ERRORS:
				print 'Error in key or value: ', e
			return (-1, None)
		except ConnectionError as e:
			if global_PRINT_ERRORS:
				print 'No connection to server! Error was: ', e
			return (-1, None)
		except Exception as e:
			if global_PRINT_ERRORS:
				print 'Some error occurred: ', e
			return (-1, None)
	return wrapper

@catch_errors
def kv739_init(server_address, print_errors=True):
	global global_PRINT_ERRORS
	global_PRINT_ERRORS = print_errors

	global global_client
	global_client = SingleServerClient(server_address)

	try:
		global_client.get('dummykey')
	except ConnectionError as e:
		print 'Could not get a connection! Error was: ', e
		return -1
	except Exception as e:
		raise e

@catch_errors
def kv739_get(key):
	sanitycheck_key(key)
	return global_client.get(key)

@catch_errors
def kv739_put(key, value):
	sanitycheck_key(key)
	sanitycheck_value(value)
	return global_client.put(key,value)

@catch_errors
def kv739_delete(key):
	sanitycheck_key(key)
	return global_client.delete(key)

if __name__ == "__main__":
	# Should we run tests here?
	pass