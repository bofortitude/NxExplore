#!/usr/bin/python

import logging
from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat
from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2 import Default

def pushInfo(message, logger=None):
    if logger is None:
        logger = logging.getLogger()
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret, logger=logger)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=Default.infoReceiver)


def send2Me(message, logger=None):
    if logger is None:
        logger = logging.getLogger()
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret, logger=logger)
    myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], message, toUserList=Default.debugReceiver)