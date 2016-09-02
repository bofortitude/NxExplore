#!/usr/bin/python

import re

from . import PreDefault
from ....NxUsr.NxLib.NxConfig import NxConfig
from ....NxUsr.NxLib.DumpInfo import dumpInfo
from ....NxUsr.NxLib import NxFiles




selectedImageReList = [re.compile(r'^FAD_700D.*\.out$'),
                           re.compile(r'^FAD_1500D.*\.out$'),
                           re.compile(r'^FAD_VM.*\.out$'),
                       re.compile(r'^FAD_VM.*\.ovf\.zip$'),
                       re.compile(r'^FORTINET.*\.mib$')
                       ]



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


iMustangPrivateFolderName = 'iMustangPrivate'
buildModifiedMapName = 'buildModified.conf'

inputFilesRootPath = PreDefault.NxExploreInputPath
fileExceptBuildList = inputFilesRootPath+'/'+'iMustangExceptList.txt'
fileImustangConf = inputFilesRootPath+'/'+'iMustang.conf'
imageLocalStoragePath='/srv/ftp/upload2'

if not NxFiles.isFile(fileImustangConf):
    dumpInfo('The config file '+str(fileImustangConf)+' does not exist, exit now !!!')
    exit()
iMustangConfigObj = NxConfig(fileImustangConf)
if 'iMustang' not in iMustangConfigObj.getSections():
    dumpInfo('The config file '+str(fileImustangConf)+' has no "iMustang" section, exit now !!!')
    exit()
username = iMustangConfigObj.getValueOfOption('iMustang', 'username')
if username == False:
    dumpInfo('The config file '+str(fileImustangConf)+' has no username option, exit now !!!')
    exit()
infoWebLoginUser = unicode(username)
password = iMustangConfigObj.getValueOfOption('iMustang', 'password')
if not password:
    dumpInfo('The config file '+str(fileImustangConf)+' has no password option, exit now !!!')
    exit()
infoWebLoginPasswd = unicode(password)
ignoreMainVerionOption = iMustangConfigObj.getValueOfOption('iMustang', 'ignoreMainVersion')
if not ignoreMainVerionOption:
    ignoreMainVersion = []
else:
    ignoreMainVersion = ignoreMainVerionOption.split(',')
checkIntervalOption = iMustangConfigObj.getValueOfOption('iMustang', 'checkInterval')
if not checkIntervalOption:
    checkInterval = 300
else:
    checkInterval = int(checkIntervalOption)

checkOverCount = iMustangConfigObj.getValueOfOption('iMustang', 'checkOverCount')
if not checkOverCount:
    checkOverCount = 5
else:
    checkOverCount = int(checkOverCount)
infoReceiver = iMustangConfigObj.getValueOfOption('iMustang', 'infoReceiver')
if not infoReceiver:
    infoReceiver = ['bofei']
else:
    infoReceiver = infoReceiver.split(',')
diskThreshold = iMustangConfigObj.getValueOfOption('iMustang', 'diskThreshold')
if not diskThreshold:
    diskThreshold = 80
else:
    diskThreshold = int(diskThreshold)














