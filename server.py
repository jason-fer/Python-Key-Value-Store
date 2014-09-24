from flask import Flask, request, json
import os, sys
sys.path.append(os.getcwd()+'/lib')
import dbWorkers, cache

from config import *
# 500: error
# 404: key doesn't exist
# 200: key exists
# 201: key created 

get_from_db = cache.get
put_in_db = cache.put
delete_in_db = cache.delete

app = Flask(__name__)

client_ip = ''
def check_key(method_name, key):
	# throw error if there's no key
	if not key: 
		return  False, {'errors': [ method_name + ' requires a key']}

	# throw error if key exceeds length limits
	key_length = len(key.encode('utf-8'))
	if key_length > 128 and '[' not in key and ']' not in key:
		return  False, {'errors': [ method_name + ' key was ' 
		+  str(key_length) + ' bytes. This exceeds the 128 byte limit'] }

	# the key is OK
	return True, ''

def check_value(method_name, value):
	# throw error value not present
	if not value: 
		return  True, ''

	# throw error if value exceeds length limits
	value_length = len(value.encode('utf-8'))
	if value_length > 2048  and '[' not in value and ']' not in value:	
		return  False, {'errors': [ method_name + ' value was ' 
		+ str(value_length) + ' bytes. This exceeds the 2048 byte limit'] }

	# the value is OK
	return True, ''

def delete_value():
	key = request.form.get('key', '')

	#check the key
	ok, error_message = check_key('delete()', key)
	if not ok:
		return error_message, 500

	status, old_value = delete_in_db(key)

	# system error = 500 server error
	# key wasn't present = 201 created (insert)
	if status == 1 or status == 0:
		return  {'old_value': old_value}, 200
	else: #status == -1
		return  {'errors': [ 'unknown database error'] }, 500

def get_value():
	client_ip = request.remote_addr
	key = request.args.get('key', '');
	#check the key
	ok, error_message = check_key('get()', key)
	if not ok:
		# 500 = error
		return error_message, 500

	# retrieve the value
	status, value = get_from_db(key, client_ip);

	# key wasn't present = 404 not found
	if status == 1:
		return  {'value': '', 'errors': [ 'key not found'] }, 404
	# system error = 500 server error
	elif status == -1:
		return  {'value': value, 'errors': [ 'unknown database error'] }, 500
	# key was present = 200 ok
	else:
		return  {'value': value }, 200

def put_value():
	client_ip = request.remote_addr
	key = request.form.get('key', '')
	if not key:
		# this is just a backup since this is incorrect
		key = request.args.get('key', '')
	value = request.form.get('value', '')

	#check the key
	ok, error_message = check_key('put()', key)
	if not ok:
		return error_message, 500

	#check the value
	ok, error_message = check_value('put()', value)
	if not ok:
		return error_message, 500

	status, old_value = put_in_db(key, value, client_ip);

	# key wasn't present = 201 created (insert)
	if status == 1:
		return  {'value': value}, 201
	# system error = 500 server error
	elif status == -1: 
		return  {'value': value, 'errors': [ 'unknown database error'] }, 500
	# key was present = 200 ok (update)
	else:
		return  {'value': value, 'old_value': old_value}, 200

def delete_key():
	client_ip = request.remote_addr
	key = request.form.get('key', '')
	if not key:
		# this is just a backup since this is incorrect
		key = request.args.get('key', '')
	#check the key
	ok, error_message = check_key('delete()', key)
	if not ok:
		# 500 = error
		return error_message, 500

	# retrieve the value
	status, value = delete_in_db(key, client_ip);

	if status == 1 or status == 0:
		return  {'old_value': value }, 200
	# system error = 500 server error
	else:
		return  {'old_value': value, 'errors': [ 'unknown database error'] }, 500
	
@app.route('/', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def main():
	if request.method == 'GET':
		data, http_status = get_value() 
		return json.dumps(data), http_status

	elif request.method == 'PUT':
		data, http_status = put_value()
		return json.dumps(data), http_status

	if request.method == 'DELETE':
		data, http_status = delete_key() 
		return json.dumps(data), http_status

	if request.method == 'OPTIONS':
		key = request.args.get('heartbeat', '');
		if key:
			return json.dumps({'heartbeat':'I am alive!!!'}), 200
		else:
			allowed_methods = {
				'HTTP GET': [
					{'arguments':'(string) key'},
					{'description':'retrieve the value of a key'},
					{'HTTP Status':'404 (key not found), 200 (key found), 500 (server error)'},
					{'returns':'(string) value'},
				],
				'HTTP PUT': [
					{'arguments':'(string) key, (string) value'},
					{'description':'set the value of a key'},
					{'HTTP Status':'201 (created), 200 (updated), 500 (server error)'},
					{'returns':'(string) old_value, only on HTTP Status 200'},
				],
				'HTTP DELETE': [
					{'arguments':'(string) key'},
					{'description':'invalidate a key / value'},
					{'HTTP Status':'200 (deleted), 500 (server error)'},
					{'returns':'(string) value'},
				],
				'HTTP OPTIONS (heartbeat)': [
					{'arguments':'(string) key'},
					{'description':'pass the query string <url>?heartbeat=true'},
					{'HTTP Status':'200 (server is alive), 500 (server error)'},
					{'returns':'(JSON) {\'heartbeat\':\'I am alive!!!\'}'},
				],
				'HTTP OPTIONS': [
					{'arguments':'None'},
					{'description':'View arguments for all possible HTTP REQUEST methods'},
					{'HTTP Status':'200 (server is alive), 500 (server error)'},
					{'returns':'descriptions for all methods.'},
				],
			}
			return json.dumps(allowed_methods), 200
	else:
		return json.dumps({'errors':['Not implemented']}), 405


if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0')
