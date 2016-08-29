#!/usr/bin/python


logFile = 'logName.txt'
finalMessage = 'message'

myFile = open(logFile, 'a')
myFile.write(finalMessage+'\n')
myFile.close()


myFile = open(logFile, 'w')
myFile.write(finalMessage+'\n')
myFile.close()

# 'a' : add content
# 'w' : force writing, create a new if none
# 'r' : read





