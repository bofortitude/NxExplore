#!/usr/bin/python

import time
import subprocess
from ....NxEtc.NxPublicConfig.NxPredefined import PreWebInfoFortinet


from ....NxUsr.NxLib.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat

def checkSubnet():
    dstIp = 'info.fortinet.com'
    subnetOk = True
    subnetOkCount = 0
    subnetFailCount = 0
    command = 'ping '+str(dstIp)+' -c 1'
    while True:
        #print 'Starting to ping destination ...'
        shell_run = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if shell_run == 0:
            #print 'Destination is reachable.'
            subnetOkCount += 1
            subnetFailCount = 0
        else:
            #print 'Destination is unreachable.'
            subnetOkCount = 0
            subnetFailCount += 1

        if subnetFailCount >= 20:
            subnetFailCount = 0
            if subnetOk == True:
                unreachableMessage = '[Connectivity Fails!]  Website "'+str(dstIp)+'" for Server 172.22.15.138 is unreachable!'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], unreachableMessage, toUserList=PreWebInfoFortinet.infoReceiver)
                subnetOk = False
        if subnetOkCount >= 20:
            subnetOkCount = 0
            if subnetOk == False:
                reachableMessage = '[Connectivity OK!] Website "'+str(dstIp)+'" for Server 172.22.15.138 is reachable now.'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], reachableMessage, toUserList=PreWebInfoFortinet.infoReceiver)
                subnetOk = True

        #print 'Sleep 5 second ...'
        time.sleep(5)