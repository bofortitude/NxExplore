#!/usr/bin/python

import time


def dumpInfo(message, raw=False, logFile=None):
    myMessage = str(message)
    if raw:
        finalMessage = message
    else:
        finalMessage = '['+str(time.ctime())+'] '+message
    print finalMessage
    if logFile:
        myFile = open(logFile, 'a')
        myFile.write(finalMessage+'\n')
        myFile.close()







