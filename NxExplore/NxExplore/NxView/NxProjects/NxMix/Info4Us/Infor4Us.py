#!/usr/bin/python

import logging

from ....NxUsr.NxLib.NxLogging import setSimpleLogging
from ....NxEtc.NxPublicConfig.NxPredefined import PreWechat as PredefinedWechat
from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from ....NxLib import schedule


import time

taskList = []


def sendToUs(text):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(3, text, toUserList=['bofei', 'xiaoniuniu'])

def sendToMe(text):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(3, text, toUserList=['bofei'])

def sendToXiaoniuniu(text):
    myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
    myAgent.sendText(3, text, toUserList=['xiaoniuniu'])


def scheduleMe(timeString, message):
    schedule.every().day.at(timeString).do(sendToMe, '['+timeString+'] '+message)
    taskList.append('Dadiao husband: '+'['+timeString+'] '+message)

def scheduleXiaoniuniu(timeString, message):
    schedule.every().day.at(timeString).do(sendToXiaoniuniu, '['+timeString+'] '+message)
    taskList.append('Xiaoniuniu: '+'['+timeString+'] '+message)

def scheduleUs(timeString, message):
    schedule.every().day.at(timeString).do(sendToUs, '['+timeString+'] '+message)
    taskList.append('Xiaoniuniu & Dadiao husband: ' + '[' + timeString + '] ' + message)



def mainEn():
    setSimpleLogging()
    scheduleMe('07:10', 'It\'s time to get up and go to defecate now!')
    scheduleMe('07:40', 'It\'s time to complete defecation and go to to wash now!')
    scheduleMe('07:55', 'It\'s time to complete your wash and go to cook now!')
    scheduleMe('09:00', 'It\'s time to go to work now!')
    scheduleXiaoniuniu('11:35', 'It\'s time to prepare to have lunch with your Dadiao husband, xiaoniuniu~~~^_^~~~')
    scheduleMe('11:40', 'It\'s time to go home to have lunch with Xiaoniuniu wife now!')
    scheduleMe('13:40', 'It\'s time to work now!')
    scheduleXiaoniuniu('22:30', 'It\'s time to wash, Xiaoniuniu~~~^_^~~~')
    scheduleMe('22:45', 'It\'s time to wash now!')
    scheduleMe('23:00', 'It\'s time to sleep with your Xiaoniuniu wife now!')
    scheduleXiaoniuniu('23:05', 'It\'s time to sleep with your Dadiao husband, Xiaoniuniu~~~^_^~~~')

    sendToUs('Xiaoniuniu assistant has been restarted ... ^_^~~~')
    taskString = ''
    for i in taskList:
        taskString = taskString + i + '\n'
    sendToUs(taskString)
    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute



