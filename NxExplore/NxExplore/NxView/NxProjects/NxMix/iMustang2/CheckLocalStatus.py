#!/usr/bin/python



import logging
import time


from ....NxEtc.NxPublicConfig.NxPredefined.PreWebInfoFortinet import *
from ....NxUsr.NxLib.NxSystemInfo import diskUsage
import InfoPush







def checkDiskUsage(checkInterval=120):
    threshold = diskThreshold
    buildFolderPattern = re.compile(r'^build\d+$')
    while True:
        try:
            logging.debug('Getting the disk usage of the '+str(imageLocalStoragePath))
            rootDiskUsage = diskUsage(imageLocalStoragePath)
            if not rootDiskUsage:
                time.sleep(checkInterval)
                continue
            if rootDiskUsage >= int(threshold):
                entireFiles = NxFiles.getDirList(imageLocalStoragePath)
                buildFolderList = []
                for i in entireFiles:
                    if buildFolderPattern.search(i):
                        buildFolderList.append(i)

                buildNumMap = {}
                for j in buildFolderList:
                    buildNumMap[j] = int(j.replace('build', ''))

                deletedList = []
                for k in xrange(10):
                    if buildNumMap == {}:
                        break
                    minTuple = min(buildNumMap.items(), key=lambda x: x[1])
                    NxFiles.removeForce(imageLocalStoragePath+'/'+minTuple[0])
                    deletedList.append(str(imageLocalStoragePath+'/'+minTuple[0]))
                    del buildNumMap[minTuple[0]]
                    if diskUsage(imageLocalStoragePath) < int(threshold):
                        break
                if deletedList != []:
                    InfoPush.pushInfo('[172.22.15.138]: "'+str(imageLocalStoragePath)+'" disk is used '
                                      +str(rootDiskUsage)+'%, these build folders have been removed:'+str(deletedList))

        except Exception as e:
            pass

        time.sleep(checkInterval)






