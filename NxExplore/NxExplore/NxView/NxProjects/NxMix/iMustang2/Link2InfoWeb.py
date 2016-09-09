#!/usr/bin/python



from ....NxUsr.NxLib import NxRequests
from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2.Default import *


import HtmlParser

import time
import logging



class Link2InfoWeb():
    def __init__(self, retry=20):
        self.retry = retry
        self.cookies = {}

    def returnCookies(self):
        return self.cookies

    def _buildSender(self, headers=None, cookies=None):
        httpAgent = NxRequests.NxRequests()
        if headers:
            if isinstance(headers, list):
                logging.debug('Adding the required headers ...')
                for i in headers:
                    logging.debug('Adding header '+str(i)+' .')
                    httpAgent.addHeader(i[0], i[1])
            else:
                logging.debug('The given headers is not a list, return None!')
                return None
        if cookies:
            if isinstance(cookies, dict):
                logging.debug('Adding the required cookies ...')
                for (i,j) in cookies.items():
                    logging.debug('Adding cookie '+str(i)+'='+str(j)+' .')
                    httpAgent.addCookie(i, j)
            else:
                logging.debug('The given cookies is not a dict, return None!')
                return None
        return httpAgent

    def _checkCookies(self):
        if self.cookies == {}:
            logging.info('Object has no cookies, try to get the login cookies ...')
            if not self.login():
                logging.info('Login failed, please check your username & password or connectivity, return False!')
                return False
        return True

    def _relogin(self):
        logging.info('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
        if not self.login():
            logging.info('Login failed, please check your username & password or connectivity, return False!')
            return False
        return True

    def login(self):
        logging.info('Preparing to login the '+str(infoWebLoginUrl)+' ...')
        httpAgent = self._buildSender(headers=infoWebLoginHeadersList)

        logging.debug('Adding the username:'+str(infoWebLoginUser)+' & password:'+str(infoWebLoginPasswd)+' ...')
        httpAgent.addData(u'name', infoWebLoginUser)
        httpAgent.addData(u'password', infoWebLoginPasswd)

        for i in xrange(self.retry):
            try:
                logging.info('Sending the login requests(URL: '+str(infoWebLoginUrl)+') ...')
                response = httpAgent.post(infoWebLoginUrl)
                if not HtmlParser.isLoginOk(response.content):
                    logging.info('Login failed, please check your username and password, return False!')
                    return False
                else:
                    break
            except Exception as e:
                logging.debug('Meets exception:')
                logging.debug(str(e))
                if i == self.retry-1:
                    logging.info('Tried '+str(self.retry)+' times, it still failed, please check your connectivity, return False!')
                    return False
                logging.info('Sending login requests fails, wait 1s for next retry...')
            time.sleep(1)
        logging.info('Login succeeds.')

        self.cookies = response.cookies.get_dict()
        logging.debug('The response cookies is:')
        logging.debug(str(self.cookies))
        return True

    def getMainVersion(self):
        logging.info('Starting to get the main version list on website ...')

        if self.cookies == {}:
            logging.info('Object has no cookies, try to ge the login cookies ...')
            if not self.login():
                logging.info('Login failed, please check your username & password or connectivity, return False!')
                return False
        logging.info('Building the requests ...')

        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                logging.info('Sending the getting main version requests(URL: '+str(infoWebMainVersionUrl)+') ...')
                mainVersionResponse = httpAgent.get(infoWebMainVersionUrl)
                if not HtmlParser.isLoginOk(mainVersionResponse.content):
                    logging.info('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
                    if not self.login():
                        logging.info('Login failed, please check your username & password or connectivity, return False!')
                        return False
                    mainVersionResponse = httpAgent.get(infoWebMainVersionUrl)
                break
            except Exception as e:
                logging.debug('Meets exception:')
                logging.debug(str(e))

                if i == self.retry-1:
                    logging.info('Tried '+str(self.retry)+' times, getting main version list still failed, please check your connectivity, return False!')
                    return False
                logging.info('Getting main version list failed, wait 1s for next retry ...')
            time.sleep(1)
        logging.info('Getting main version list succeeds.')

        logging.debug('The getting main version list response content is:')
        logging.debug(str(mainVersionResponse.content))

        mainVersionList = HtmlParser.getMainVersionList(mainVersionResponse.content)
        logging.info('The main version list on server is:')
        logging.info(str(mainVersionList))

        return mainVersionList

    def getBuildListOnSite(self, buildListUrl, infoWebHtmlBuildTableAttrs):
        logging.info('Starting to get the build list on website ...')

        if self.cookies == {}:
            logging.info('Object has no cookies, try to get the login cookies ...')

            if not self.login():
                logging.info('Login failed, please check your username & password or connectivity, return False!')
                return False
        logging.info('Building the requests ...')

        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)

        for i in xrange(self.retry):
                try:
                    logging.info('Sending the getting build list requests('+str(buildListUrl)+') ...')

                    buildResponse = httpAgent.get(buildListUrl)
                    #imageResponse = httpAgent.get(buildListUrl)
                    if not HtmlParser.isLoginOk(buildResponse.content):
                        logging.info('Server responds login UI, it seems that request cookie is invalid, try to relogin ...')
                        if not self.login():
                            logging.info('Login failed, please check your username & password or connectivity, return False!')

                            return False
                        buildResponse = httpAgent.get(buildListUrl)
                    break
                except Exception as e:
                    logging.debug('Meets exception:')
                    logging.debug(str(e))

                    if i == self.retry-1:
                        logging.info('Tried '+str(self.retry)+' times, getting build list still failed, please check your connectivity, return False!')

                        return False
                    logging.info('Getting build list failed, wait 1s for next retry ...')

                time.sleep(1)

        logging.info('Getting build list succeeds.')

        logging.debug('The getting build list response content is:')
        logging.debug(str(buildResponse.content))

        buildListOnSite = HtmlParser.getBuildList(buildResponse.content, infoWebHtmlBuildTableAttrs)
        logging.info('The build list on server is:')
        logging.info(str(buildListOnSite))

        return buildListOnSite

    def getSelectedMainVersion(self, rawMainVersionList):
        selectedList = []
        for i in rawMainVersionList:
            if i not in ignoreMainVersion:
                selectedList.append(i)
        logging.info('The selected main version list is:')
        logging.info(str(selectedList))

        return selectedList

    def getImageDictOnSite(self, imageListUrl, imagePageTableAttrs):
        logging.info('Starting to get the image dict on website ...')
        if not self._checkCookies():
            return False
        logging.info('Building the getting image list request ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                logging.info('Sending the getting image list requests('+str(imageListUrl)+') ...')

                imageListResponse = httpAgent.get(imageListUrl)
                if not HtmlParser.isLoginOk(imageListResponse.content):
                    if not self._relogin():
                        return False
                    imageListResponse = httpAgent.get(imageListUrl)
                break
            except Exception as e:
                logging.debug('Meets exception:')
                logging.debug(str(e))

                if i == self.retry-1:
                    logging.info('Tried ' + str(
                        self.retry) + ' times, getting image dict still failed, please check your connectivity, return False!')

                    return False
                logging.info('Getting image dict failed, wait 1s for next retry ...')

            time.sleep(1)
        logging.info('Getting image dict succeeds.')
        logging.debug('The getting image dict content is:')
        logging.debug(str(imageListResponse.content))

        imageModifiedDict = HtmlParser.getImageDict(imageListResponse.content, imagePageTableAttrs)
        logging.info('The image modified dict on server is:')

        logging.info(str(imageModifiedDict))
        return imageModifiedDict


    def headImageSize(self, imageList, buildUrl):
        logging.info('Starting to head the image size ...')

        imageSizeMap = {}
        for i in imageList:
            ximageUrl = buildUrl+str(i)
            if not self._checkCookies():
                return False
            logging.info('Building the heading image size request ...')

            httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
            for j in xrange(self.retry):
                try:
                    logging.info('Sending the head requests ('+ximageUrl+') ...')
                    headResponse = httpAgent.head(ximageUrl)
                    if not HtmlParser.isLoginOk(headResponse.content):
                        if not self._relogin():
                            return False
                        headResponse = httpAgent.head(ximageUrl)
                    break
                except Exception as e:
                    logging.debug('Meets exception:')
                    logging.debug(str(e))

                    if i == self.retry-1:
                        logging.info('Tried ' + str(
                            self.retry) + ' times, heading image size still failed, please check your connectivity, return False!')

                        return False
                    logging.info('Heading the image size failed, wait 1s for next retry ...')
                time.sleep(1)
            logging.info('Heading the image size succeeds.')


            try:
                logging.debug('The image size response content is:')
                logging.debug(str(headResponse.content))
                logging.debug('The content length of the response is:')
                logging.debug(str(headResponse.headers['Content-Length']))
            except Exception as e:
                logging.debug('Getting content-length meets exception:')
                logging.debug(str(e))
                continue
            imageSizeMap[i] = headResponse.headers['Content-Length']
        logging.info('The image size map is:')
        logging.info(str(imageSizeMap))
        return imageSizeMap

    def getRemoteImageList(self, buildUrl, imagePageTableAttrs):
        logging.info('Starting to get the remote image list via url'+str(buildUrl)+' ...')
        if not self._checkCookies():
            return False
        logging.info('Building the getting remote image list requests ...')
        httpAgent = self._buildSender(headers=infoWebBasicHeadersList, cookies=self.cookies)
        for i in xrange(self.retry):
            try:
                logging.info('Sending the getting remote image list requests('+str(buildUrl)+') ...')
                imageListResponse = httpAgent.get(buildUrl)
                if not HtmlParser.isLoginOk(imageListResponse.content):
                    if not self._relogin():
                        return False
                    imageListResponse = httpAgent.get(buildUrl)
                break
            except Exception as e:
                logging.debug('Meets exception:')
                logging.debug(str(e))

                if i == self.retry-1:
                    logging.info('Tried ' + str(
                        self.retry) + ' times, getting image list still failed, please check your connectivity, return False!')

                    return False
                logging.info('Getting image list failed, wait 1s for next retry ...')
            time.sleep(1)
        logging.info('Getting image list response succeeds.')
        logging.debug('The getting image list response content is:')
        logging.debug(str(imageListResponse.content))

        imageList = HtmlParser.getImageList(imageListResponse.content, imagePageTableAttrs)
        logging.info('The remote image list is:')
        logging.info(str(imageList))
        return imageList



















