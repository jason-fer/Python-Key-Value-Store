from flask import Flask
from flask import request
import dbWorkers
app = Flask(__name__)

#@todo: json encode / decode payload

dbWorkers.startConnection()

def get_value():
  key = request.args.get('key');

  return dbWorkers.get(key)

def create_value():
  key = request.form['key'];
  value = request.form['value'];

  if not key or not value: 
    return 'error'

  return dbWorkers.put(key, value)

@app.route('/', methods=['GET', 'POST'])
def main():
  if request.method == 'GET':
      return get_value()
  elif  request.method == 'POST':
      return create_value()
  else:
      return 'error'

if __name__ == "__main__":
  app.debug = True
  app.run()

