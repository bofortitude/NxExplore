#!/usr/bin/python


myFile = open('fineName')
line = myFile.readline()
while line:
    print line,
    line = myFile.readline()

myFile.close()




# simple type:

for line in open('fileName'):
    print line,



