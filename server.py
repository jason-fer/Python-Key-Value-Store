from flask import Flask
from flask import request
import dbWorkers
app = Flask(__name__)

dbWorkers.startConnection()

def get_value():
  key = request.args.get('key');
  return dbWorkers.get(key)
  #run Saikats get method to retrieve the value from the db
  #just return the result

def create_value():
  return "create_value()"
  #json decode the payload
  #make sure there's at least a key
  #run Saikats create method to set the value in the database
  #just return the result

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

