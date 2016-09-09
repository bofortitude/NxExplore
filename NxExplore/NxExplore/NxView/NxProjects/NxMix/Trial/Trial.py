#!/usr/bin/python

import multiprocessing
import logging
from ....NxUsr.NxLib.NxLogging import setConcurrentLogging
from ....NxUsr.NxLib.NxLogging import setSimpleLogging
from ....NxEtc.NxPublicConfig.NxPredefined.PreDefault import *
from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import *
from ....NxEtc.NxPublicConfig.NxPredefined.PreWechat import *




def process1(logger, processName):
    abc = 1
    while True:
        logger.info(str(processName)+'=='+str(abc)+'==fdlkjfkdljafdjkaghjklfdjaklfjnvkhuiaguerbvyasufbeuhioyvdbaklfhuidosa')
        abc += 1






def mainEn(*args, **kwargs):
    #setConcurrentLogging(logFile=NxVarLogPath+'/GlobalLogs/trial.log')
    setSimpleLogging(logFile=NxVarLogPath+'/GlobalLogs/trial.log')

    #exit()

    plist = []
    for i in xrange(100):
        logger = logging.getLogger()
        #logger.setLevel(logging.WARNING)
        p = multiprocessing.Process(target=process1, args=(logger, 'procname'+str(i)))

        plist.append(p)
    for j in plist:
        j.start()
    for k in plist:
        k.join()








