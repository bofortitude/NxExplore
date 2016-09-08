#!/usr/bin/python

import multiprocessing
import logging
from ....NxUsr.NxLib.NxLogging import setSimpleLogging
from ....NxEtc.NxPublicConfig.NxPredefined.PreDefault import *
from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import *
from ....NxEtc.NxPublicConfig.NxPredefined.PreWechat import *




def process1(logger, processName):
    while True:
        logger.info(str(processName)+'fdlkjfkdljafdjkaghjklfdjaklfjnvkhuiaguerbvyasufbeuhioyvdbaklfhuidosa')






def mainEn(*args, **kwargs):
    setSimpleLogging()

    plist = []
    for i in xrange(100):
        logger = logging.getLogger('proc'+str(i))
        #logger.setLevel(logging.WARNING)
        p = multiprocessing.Process(target=process1, args=(logger, 'procname'+str(i)))

        plist.append(p)
    for j in plist:
        j.start()
    for k in plist:
        k.join()








