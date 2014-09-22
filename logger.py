import time
import datetime
import sys
import os
from config import *

logFileObj = None
msgType = ["INFO", "ERROR"]

# current time for logging
def getTime():
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d|%H:%M:%S|%f')
    return dt

# current date for logging
def getDate():
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y')
    return dt

# print std message to console
def msg(typ, method, message, IP=None, caller='server'):
    logMsg = " | ".join([getTime(),
                         str(msgType[typ]),
                         str(os.getpid()),
                         str(IP), str(caller), str(method),
                         str(message)])
    if PRINT_TO_SCREEN:
        print(logMsg)
    if LOGGING_OFF: return
    global logFileObj
    opType = "LOGGING"
    if not IP:
        IP = "<client_unknown>"
    dt = getDate()
    logParentDir = 'log'
    logFile = logParentDir + '/' + dt + ".log"
    if not os.path.isdir(logParentDir):
        print(getTime() + "|" + msgType[0] + "|" + str(os.getpid()) + "|" + IP + "|" \
              + opType + "|creating parent log dir")
        try:
            os.makedirs(logParentDir)
            print(getTime() + "|" + msgType[0] + "|" + str(os.getpid()) + "|" + IP + "|" \
                  + opType + "|parent log folder created: " + logParentDir)
        except:
            print(getTime() + "|" + msgType[1] + "|" + str(os.getpid()) + "|" + IP + "|" \
                  + opType + "|parent log  folder could not be created at " + logParentDir)
    if not logFileObj:
        if not os.path.exists(logFile):
            print(getTime() + "|" + msgType[0] + "|" + str(os.getpid()) + "|" + IP + "|" \
                  + opType + "|creating daily log file: " + logFile)
            try:
                logFileObj = open(logFile, "a")
                print(getTime() + "|" + msgType[0] + "|" + str(os.getpid()) + "|" + IP + "|" \
                      + opType + "|daily log file created: " + logFile)
            except:
                print(getTime() + "|" + msgType[1] + "|" + str(os.getpid()) + "|" + IP + "|" \
                      + opType + "|daily log file " + logFile + " cannot be created!!!")
    try:
        logFileObj = open(logFile, "a")
    except:
        print(getTime() + "|" + msgType[1] + "|" + str(os.getpid()) + "|" + IP + "|" \
              + opType + "|daily log file " + logFile + " cannot be accessed")
    if logFileObj:
        logFileObj.write(logMsg + "\n")

