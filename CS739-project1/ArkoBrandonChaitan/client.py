import sys
import requests

URL = None

def kv739_init(server):
  global URL
  code = 0
  URL = 'http://%s/' % (server)
  print URL
  try:
    requests.head(URL, stream=False)
  except requests.exceptions.ConnectionError as e:
    print e
    sys.stderr.write('Could not connect to server at %s\n' % (server,))
    code = -1
    URL = None
  return code

def kv739_get(key):
  if URL == None:
    return -1
  params = {'key': key}
  try:
    r = requests.get(URL, params=params)
  except Exception as e:
    sys.stderr.write('get: Exception: %s\n' % (e,))
    code = -1
    value = None
  else:
    try:
      if r.status_code == requests.codes.OK:
        code = 0
        value = r.json()['value'].encode('ascii')
      elif r.status_code == requests.codes.NOT_FOUND:
        code = 1
        value = None
      else:
        code = -1
        value = None
        for err in r.json()['errors']:
          sys.stderr.write('%s\n' % (err))
    except ValueError as e:
      sys.stderr.write('get: Expected JSON object in response. Body: %s\n' % (r.text,))
      code = -1
      value = None
  return code, value

def kv739_put(key, value):
  if URL == None:
    return -1
  payload = {'key': key, 'value': value}
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  try:
    r = requests.put(URL, data=payload, headers=headers)
  except Exception as e:
    sys.stderr.write('put: Exception: %s\n' % (e,))
    code = -1
    old_value = None
  else:
    try:
      if r.status_code == requests.codes.OK:
        code = 0
        old_value = r.json()['old_value'].encode('ascii')
      elif r.status_code == requests.codes.CREATED:
        code = 1
        old_value = None
      else:
        code = -1
        old_value = None
        for err in r.json()['errors']:
          sys.stderr.write('%s\n' % (err))
    except ValueError as e:
      sys.stderr.write('put: Expected JSON object in response. Body: %s\n' % (r.text,))
      code = -1
      old_value = None
  return code, old_value

def kv739_delete(key):
  if URL == None:
    return -1
  params = {'key': key}
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  try:
    r = requests.delete(URL, params=params, data=params, headers=headers)
  except Exception as e:
    sys.stderr.write('delete: Exception: %s\n' % (e,))
    code = -1
    old_value = None
  else:
    try:
      if r.status_code == requests.codes.OK:
        old_value = r.json()['old_value'].encode('ascii')
        if old_value == '':
          code = 1
          old_value = None
        else:
          code = 0
      else:
        code = -1
        old_value = None
        for err in r.json()['errors']:
          sys.stderr.write('%s\n' % (err))
    except ValueError as e:
      sys.stderr.write('delete: Expected JSON object in response. Body: %s\n' % (r.text,))
      code = -1
      old_value = None
  return code, old_value
