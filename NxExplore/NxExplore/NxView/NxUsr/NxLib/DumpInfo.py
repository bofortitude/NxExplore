#!/usr/bin/python

import time
import os
import threading

import NxFiles


threadLock = threading.Lock()

def dumpInfo(message, raw=False, logFile=None, logRotateSize=10000000):
    myMessage = str(message)
    if raw:
        finalMessage = myMessage
    else:
        finalMessage = '['+str(time.ctime())+'] '+myMessage
    print finalMessage
    if logFile:
        if NxFiles.isFile(logFile):
            if os.path.getsize(logFile) >= logRotateSize:
                NxFiles.removeForce(str(logFile)+'.bk')
                os.rename(logFile, logFile+'.bk')
        myFile = open(logFile, 'a')
        myFile.write(finalMessage+'\n')
        myFile.close()


def dumpInfoSafe(message, raw=False, logFile=None, logRotateSize=10000000): # NOT READY
    myMessage = str(message)
    if raw:
        finalMessage = myMessage
    else:
        finalMessage = '[' + str(time.ctime()) + '] ' + myMessage
    print finalMessage
    if logFile:
        if NxFiles.isFile(logFile):
            if os.path.getsize(logFile) >= logRotateSize:
                NxFiles.removeForce(str(logFile) + '.bk')
                os.rename(logFile, logFile + '.bk')
        myFile = open(logFile, 'a')
        myFile.write(finalMessage + '\n')
        myFile.close()




