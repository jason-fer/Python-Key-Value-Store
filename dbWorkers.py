import sqlite3
import time
import datetime

myConnection = None
myCursor = None

dbName="allData"
dbTable="allData" #messedupSomewhere!

def startConnection():
	global myCursor, myConnection
	print "Creating Connection ..."
	#myConnection = sqlite3.connect('db/allData')
	myConnection = sqlite3.connect('db/'+dbName)
	myCursor = myConnection.cursor()
	#TODO: check if connection was successful

def stopConnection():
	global myCursor, myConnection
	myConnection.close()
	myConnection = None
	myCursor = None
	#TODO: check if successful

def get(key):
	global myCursor, myConnection
	#check if connection is open else open it!
	if not myCursor:
		startConnection()

	# throws an error if you try to retrieve a key that doesn't exist
	try:
		myCursor.execute("SELECT value from "+dbTable+" where key = '"+key+"'")
		value=myCursor.fetchone()[0]
	except:
		value = ''
		
	return value

def put(key,value):
	global myCursor, myConnection
	#check if connection is open else open it!
	if not myCursor:
		startConnection()

	myCursor.execute("INSERT INTO "+dbTable+" VALUES ('"+key+"','"+value+"')")
	myConnection.commit()

	#TODO: check if successful

def unit_test():
	#UNIT TEST BELOW!
	startConnection();	
	ts = time.time()
	put(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),"newValue")
	value=get("1")
	print("Value for Key=1 is "+value)
	stopConnection();
	#testing when connection is closed!
	value=get("2")
	print("Value for Key=2 is "+value)
	stopConnection();

if __name__ == '__main__':
	unit_test()


