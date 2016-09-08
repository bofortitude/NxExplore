#!/usr/bin/python


from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat
from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2 import Default

def pushInfo(message):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=Default.infoReceiver)


def send2Me(message):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=Default.debugReceiver)