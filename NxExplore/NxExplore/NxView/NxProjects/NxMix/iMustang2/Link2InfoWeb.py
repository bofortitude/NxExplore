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

    def returnCookies(self):
        return self.cookies

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

    def _checkCookies(self):
        if self.cookies == {}:
            dumpInfo('Object has no cookies, try to get the login cookies ...')
            if not self.login():
                dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                return False
        return True

    def _relogin(self):
        dumpInfo('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
        if not self.login():
            dumpInfo('Login failed, please check your username & password or connectivity, return False!')
            return False
        return True

    def login(self):
        dumpInfo('Preparing to login the '+str(infoWebLoginUrl)+' ...')
        httpAgent = self._buildSender(headers=infoWebLoginHeadersList)

        if self.debug:
            dumpInfo('Adding the username:'+str(infoWebLoginUser)+' & password:'+str(infoWebLoginPasswd)+' ...')
        httpAgent.addData(u'name', infoWebLoginUser)
        httpAgent.addData(u'password', infoWebLoginPasswd)

        for i in xrange(self.retry):
            try:
                dumpInfo('Sending the login requests(URL: '+str(infoWebLoginUrl)+') ...')
                response = httpAgent.post(infoWebLoginUrl)
                if not HtmlParser.isLoginOk(response.content):
                    dumpInfo('Login failed, please check your username and password, return False!')
                    return False
                else:
                    break
            except Exception as e:
                if self.debug:
                    dumpInfo('Meets exception:')
                    dumpInfo(e, raw=True)
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

    def getMainVersion(self):
        dumpInfo('Starting to get the main version list on website ...')
        if self.cookies == {}:
            dumpInfo('Object has no cookies, try to ge the login cookies ...')
            if not self.login():
                dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                return False
        dumpInfo('Building the requests ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                dumpInfo('Sending the getting main version requests(URL: '+str(infoWebMainVersionUrl)+') ...')
                mainVersionResponse = httpAgent.get(infoWebMainVersionUrl)
                if not HtmlParser.isLoginOk(mainVersionResponse.content):
                    dumpInfo('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
                    if not self.login():
                        dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                        return False
                    mainVersionResponse = httpAgent.get(infoWebMainVersionUrl)
                break
            except Exception as e:
                if self.debug:
                    dumpInfo('Meets exception:')
                    dumpInfo(e, raw=True)
                if i == self.retry-1:
                    dumpInfo('Tried '+str(self.retry)+' times, getting main version list still failed, please check your connectivity, return False!')
                    return False
                dumpInfo('Getting main version list failed, wait 1s for next retry ...')
            time.sleep(1)
        dumpInfo('Getting main version list succeeds.')
        if self.debug:
            dumpInfo('The getting main version list response content is:')
            dumpInfo(mainVersionResponse.content, raw=True)
        mainVersionList = HtmlParser.getMainVersionList(mainVersionResponse.content)
        dumpInfo('The main version list on server is:')
        dumpInfo(str(mainVersionList), raw=True)
        return mainVersionList

    def getBuildListOnSite(self, buildListUrl, infoWebHtmlBuildTableAttrs):
        dumpInfo('Starting to get the build list on website ...')
        if self.cookies == {}:
            dumpInfo('Object has no cookies, try to get the login cookies ...')
            if not self.login():
                dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                return False
        dumpInfo('Building the requests ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)

        for i in xrange(self.retry):
                try:
                    dumpInfo('Sending the getting build list requests('+str(buildListUrl)+') ...')
                    buildResponse = httpAgent.get(buildListUrl)
                    #imageResponse = httpAgent.get(buildListUrl)
                    if not HtmlParser.isLoginOk(buildResponse.content):
                        dumpInfo('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
                        if not self.login():
                            dumpInfo('Login failed, please check your username & password or connectivity, return False!')
                            return False
                        buildResponse = httpAgent.get(buildListUrl)
                    break
                except Exception as e:
                    if self.debug:
                        dumpInfo('Meets exception:')
                        dumpInfo(e, raw=True)
                    if i == self.retry-1:
                        dumpInfo('Tried '+str(self.retry)+' times, getting build list still failed, please check your connectivity, return False!')
                        return False
                    dumpInfo('Getting build list failed, wait 1s for next retry ...')
                time.sleep(1)

        dumpInfo('Getting build list succeeds.')
        if self.debug:
            dumpInfo('The getting build list response content is:')
            dumpInfo(buildResponse.content, raw=True)
        buildListOnSite = HtmlParser.getBuildList(buildResponse.content, infoWebHtmlBuildTableAttrs)
        dumpInfo('The build list on server is:')
        dumpInfo(str(buildListOnSite), raw=True)
        return buildListOnSite

    def getSelectedMainVersion(self, rawMainVersionList):
        selectedList = []
        for i in rawMainVersionList:
            if i not in ignoreMainVersion:
                selectedList.append(i)
        dumpInfo('The selected main version list is:')
        dumpInfo(selectedList, raw=True)
        return selectedList

    def getImageDictOnSite(self, imageListUrl, imagePageTableAttrs):
        dumpInfo('Starting to get the image dict on website ...')
        if not self._checkCookies():
            return False
        dumpInfo('Building the getting image list request ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                dumpInfo('Sending the getting image list requests('+str(imageListUrl)+') ...')
                imageListResponse = httpAgent.get(imageListUrl)
                if not HtmlParser.isLoginOk(imageListResponse.content):
                    if not self._relogin():
                        return False
                    imageListResponse = httpAgent.get(imageListUrl)
                break
            except Exception as e:
                if self.debug:
                    dumpInfo('Meets exception:')
                    dumpInfo(e, raw=True)
                if i == self.retry-1:
                    dumpInfo('Tried ' + str(
                        self.retry) + ' times, getting image dict still failed, please check your connectivity, return False!')
                    return False
                dumpInfo('Getting image dict failed, wait 1s for next retry ...')
            time.sleep(1)
        dumpInfo('Getting image dict succeeds.')
        if self.debug:
            dumpInfo('The getting image dict content is:')
            dumpInfo(imageListResponse.content, raw=True)
        imageModifiedDict = HtmlParser.getImageDict(imageListResponse.content, imagePageTableAttrs)
        dumpInfo('The image modified dict on server is:')
        dumpInfo(str(imageModifiedDict), raw=True)
        return imageModifiedDict


    def headImageSize(self, imageList, buildUrl):
        dumpInfo('Starting to head the image size ...')
        imageSizeMap = {}
        for i in imageList:
            ximageUrl = buildUrl+str(i)
            if not self._checkCookies():
                return False
            dumpInfo('Building the heading image size request ...')
            httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
            for j in xrange(self.retry):
                try:
                    dumpInfo('Sending the head requests ('+ximageUrl+') ...')
                    headResponse = httpAgent.head(ximageUrl)
                    if not HtmlParser.isLoginOk(headResponse.content):
                        if not self._relogin():
                            return False
                        headResponse = httpAgent.head(ximageUrl)
                    break
                except Exception as e:
                    if self.debug:
                        dumpInfo('Meets exception:')
                        dumpInfo(e, raw=True)
                    if i == self.retry-1:
                        dumpInfo('Tried ' + str(
                            self.retry) + ' times, heading image size still failed, please check your connectivity, return False!')
                        return False
                    dumpInfo('Heading the image size failed, wait 1s for next retry ...')
                time.sleep(1)
            dumpInfo('Heading the image size succeeds.')
            if self.debug:
                try:
                    dumpInfo('The image size response content is:')
                    dumpInfo(headResponse.content, raw=True)
                    dumpInfo('The content length of the response is:')
                    dumpInfo(headResponse.headers['Content-Length'], raw=True)
                except Exception as e:
                    dumpInfo('Getting content-length meets exception:')
                    dumpInfo(str(e), raw=True)
                    continue
            imageSizeMap[i] = headResponse.headers['Content-Length']
        dumpInfo('The image size map is:')
        dumpInfo(imageSizeMap, raw=True)
        return imageSizeMap

    def getRemoteImageList(self, buildUrl, imagePageTableAttrs):
        dumpInfo('Starting to get the remote image list via url'+str(buildUrl)+' ...')
        if not self._checkCookies():
            return False
        dumpInfo('Building the getting remote image list requests ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                dumpInfo('Sending the getting remote image list requests('+str(buildUrl)+') ...')
                imageListResponse = httpAgent.get(buildUrl)
                if not HtmlParser.isLoginOk(imageListResponse.content):
                    if not self._relogin():
                        return False
                    imageListResponse = httpAgent.get(buildUrl)
                break
            except Exception as e:
                if self.debug:
                    dumpInfo('Meets exception:')
                    dumpInfo(e, raw=True)
                if i == self.retry-1:
                    dumpInfo('Tried ' + str(
                        self.retry) + ' times, getting image list still failed, please check your connectivity, return False!')
                    return False
                dumpInfo('Getting image list failed, wait 1s for next retry ...')
            time.sleep(1)
        dumpInfo('Getting image list response succeeds.')
        if self.debug:
            dumpInfo('The getting image list response content is:')
            dumpInfo(imageListResponse.content, raw=True)
        imageList = HtmlParser.getImageList(imageListResponse.content, imagePageTableAttrs)
        dumpInfo('The remote image list is:')
        dumpInfo(imageList, raw=True)
        return imageList



















