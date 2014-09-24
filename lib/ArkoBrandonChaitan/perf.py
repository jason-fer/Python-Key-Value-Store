import client
import sys
from datetime import datetime

def test(req_type, key_size, value_size):
	N = 500
	total_diff = 0
	time_min, time_max = None, None

	value = 'v'*value_size
	for i in range(N):
		key = ''.join([str(i), 'k'*(key_size - len(str(i)))])

		time_start = datetime.now()
		if req_type == 'put':
			client.kv739_put(key, value)
		elif req_type == 'get':
			client.kv739_get(key)
		else:
			client.kv739_delete(key)
		time_diff = datetime.now() - time_start

		time_dt = time_diff.microseconds
		total_diff = total_diff + time_dt
		if time_min == None:
			time_min = time_dt
			time_max = time_dt
		elif time_dt < time_min:
			time_min = time_dt
		elif time_dt > time_max:
			time_max = time_dt
	client_tput = (N*1000000.)/total_diff
	time_avg =	float(total_diff)/N
	print 'req/s,', str(client_tput)
	print 'kb/s,', str(client_tput * value_size / (1024.))
	print 'avgDelay,', str(time_avg)
	print 'maxDelay,', str(time_max)
	print 'minDelay,', str(time_min)

if __name__ == '__main__':
	if len(sys.argv) < 2 or client.kv739_init(sys.argv[1]) == -1:
		print 'Please provide server <host:port>'
		sys.exit()
	for (k,v) in [(4, 2), (8, 8), (16, 32), (32, 128), (64, 512), (128, 2048)]:
		print 'Tests for key(%d) and value(%d)' % (k,v)
		print 'PUT'
		test('put', k, v)
		print 'GET'
		test('get', k, v)
		print 'DELETE'
		test('delete', k, v)
