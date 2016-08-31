#!/usr/bin/python

from ....NxUsr.NxLib.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat
from ....NxEtc.NxPublicConfig.NxPredefined import PreWebInfoFortinet

def pushInfo(message):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=PreWebInfoFortinet.infoReceiver)


def send2Me(message):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=['bofei'])