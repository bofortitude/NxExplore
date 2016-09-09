#!/usr/bin/python



import logging
import time


from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2.Default import *
from ....NxUsr.NxLib.NxSystemInfo import diskUsage
import InfoPush







def checkDiskUsage(checkInterval=120):
    threshold = diskThreshold
    buildFolderPattern = re.compile(r'^build\d+$')

    logger = logging.getLogger('checkDiskUsage')
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    if logDirectory:
        logPath = logDirectory+'/'+checkDiskUsageLogName
        rotatingFileHandler = logging.handlers.RotatingFileHandler(logPath, maxBytes=10000000, backupCount=3)
        rotatingFileHandler.setFormatter(formatter)
        logger.addHandler(rotatingFileHandler)


    while True:
        try:
            logger.debug('Getting the disk usage of the '+str(imageLocalStoragePath)+' ...')
            rootDiskUsage = diskUsage(imageLocalStoragePath)
            logger.debug('The disk usage is '+str(rootDiskUsage)+'.')
            if not rootDiskUsage:
                logger.warning('Getting disk usage failed!')
                time.sleep(checkInterval)
                continue
            if rootDiskUsage >= int(threshold):
                logger.debug('The disk usage is greater than '+str(threshold)+' .')
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
                    logger.warning('[172.22.15.138]: "'+str(imageLocalStoragePath)+'" disk is used '
                                      +str(rootDiskUsage)+'%, these build folders have been removed:'+str(deletedList))
                    InfoPush.pushInfo('[172.22.15.138]: "'+str(imageLocalStoragePath)+'" disk is used '
                                      +str(rootDiskUsage)+'%, these build folders have been removed:'+str(deletedList), logger=logger)

        except Exception as e:
            logger.warning('Checking disk usage meets exception:\n'+str(e))

        logger.info('Sleep '+str(checkInterval)+' seconds...')
        time.sleep(checkInterval)






