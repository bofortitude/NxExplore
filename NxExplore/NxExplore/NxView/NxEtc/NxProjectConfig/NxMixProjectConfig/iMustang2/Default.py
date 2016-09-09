#!/usr/bin/python

import logging
import re

from .....NxUsr.NxLib import NxLogging
from ....NxPublicConfig.NxPredefined import PreDefault
from .....NxUsr.NxLib.NxConfig import NxConfig
from .....NxUsr.NxLib import NxFiles








selectedImageReList = [ re.compile(r'^FAD_700D.*\.out$'),
                        re.compile(r'^FAD_1500D.*\.out$'),
                        re.compile(r'^FAD_VM.*\.out$'),
                        re.compile(r'^FAD_VM.*\.ovf\.zip$'),
                        re.compile(r'^FORTINET.*\.mib$'),
                        re.compile(r'^FAD_VM.*debug-info.tar.gz$')
                       ]






# Global configs
iMustang2ConfigFileName = 'iMustang2.conf'
iMustang2ExceptListName = 'iMustang2ExceptList.txt'
mainLogName = 'iMustang2.log'
checkDiskUsageLogName = 'checkDiskUsage.log'
checkWebConnectivityLogName = 'checkWebConnectivity.log'
inputPath = PreDefault.NxExploreInputPath
configPath = inputPath+'/'+iMustang2ConfigFileName
fileExceptBuildList = inputPath+'/'+iMustang2ExceptListName


# config from iMustang2.conf file


NxLogging.setSimpleLogging(debug=True)

if not NxFiles.isFile(configPath):
    logging.warning('The config file '+str(configPath)+' does not exist, exit now !!!')
    exit()
defaultSection = 'iMustang2'
iMustang2ConfigObj = NxConfig(configPath)
if defaultSection not in iMustang2ConfigObj.getSections():
    logging.warning('The config file '+str(configPath)+' has no "'+str(defaultSection)+'" section, exit now !!!')
    exit()

logDirectory = iMustang2ConfigObj.getValueOfOption(defaultSection, 'logDirectory')
if not logDirectory:
    NxLogging.setSimpleLogging()
else:
    NxLogging.setSimpleLogging(logFile=logDirectory+'/'+str(mainLogName))

username = iMustang2ConfigObj.getValueOfOption(defaultSection, 'username')
if username == False:
    logging.warning('The config file '+str(configPath)+' has no username option, exit now !!!')
    exit()
infoWebLoginUser = unicode(username)

password = iMustang2ConfigObj.getValueOfOption(defaultSection, 'password')
if not password:
    logging.warning('The config file '+str(configPath)+' has no password option, exit now !!!')
    exit()
infoWebLoginPasswd = unicode(password)

ignoreMainVerionOption = iMustang2ConfigObj.getValueOfOption(defaultSection, 'ignoredMainVersion')
if not ignoreMainVerionOption:
    ignoreMainVersion = []
else:
    ignoreMainVersion = ignoreMainVerionOption.split(',')
checkIntervalOption = iMustang2ConfigObj.getValueOfOption(defaultSection, 'globalLoopSleepTime')
if not checkIntervalOption:
    checkInterval = 300
else:
    checkInterval = int(checkIntervalOption)

checkOverCount = iMustang2ConfigObj.getValueOfOption(defaultSection, 'successCountForBuildCheck')
if not checkOverCount:
    checkOverCount = 5
else:
    checkOverCount = int(checkOverCount)

debugReceiver = iMustang2ConfigObj.getValueOfOption(defaultSection, 'debugReceivers')
if not debugReceiver:
    debugReceiver = ['bofei']
else:
    debugReceiver = debugReceiver.split(',')


infoReceiver = iMustang2ConfigObj.getValueOfOption(defaultSection, 'infoReceivers')
if not infoReceiver:
    infoReceiver = debugReceiver
else:
    infoReceiver = infoReceiver.split(',')


mainDirectory = iMustang2ConfigObj.getValueOfOption(defaultSection, 'mainDirectory')
if not mainDirectory:
    mainDirectory = '/srv/ftp/upload2'
imageLocalStoragePath = mainDirectory


diskThreshold = iMustang2ConfigObj.getValueOfOption(defaultSection, 'mainDirectoryUsedThreshold')
if not diskThreshold:
    diskThreshold = 80
else:
    diskThreshold = int(diskThreshold)




# Predefined parameters of info.fortinet.com
infoWebLoginUrl = 'https://info.fortinet.com/session'
infoWebBasicHeadersList= [
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
]
infoWebLoginHeadersList = infoWebBasicHeadersList+\
                          [
    ('Referer', 'https://info.fortinet.com/'),
    ('Origin', 'https://info.fortinet.com')
]

infoWebMainVersionUrl = 'https://info.fortinet.com/files/FortiADC/'

#infoWebBuildListUrl = 'https://info.fortinet.com/files/FortiADC/v4.00/Images/'
#infoWebHtmlBuildTableAttrs = {'data-current':'/files/FortiADC/v4.00/Images'}
infoWebHtmlBuildStrPattern = re.compile(r'^build.*/$')
infoWebHtmlImageStrPattern = re.compile(r'.*')
infoWebHtmlMainVersionTableAttrs = {'data-current':'/files/FortiADC'}




































