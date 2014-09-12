from flask import Flask
from flask import request
import json
import dbWorkers
get_from_db = dbWorkers.get
create_in_db = dbWorkers.put
update_in_db = dbWorkers.put

#insert can't insert an empty value (this will prevent errors)

app = Flask(__name__)

def get_value():
	key = request.args.get('key', '');
	# assume present
	status = 1;

	if not key:
		# not present
		status = 1;
	ret, value = get_from_db(key)
	return  {
		'return': status,
		'key': key,
		'value': value
		}

def create_value():
	key = request.form.get('key', '')
	value = request.form.get('value', '')
	status = -1

	if not key or not value: 
		return  {
			'return': status,
			'errors': [
				'get() requires a key'
				]
			}

	ret, old_value = get_from_db(key)

	if not old_value:
		#1 = the key was not present
		status = 1
		create_in_db(key, value)
	else:
		#0 = the key was present
		status = 0
		update_in_db(key, value)

	data = {
		'return': status, 
		'key': key,
		'value': value,
		'old_value': old_value
		}

	return data;

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return json.dumps(get_value()) 
	elif  request.method == 'POST':
		return json.dumps(create_value())
	else:
		return json.dumps({'status': 'error', 'message': 'only GET and POST are valid methods'})

if __name__ == "__main__":
	app.debug = True
	app.run()
