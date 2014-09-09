from flask import Flask
from flask import request
import json
import dbWorkers
get_from_db = dbWorkers.get
put_in_db = dbWorkers.put

app = Flask(__name__)

#@todo: json encode / decode payload

dbWorkers.startConnection()

def get_value():
	key = request.args.get('key', '');
	return dbWorkers.get(key)

def create_value():
	key = request.form['key'];
	value = request.form['value'];

	if not key or not value: 
		return json.dumps({'status': 'error', 'message': 'get() requires a key'})

	return dbWorkers.put(key, value)

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		key = request.args.get('key', '');
		return json.dumps({'key': key, 'value': get_from_db()})

  elif  request.method == 'POST':
    key = request.form.get('key', '')
    value = request.form.get('value', '')
    d  = {'return': -1, 
          'value': "",
          'old_value': ""}
    if not key or not value:
      return d
    o_val = get_from_db(key)
    d['return'] = 0 if o_val else 1
    ret = put_in_db(key, value)
    return json.dumps(d)
  else:
    return json.dumps({'status': 'error', 'message': 'only GET or POST are valid methods'})

if __name__ == "__main__":
  app.debug = True
  app.run()
