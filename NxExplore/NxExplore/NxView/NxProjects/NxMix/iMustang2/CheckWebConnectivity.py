#!/usr/bin/python

import time
import subprocess
import logging
from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2 import Default

from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat

def checkSubnet():
    dstIp = 'info.fortinet.com'
    subnetOk = True
    subnetOkCount = 0
    subnetFailCount = 0
    command = 'ping '+str(dstIp)+' -c 1'

    logger = logging.getLogger('checkSubnet')
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    if Default.logDirectory:
        logPath = Default.logDirectory + '/' + Default.checkWebConnectivityLogName
        rotatingFileHandler = logging.handlers.RotatingFileHandler(logPath, maxBytes=10000000, backupCount=3)
        rotatingFileHandler.setFormatter(formatter)
        logger.addHandler(rotatingFileHandler)

    while True:
        try:
            #print 'Starting to ping destination ...'
            logger.debug('Running the command '+str(command)+'...')
            shell_run = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            if shell_run == 0:
                #print 'Destination is reachable.'
                logger.debug('The command return code is 0.')
                subnetOkCount += 1
                subnetFailCount = 0
            else:
                #print 'Destination is unreachable.'
                logger.debug('The command return code is 1.')
                subnetOkCount = 0
                subnetFailCount += 1

            if subnetFailCount >= 20:
                subnetFailCount = 0
                if subnetOk == True:
                    unreachableMessage = '[Connectivity Fails!]  Website "'+str(dstIp)+'" for Server 172.22.15.138 is unreachable!'
                    logger.debug(unreachableMessage)
                    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret, logger=logger)
                    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], unreachableMessage, toUserList=Default.infoReceiver)
                    subnetOk = False
            if subnetOkCount >= 20:
                subnetOkCount = 0
                if subnetOk == False:
                    reachableMessage = '[Connectivity OK!] Website "'+str(dstIp)+'" for Server 172.22.15.138 is reachable now.'
                    logger.debug(reachableMessage)
                    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret, logger=logger)
                    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], reachableMessage, toUserList=Default.infoReceiver)
                    subnetOk = True
        except Exception as e:
            logger.warning('Running command failed!')

        #print 'Sleep 5 second ...'
        logger.info('Sleep 5 seconds ...')
        time.sleep(5)