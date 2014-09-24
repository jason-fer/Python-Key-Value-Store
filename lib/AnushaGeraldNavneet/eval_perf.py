'''Evaluates the performance of the K-V store.'''

import time, timeit
import math
import random
from client import *

global_server = 'localhost:5000' #'twostep.cs.wisc.edu:5000'
NUM_KEYS = 10
NUM_RUNS = 10

def mean(l):
	return float(sum(l))/len(l)

def stdev(l):
	m = mean(l)
	mean_squared_deviation = sum([ (x-m)*(x-m) for x in l ])
	return math.sqrt(mean_squared_deviation/(len(l) - 1))

class MeasureLatency:
	def __init__(self, num_keys, num_runs):
		kv739_init(global_server, print_errors=False)
		self.num_keys = num_keys
		self.num_runs = num_runs

	def put_keys(self, keys, vals):
		for k, v in zip(keys, vals):
			status, old_val = kv739_put(k,v)

	def get_keys(self, keys):
		for k in keys:
			status, val = kv739_get(k)

	def delete_keys(self, keys):
		for k in keys:
			status, old_val = kv739_delete(k)

	def generate_random_workload(self, keys, vals, put_prob, get_prob):
		workload = []
		for k,v in zip(keys, vals):
			x = random.random()
			if x < put_prob:
				workload.append((kv739_put, (k,v)))
			elif x < put_prob + get_prob:
				workload.append((kv739_get, (k,)))
			else:
				workload.append((kv739_delete, (k,)))
		return workload

	def run_random_workload(self, workload):
		for func, params in workload:
			func(*params)

	def evaluate_latency(self, func_name, func, *args):
		latencies = []
		for i in xrange(self.num_runs):
			time1 = time.time()
			func(*args)
			time2 = time.time()
			latencies.append(1e6 * (time2-time1)/self.num_keys)
		mean_latency_us = mean(latencies)
		stdev_latency_us = stdev(latencies)
		hostname = global_server.split(':')[0]
		print 'Latency_us|%s|%s|%0.4f|%0.4f' % (hostname, func_name, mean_latency_us, stdev_latency_us)

	def run(self):
		keys = [ str(i) for i in xrange(1, self.num_keys) ]
		original_vals = [ k * 2 for k in keys ]
		new_vals = [ 'new_' + k for k in keys ]

		# Ensure we are starting from a clean store	
		self.delete_keys(keys)

		self.evaluate_latency('put_new', self.put_keys, keys, original_vals)

		self.evaluate_latency('get', self.get_keys, keys)

		self.evaluate_latency('put_existing', self.put_keys, keys, new_vals)
	
		self.evaluate_latency('delete', self.delete_keys, keys)

		for put_prob, get_prob in [(0.1,0.7), (0.3,0.5), (0.5,0.3), (0.7,0.1)]: 
			self.put_keys(keys, original_vals)		# Put back into known original state
			func_name = 'random(%.2f,%.2f)' % (put_prob, get_prob)
			workload = self.generate_random_workload(keys, original_vals, put_prob, get_prob)
			self.evaluate_latency(func_name, self.run_random_workload, workload)

def run_evaluation():
	l = MeasureLatency(NUM_KEYS, NUM_RUNS)
	l.run()

if __name__ == "__main__":
	run_evaluation()
