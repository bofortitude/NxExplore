#!/usr/bin/python



from ....NxUsr.NxLib import NxRequests
from ....NxEtc.NxPublicConfig.NxPredefined.PreWebInfoFortinet import *
from ....NxUsr.NxLib.DumpInfo import dumpInfo

import HtmlParser

import time



class Link2InfoWeb():
    def __init__(self, debug=True, retry=20):
        self.debug = debug
        self.retry = retry
        self.cookies = {}

    def _buildSender(self, headers=None, cookies=None):
        httpAgent = NxRequests.NxRequests()
        if headers:
            if isinstance(headers, list):
                if self.debug:
                    dumpInfo('Adding the required headers ...')
                for i in headers:
                    if self.debug:
                        dumpInfo('Adding header '+str(i)+' .')
                    httpAgent.addHeader(i[0], i[1])
            else:
                if self.debug:
                    dumpInfo('The given headers is not a list, return None!')
                return None
        if cookies:
            if isinstance(cookies, dict):
                if self.debug:
                    dumpInfo('Adding the required cookies ...')
                for (i,j) in cookies.items():
                    if self.debug:
                        dumpInfo('Adding cookie '+str(i)+'='+str(j)+' .')
                    httpAgent.addCookie(i, j)
            else:
                if self.debug:
                    dumpInfo('The given cookies is not a dict, return None!')
                return None
        return httpAgent

    def login(self):
        dumpInfo('Preparing to login the '+str(infoWebLoginUrl)+' ...')
        httpAgent = self._buildSender(headers=infoWebLoginHeadersList)

        if self.debug:
            dumpInfo('Adding the username:'+str(infoWebLoginUser)+' & password:'+str(infoWebLoginPasswd)+' ...')
        httpAgent.addData(u'name', infoWebLoginUser)
        httpAgent.addData(u'password', infoWebLoginPasswd)

        for i in xrange(self.retry):
            try:
                dumpInfo('Sending the login requests ...')
                response = httpAgent.post(infoWebLoginUrl)
                if not HtmlParser.isLoginOk(response.content):
                    dumpInfo('Login failed, please check your username and password, return False!')
                    return False
                else:
                    break
            except:
                if i == self.retry-1:
                    dumpInfo('Tried '+str(self.retry)+' times, it still failed, please check your connectivity, return False!')
                    return False
                dumpInfo('Sending login requests fails, wait 1s for next retry...')
            time.sleep(1)
        dumpInfo('Login succeeds.')
        self.cookies = response.cookies.get_dict()
        if self.debug:
            dumpInfo('The response cookies is:')
            dumpInfo(str(self.cookies), raw=True)
        return True

    def getBuildListOnSite(self, buildListUrl):
        dumpInfo('Starting to get the build list on website ...')
        if self.cookies == {}:
            dumpInfo('Object has no cookies, try to get the login cookies ...')
            if not self.login():
                dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                return False
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)

        for i in xrange(self.retry):
                try:
                    imageResponse = httpAgent.get(buildListUrl)
                    if not HtmlParser.isLoginOk(imageResponse.content):
                        dumpInfo('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
                        if not self.login():
                            dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                            return False
                    imageResponse = httpAgent.get(buildListUrl)
                    break
                except:
                    if i == self.retry-1:
                        dumpInfo('Tried '+str(self.retry)+' times, getting build list still failed, please check your connectivity, return False!')
                        return False
                    dumpInfo('Getting build list failed, wait 1s for next retry ...')
                time.sleep(1)

        dumpInfo('Getting build list succeeds.')
        buildListOnSite = HtmlParser.getBuildList(imageResponse.content)
        dumpInfo('The build list on server is:')
        dumpInfo(str(buildListOnSite), raw=True)
        return buildListOnSite

    def returnCookies(self):
        return self.cookies






def test():
    link = Link2InfoWeb()
    link.login()
    link.getBuildListOnSite(infoWebBuildListUrl)



