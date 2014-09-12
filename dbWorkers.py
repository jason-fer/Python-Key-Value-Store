import sqlite3
import time
import datetime

myConnection = None
myCursor = None

dbName="allData"
dbTable="allData" #messedupSomewhere!

def getTime():
	ts = time.time()
	dt=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S:%f')
	return dt

def startConnection():
	global myCursor, myConnection
	isSuccess=0;
	print("[INFO] "+getTime()+": Creating Connection ...")
	try:
		myConnection = sqlite3.connect('db/'+dbName)
		myCursor = myConnection.cursor()
		isSuccess=1
		print("[INFO] "+getTime()+": Connection Successful!")
	except:
		print("[ERROR] "+getTime()+": Connection failure!")

	return isSuccess

def stopConnection():
	global myCursor, myConnection
	isClosed=0;
	print("[INFO] "+getTime()+": Closing Connection ...")
	try:
		myConnection.close()
		myConnection = None
		myCursor = None
		isClosed=1
		print("[INFO] "+getTime()+": Connection Closed!")
	except:
		print("[ERROR] "+getTime()+": Failed to close connection!")
		

def get(key):
	global myCursor, myConnection
	retFlag=-1
	# return values
	# 0  - if key present
	# 1  - if key not present
	# -1 - failure
	if not myCursor:
		startConnection()

	value = ''
	try:
		myCursor.execute("SELECT value from "+dbTable+" where key = '"+key+"'")
		print myCursor.fetchone()
		if myCursor.fetchone():
			value=myCursor.fetchone()[0]
			retFlag=0
			print("[INFO] "+getTime()+": {GET} key found!")
		else:
			retFlag=1
			print("[INFO] "+getTime()+": {GET} key not found!")
	except:
		retFlag = -1
		print("[ERROR] "+getTime()+": {GET} operation failed!")
		
	return retFlag,value

def put(key,value):
	global myCursor, myConnection
	
	retFlag=-1
	# return values
	# 0  - if key present
	# 1  - if key not present
	# -1 - failure
	if not myCursor:
		startConnection()
	try:
		retFlag, oldV=get(key)
		if retFlag==-1:
			raise
		if retFlag==1:
			myCursor.execute("INSERT INTO "+dbTable+" VALUES ('"+key+"','"+value+"')")
		else:
			myCursor.execute("UPDATE TABLE "+dbTable+" SET value='"+value+"' where key='"+key+"')")	
		myConnection.commit()
		print("[INFO] "+getTime()+": {PUT} value insert!")
	except:
		print("[ERROR] "+getTime()+": {PUT} failed!")
		
	return retFlag

def unit_test():
	#UNIT TEST BELOW!
	startConnection();	
	ts = time.time()
	put(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),"newValue")
	put("1", "hello")
	put("2", "world")
	r, value=get("1")
	print("Value for Key=1 is "+value)
	stopConnection();
	#testing when connection is closed!
	r, value=get("2")
	print("Value for Key=2 is "+value)
	r, value=get("IdontExist")
	print("Value for Key=IdontExist is "+value)
	stopConnection();

if __name__ == '__main__':
	unit_test()
