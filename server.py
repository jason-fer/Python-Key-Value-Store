from flask import Flask, request, json
import dbWorkers

get_from_db = dbWorkers.get
put_in_db = dbWorkers.put
app = Flask(__name__)

def check_key(method_name, key):
	# throw error if there's no key
	if not key: 
		return  False, {'return': -1, 'errors': [ method_name + ' requires a key']}

	# throw error if key exceeds length limits
	key_length = len(key.encode('utf-8'))
	if key_length > 128:
		return  False, { 'return': -1, 'errors': [ method_name + ' key was ' 
		+  str(key_length) + ' bytes. This exceeds the 128 byte limit'] }

	# the key is OK
	return True, ''

def check_value(method_name, value):
	# throw error value not present
	if not value: 
		return  False, { 'return': -1, 'errors': [ method_name + ' requires a value'] }

	# throw error if value exceeds length limits
	value_length = len(value.encode('utf-8'))
	if value_length > 2048:	
		return  False, { 'return': -1, 'errors': [ method_name + ' value was ' 
		+ str(value_length) + ' bytes. This exceeds the 2048 byte limit'] }

	# the value is OK
	return True, ''

def get_value():
	key = request.args.get('key', '');

	#check the key
	ok, error_message = check_key('get()', key);
	if not ok:
		return error_message

	# retrieve the value
	status, value = get_from_db(key);

	return  {'return': status, 'key': key, 'value': value }

def put_value():
	key = request.form.get('key', '')
	value = request.form.get('value', '')

	#check the key
	ok, error_message = check_key('put()', key);
	if not ok:
		return error_message

	#check the value
	ok, error_message = check_value('put()', value);
	if not ok:
		return error_message

	status, old_value = put_in_db(key, value);

	data = {'return': status, 'key': key, 'value': value, 'old_value': old_value}

	return data;

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return json.dumps(get_value()) 

	elif  request.method == 'POST':
		return json.dumps(put_value())

	else:
		return json.dumps({'status': 'error', 'message': 'GET and POST are the only allowed HTTP methods'})

if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0')
