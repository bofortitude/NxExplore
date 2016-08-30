#!/usr/bin/python

import time
import subprocess


from ....NxUsr.NxLib.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat

def checkSubnet(dstIp):
    subnetOk = True
    subnetOkCount = 0
    subnetFailCount = 0
    command = 'ping '+str(dstIp)+' -c 1'
    while True:
        print 'Starting to ping destination ...'
        shell_run = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if shell_run == 0:
            print 'Destination is reachable.'
            subnetOkCount += 1
            subnetFailCount = 0
        else:
            print 'Destination is unreachable.'
            subnetOkCount = 0
            subnetFailCount += 1

        if subnetFailCount >= 20:
            subnetFailCount = 0
            if subnetOk == True:
                unreachableMessage = '[Connectivity Fails!] IP address '+str(dstIp)+' for Sunnyvale is unreachable!'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], unreachableMessage, toUserList=['bofei', 'youjunsong'])
                subnetOk = False
        if subnetOkCount >= 20:
            subnetOkCount = 0
            if subnetOk == False:
                reachableMessage = '[Connectivity OK!] IP address '+str(dstIp)+' for Sunnyvale is reachable now.'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], reachableMessage, toUserList=['bofei', 'youjunsong'])
                subnetOk = True

        print 'Sleep 1 second ...'
        time.sleep(1)

def mainEn(dstIp = '1.1.1.1'):
    checkSubnet(dstIp)
