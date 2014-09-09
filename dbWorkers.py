import sqlite3
#myConnection = sqlite3.connect('db/allData')
#myCursor = myConnection.cursor()

dbName="allData"
dbTable="allData" #messedupSomewhere!

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
	value=key
	return value

def put(key,value):
	#check if connection is open else open it!
	myCursor.exceute("INSERT INTO "+dbTable+" VALUE ('"+key+"','"+value+"')")
	myConnection.commit()

if __name__ == '__main__':
	hello("saikat")
