#!/usr/bin/python


import os
import time
import sys

import NxRequests
from .. import NxFiles
from DumpInfo import dumpInfo
from ....NxEtc.NxPublicConfig.NxPredefined import PreDefault as PredefinedDefault
import logging


# accessTokenFile:
# expiresTime
# access_token
# expires_in





class WechatActive():
    def __init__(self, corpId, secret,
                 retry=20, debug=True,
                 accessTokenStoragePath=None, accessTokenFileName='WechatAccessToken'):
        self.corpId = corpId
        self.secret = secret
        self.retry = retry
        self.debug = debug
        self.accessTokenFileName = accessTokenFileName
        #scriptPath = os.path.split(os.path.realpath(__file__))[0]
        if accessTokenStoragePath:
            self.accessTokenStoragePath = accessTokenStoragePath
        else:
            #upperPath = NxFiles.getUpperPath(scriptPath)
            #self.accessTokenStoragePath = upperPath+'/ExchangeData'
            self.accessTokenStoragePath = PredefinedDefault.NxRunPath
        self.accessTokenFile = self.accessTokenStoragePath+'/'+self.accessTokenFileName
        self.accessTokenDict = None
        self.sender = NxRequests.NxRequests()

    def getExpireTime(self, timeout):
        '''Return type is integer.'''
        currentTime = int(time.time())
        expiresTime = currentTime+timeout-60
        if expiresTime > 0:
            return expiresTime
        else:
            return currentTime

    def isValid(self, accessTokenDict=None):
        if accessTokenDict:
            myAccessTokenDict = accessTokenDict
        else:
            myAccessTokenDict = self.accessTokenDict

        if myAccessTokenDict:
            # expires_in
            if 'expiresTime' not in myAccessTokenDict:
                return False
            else:
                if myAccessTokenDict['expiresTime'] > int(time.time()):
                    if 'access_token' in myAccessTokenDict:
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def _getAndWriteToken(self):
        logging.debug('Starting to get access_token now...')

        self.sender.resetSession()
        isQueryOk = False
        for i in xrange(self.retry):
            try:
                accessTokenResponse = self.sender.get(
                    'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + str(self.corpId) + '&corpsecret=' + str(self.secret))
                isQueryOk = True
                break
            except:
                logging.warning('Getting access_token meets exception!')
                e = sys.exc_info()[0]
                logging.debug(str(e))
                isQueryOk = False
            time.sleep(1)

        if not isQueryOk:
            return False


        logging.debug('The response code is:')
        logging.debug(str(accessTokenResponse))
        myAccessTokenDict = accessTokenResponse.json()
        logging.debug('The response json is:')
        logging.debug(str(myAccessTokenDict))
        if 'access_token' not in myAccessTokenDict:
            logging.info('Getting access_token fails!')
            if 'errcode' in myAccessTokenDict:
                logging.info('errcode is '+str(myAccessTokenDict['errcode'])+'.')
            if 'errmsg' in myAccessTokenDict:
                logging.info('errmsg is '+str(myAccessTokenDict['errmsg'])+'.')
            return False

        if 'expires_in' not in myAccessTokenDict:
            logging.info('expires_in is not in the response json!')
            return False
        self.accessTokenDict = myAccessTokenDict
        self.accessTokenDict['expiresTime'] = self.getExpireTime(self.accessTokenDict['expires_in'])
        if not NxFiles.isDir(self.accessTokenStoragePath):
            NxFiles.makeDirs(self.accessTokenStoragePath)
        myFile = open(self.accessTokenFile, 'w')
        myFile.write(str(self.accessTokenDict['expiresTime']) + '\n')
        myFile.write(str(self.accessTokenDict['access_token']) + '\n')
        myFile.write(str(self.accessTokenDict['expires_in'])+'\n')
        myFile.close()
        return True

    def getAccessToken(self):
        logging.debug('Starting to get access_token ...')
        if self.accessTokenDict:
            if self.isValid():
                logging.debug('The access_token in the object is valid.')
                return True

        if NxFiles.isFile(self.accessTokenFile):
            logging.debug('Starting to verify the access_token file "'+str(self.accessTokenFile)+'" ...')
            isFileValid = False
            myTokenFile = open(self.accessTokenFile)
            fileExpiresTime = myTokenFile.readline()
            if fileExpiresTime:
                fileAccessToken = myTokenFile.readline()
                if fileAccessToken:
                    fileExpiresIn = myTokenFile.readline()
                    if fileExpiresIn:
                        isFileValid = True
                    else:
                        isFileValid = False
                else:
                    isFileValid = False
            else:
                isFileValid = False

            if not isFileValid:
                logging.debug('Access_token file "'+str(self.accessTokenFile)+'" is invalid.')
                return self._getAndWriteToken()
            else:
                fileExpiresIn = fileExpiresIn.replace('\n', '')
                fileAccessToken = fileAccessToken.replace('\n', '')
                fileExpiresTime = fileExpiresTime.replace('\n', '')
                if int(fileExpiresTime) > int(time.time()):
                    logging.debug('The access_token in access_token file "'+str(self.accessTokenFile)+'" is valid.')
                    if not self.accessTokenDict:
                        self.accessTokenDict = {}
                    self.accessTokenDict['expiresTime'] = int(fileExpiresTime)
                    self.accessTokenDict['access_token'] = str(fileAccessToken)
                    self.accessTokenDict['expires_in'] = int(fileExpiresIn)
                    return True
                else:
                    return self._getAndWriteToken()
        else:
            logging.debug('There is no file "'+str(self.accessTokenFile)+'" .')
            return self._getAndWriteToken()

    def sendText(self, agentId, message, toUserList=None, toPartyList=None, toTagList=None):

        # toUserList --> List --> string
        # agentId --> integer
        # message --> string
        # toPartyList --> List --> string
        # toTagList --> List --> string

        # Request Method: POST
        # https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
        # {
        #"touser": "UserID1|UserID2|UserID3",  --> Not must
        #"toparty": " PartyID1 | PartyID2 ",   --> Not must
        #"totag": " TagID1 | TagID2 ",         --> Not must
        #"msgtype": "text",                    --> Must
        #"agentid": 1,                         --> Must
        #"text": {                             --> Must
        #    "content": "Holiday Request For Pony(http://xxxxx)"  --> Must
        #},                                                       --> Must
        #"safe":0                                                 --> Not must
        #}


        # {u'errcode': 0, u'errmsg': u'ok'}
        # {u'errcode': 40014, u'errmsg': u'invalid access_token'}



        if toUserList:
            if not isinstance(toUserList, list):
                logging.info('The parameter toUserList you pass is not a list!')
                return False
        if toPartyList:
            if not isinstance(toPartyList, list):
                logging.info('The parameter toPartyList you pass is not a list!')
                return False
        if toTagList:
            if not isinstance(toTagList, list):
                logging.info('The parameter toTagList you pass is not a list!')
                return False
        if not toUserList and not toPartyList and not toTagList:
            dumpInfo('One of the toUserList, toPartyList, toTagList should be given!')
            return False
        toUserString = ''
        toPartyString = ''
        toTagString = ''

        if toUserList:
            for i in toUserList:
                toUserString = toUserString+str(i)+'|'
            if toUserString[-1] == '|':
                toUserString = toUserString[0:-1]
        if toPartyList:
            for j in toPartyList:
                toPartyString = toPartyString+'|'
            if toPartyString[-1] == '|':
                toPartyString = toPartyString[0:-1]
        if toTagList:
            for k in toTagList:
                toTagString = toTagString+'|'
            if toTagString[-1] == '|':
                toTagString = toTagString[0:-1]

        if toUserString == '' and toPartyString == '' and toTagString == '':
            dumpInfo('One of the toUserList, toPartyList, toTagList should be given!')
            return False
        self.getAccessToken()



        for m in xrange(self.retry):
            self.sender.resetSession()
            self.sender.addJson('msgtype', 'text')
            self.sender.addJson('text', {'content': str(message)})
            self.sender.addJson('agentid', int(agentId))

            receiver = ''
            if toUserString != '':
                self.sender.addJson('touser', toUserString)
                receiver = receiver+' '+toUserString
            if toPartyString != '':
                self.sender.addJson('toparty', toPartyString)
                receiver = receiver+' '+toPartyString
            if toTagString != '':
                self.sender.addJson('totag', toTagString)
                receiver = receiver+' '+toTagString

            try:
                dumpInfo('Starting to send the message "'+str(message)+'" to "'+receiver+'" via agentid "'+str(agentId)+'" ...')
                response = self.sender.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+self.accessTokenDict['access_token'])

                if response.status_code == 200:
                    responseJson = response.json()
                    if 'errcode' in responseJson:
                        if int(responseJson['errcode']) == 40014:
                            if self.debug:
                                dumpInfo('The errcode from Wechat server is 40014, the errmsg is "invalid access_token", starting to get access_token again.')
                            NxFiles.removeForce(self.accessTokenFile)
                            self.accessTokenDict = None
                            self.getAccessToken()
                        elif int(responseJson['errcode'] == 0):
                            dumpInfo('Sending the message "' + str(
                                message) + '" to "' + receiver + '" via agentid "' + str(agentId) + '" succeeds.')
                            return True
                        else:
                            dumpInfo('Sending the message "' + str(
                                message) + '" to "' + receiver + '" via agentid "' + str(agentId) + '" fails!')
                            dumpInfo('Response errcode is "'+str(responseJson['errcode'])+'", the reason is "'+str(responseJson['errmsg'])+'" .')
                            return False
                    else:
                        dumpInfo('Json of response has no errcode, try it again.')

                else:
                    dumpInfo('Status code of response from Wechat server is "'+str(response.status_code)+'" not "200" , please check your parameters!')
                    if self.debug:
                        dumpInfo('Response content is:')
                        dumpInfo(response.content, raw=True)
                        dumpInfo('Response json is:')
                        dumpInfo(response.json(), raw=True)
                    return False

            except:
                dumpInfo('Sending the message "' + str(message) + '" to "' + receiver + '" via agentid "' + str(
                        agentId) + '" meets exception!')
                e = sys.exc_info()[0]
                if self.debug:
                    dumpInfo(e, raw=True)

            time.sleep(1)

        dumpInfo('The sending has been retried '+str(self.retry)+' times, but it still fails!')
        return False

    def getDepartmentList(self):
        #https://qyapi.weixin.qq.com/cgi-bin/agent/list?access_token=ACCESS_TOKEN
        self.getAccessToken()
        for i in xrange(self.retry):
            dumpInfo('Starting to get the departments list ...')
            try:
                response = self.sender.get('https://qyapi.weixin.qq.com/cgi-bin/agent/list?access_token='+str(self.accessTokenDict['access_token']))
                if response.status_code == 200:
                    responseJson = response.json()
                    if 'errcode' in responseJson:
                        if int(responseJson['errcode']) == 40014:
                            if self.debug:
                                dumpInfo('The errcode from Wechat server is 40014, the errmsg is "invalid access_token", starting to get access_token again.')
                            NxFiles.removeForce(self.accessTokenFile)
                            self.accessTokenDict = None
                            self.getAccessToken()
                        elif int(responseJson['errcode'] == 0):
                            dumpInfo('Getting the departments list succeeds, the list is:')
                            dumpInfo(responseJson['agentlist'], raw=True)
                            return responseJson['agentlist']
                        else:
                            dumpInfo()
                            dumpInfo('Response errcode is "'+str(responseJson['errcode'])+'", the reason is "'+str(responseJson['errmsg'])+'" .')
                            return False
                    else:
                        dumpInfo('Json of response has no errcode, try it again.')

                else:
                    dumpInfo('The status code of response from Wechat server is '+str(response.status_code)+', rather than 200!')
                    if self.debug:
                        dumpInfo('Response content is:')
                        dumpInfo(response.content, raw=True)
                        dumpInfo('Response json is:')
                        dumpInfo(response.json(), raw=True)
                    return False
            except:
                e = sys.exc_info()[0]
                dumpInfo('Getting departments list meets exception!')
                if self.debug:
                    dumpInfo(e, raw=True)

    def getDepartmentMembers(self, departmentId=1, fetchChild=True, memberStatus=0):

        # memberStatus = 0  --> fetch all members
        # memberStatus = 1  --> fetch the members followed wechat
        # memberStatus = 2  --> fetch disabled members
        # memberStatus = 4  --> fetch all the members unfollowed wechat

        # https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID&fetch_child=FETCH_CHILD&status=STATUS

        # {
           #"errcode": 0,
           #"errmsg": "ok",
           #"userlist": [
           #        {
           #               "userid": "zhangsan",
           #               "name": "zhangsan",
           #               "department": [1, 2]
           #        }
           #  ]
        # }

        if memberStatus != 0 and memberStatus != 1 and memberStatus != 2 and memberStatus != 4:
            memberStatus = 1
        if fetchChild:
            myFetchChild = 1
        else:
            myFetchChild = 0

        self.getAccessToken()
        for i in xrange(self.retry):
            self.sender.resetSession()
            dumpInfo('Starting to get the department members ...')
            try:
                response = self.sender.get('https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token='
                                           +str(self.accessTokenDict['access_token'])+'&department_id='+
                                           str(departmentId)+'&fetch_child='+str(myFetchChild)+'&status='+str(memberStatus))
                if response.status_code == 200:
                    responseJson = response.json()
                    if 'errcode' in responseJson:
                        if int(responseJson['errcode']) == 40014:
                            if self.debug:
                                dumpInfo('The errcode from Wechat server is 40014, the errmsg is "invalid access_token", starting to get access_token again.')
                            NxFiles.removeForce(self.accessTokenFile)
                            self.accessTokenDict = None
                            self.getAccessToken()
                        elif int(responseJson['errcode'] == 0):
                            dumpInfo('Getting the department members succeeds, the list is:')
                            dumpInfo(responseJson['userlist'], raw=True)
                            return responseJson['userlist']
                        else:
                            dumpInfo()
                            dumpInfo('Response errcode is "'+str(responseJson['errcode'])+'", the reason is "'+str(responseJson['errmsg'])+'" .')
                            return False
                    else:
                        dumpInfo('Json of response has no errcode, try it again.')

                else:
                    dumpInfo('The status code of response from Wechat server is '+str(response.status_code)+', rather than 200!')
                    if self.debug:
                        dumpInfo('Response content is:')
                        dumpInfo(response.content, raw=True)
                        dumpInfo('Response json is:')
                        dumpInfo(response.json(), raw=True)
                    return False

            except:
                e = sys.exc_info()[0]
                dumpInfo('Getting department members meets exception!')
                if self.debug:
                    dumpInfo(e, raw=True)

            time.sleep(1)




















