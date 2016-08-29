#!/usr/bin/python

import re

from . import PredefinedDefault


infoWebLoginUser = u'bofei@fortinet.com'
infoWebLoginPasswd = u'Mypasswordp123,.'
#infoWebLoginPasswd = u'Mypardpfda123,d.'


ignoreMainVersion=[
    'v2.00',
    'v3.00'
]


inputFilesRootPath = PredefinedDefault.NxInputPath
fileExceptBuildList = inputFilesRootPath+'/'+'ExceptBuildList.txt'
fileUserPasswd = inputFilesRootPath+'/'+'UserPasswd.conf'

imageLocalStoragePath=''

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

infoWebBuildListUrl = 'https://info.fortinet.com/files/FortiADC/v4.00/Images/'
infoWebHtmlBuildTableAttrs = {'data-current':'/files/FortiADC/v4.00/Images'}
infoWebHtmlBuildStrPattern = re.compile(r'^build.*/$')












