from flask import Flask
from flask import request
import json
import dbWorkers
get_from_db = dbWorkers.get
put_in_db = dbWorkers.put

app = Flask(__name__)

def get_value():
	key = request.args.get('key', '');
	return get_from_db(key)

def create_value():
	key = request.form.get('key', '')
	value = request.form.get('value', '')

	if not key or not value: 
		return {'status': 'error', 'message': 'get() requires a key'}

	old_value = get_from_db(key)

	data = {'return': -1, 
				'key': key,
				'value': value,
				'old_value': old_value}

	data['return'] = 0 if old_value else 1

	put_in_db(key, value)

	return data;

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		key = request.args.get('key', '');
		return json.dumps({'key': key, 'value': get_from_db(key)})

	elif  request.method == 'POST':
		return json.dumps(create_value())

	else:
		return json.dumps({'status': 'error', 'message': 'only GET or POST are valid methods'})

if __name__ == "__main__":
	app.debug = True
	app.run()
