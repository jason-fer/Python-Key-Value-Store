import sqlite3
#myConnection = sqlite3.connect('db/allData')
#myCursor = myConnection.cursor()

def hello(someValue):
	print "Hello MaderC."
	print("your value is "+someValue)
	return 'abc'

def startConnection():
	myConnection = sqlite3.connect('db/allData')
	myCursor = myConnection.cursor()

def stopConnection():
	myConnection.close()

def get(key):
	#do db connection here
	return value

def put(key,value):
	#do db connection here
	pass

if __name__ == '__main__':
	hello("saikat")
