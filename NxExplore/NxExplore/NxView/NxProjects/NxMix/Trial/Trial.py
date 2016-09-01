#!/usr/bin/python





def mainEn(*args, **kwargs):
    from ....NxUsr.NxLib.DumpInfo import dumpInfo
    for i in xrange(1000000000):
        dumpInfo('new line new line new line new line', logFile='/root/Temp/logtest.txt', logRotateSize=1000000)