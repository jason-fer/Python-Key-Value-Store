import sqlite3
myConnection = None
myCursor = None

dbName="allData"
dbTable="allData" #messedupSomewhere!

def hello(someValue):
	print "Hello MaderC."
	print("your value is "+someValue)
	return 'abc'

def startConnection():
	global myCursor, myConnection
	print "Creating Connection ..."
	myConnection = sqlite3.connect('db/allData')
        #myConnection = sqlite3.connect('db/'+dbName)
	myCursor = myConnection.cursor()

def stopConnection():
	global myCursor, myConnection
	myConnection.close()
        myConnection = None
        myCursor = None

def get(key):
	value=key
	return value

def put(key,value):
        global myCursor, myConnection
	#check if connection is open else open it!
	if not myCursor:
		startConnection()
	myCursor.execute("INSERT INTO "+dbTable+" VALUES ('"+key+"','"+value+"')")
	myConnection.commit()

if __name__ == '__main__':
	hello("saikat")
	startConnection();
	put("newKey","newValue")
	stopConnection();
