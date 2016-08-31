#!/usr/bin/python


import time


from ....NxEtc.NxPublicConfig.NxPredefined.PreWebInfoFortinet import *
from .Link2InfoWeb import *
from ....NxUsr.NxLib import NxFiles
from ....NxUsr.NxLib.DumpInfo import dumpInfo
from ....NxUsr.NxLib.NxConfig import NxConfig
import HttpDownload
from ....NxUsr.NxLib.NxCallSystem.Linux.RunShellCommand import runShellCmd





def getSelectedBuildList(buildListOnSite):
    selectedBuildList = []
    exceptListFile = fileExceptBuildList
    exceptList = []
    for line in open(exceptListFile):
        if line.split():
            # no space line
            exceptList.append(line.strip())
    for i in buildListOnSite:
        if i not in exceptList:
            selectedBuildList.append(i)

    dumpInfo('The selected build list is:')
    dumpInfo(selectedBuildList, raw=True)
    return selectedBuildList


def readDictFromFile(dictPathName):
    if not NxFiles.isFile(dictPathName):
        return {}
    dictToReturn = {}
    config = NxConfig(dictPathName)
    sections = config.getSections()
    for i in sections:
        keys = config.getItemsOfSection(i)
        for j in keys:
            dictToReturn[j] = config.getValueOfOption(i, j)
    return dictToReturn


def writeDict2File(name, path, dict):
    if not NxFiles.isDir(path):
        NxFiles.makeDirs(path)
    NxFiles.removeForce(str(path)+'/'+str(name))
    config = NxConfig(str(path)+'/'+str(name))
    config.addSection('default')
    for (i,j) in dict.items():
        config.setValueOfOption('default', i, j)


def wait4Next():
    dumpInfo('Sleep ' + str(checkInterval) + 's for next round checking and downloading...')
    time.sleep(checkInterval)


def getSelectedImageList(remoteImageDict):
    selectedImageList = []
    if selectedImageReList == []:
        for i in remoteImageDict:
            selectedImageList.append(i)
        return selectedImageList
    elif selectedImageReList == None:
        for i in remoteImageDict:
            selectedImageList.append(i)
        return selectedImageList

    for i in remoteImageDict:
        for j in selectedImageReList:
            if j.match(i):
                selectedImageList.append(i)
                break
    return selectedImageList

def selectBuildList(myLink, i):
    currentBuildListUrl = infoWebMainVersionUrl + str(i) + '/Images/'
    currentInfoWebHtmlBuildTableAttrs = {'data-current': '/files/FortiADC/' + str(i) + '/Images'}
    currentBuildList = myLink.getBuildListOnSite(currentBuildListUrl, currentInfoWebHtmlBuildTableAttrs)
    if not currentBuildList:
        wait4Next()
    selectedBuildList = getSelectedBuildList(currentBuildList)
    return selectedBuildList

def selectImageList(remoteImageList):
    selectedImageList = []
    if not remoteImageList:
        wait4Next()
    if selectedImageReList == []:
        return remoteImageList
    elif not selectedImageReList:
        return remoteImageList
    for i in remoteImageList:
        for j in selectedImageReList:
            if j.match(i):
                selectedImageList.append(i)
                break
    return selectedImageList

def checkLocalFolder(j):
    if not NxFiles.isDir(imageLocalStoragePath):
        NxFiles.makeDirs(imageLocalStoragePath)
    currentBuildLocalPath = imageLocalStoragePath + '/' + str(j)
    if not NxFiles.isDir(currentBuildLocalPath):
        # no local build folder
        NxFiles.makeDirs(currentBuildLocalPath)

    if not NxFiles.isDir(currentBuildLocalPath+'/'+'coredump'):
        NxFiles.makeDirs(currentBuildLocalPath+'/'+'coredump')
    runShellCmd('chown ftp:root '+currentBuildLocalPath+'/'+'coredump',
                ok_msg='The '+currentBuildLocalPath+'/'+'coredump'+' has been chowned.',
                error_msg='The '+currentBuildLocalPath+'/'+'coredump'+' chowned error!',
                doRaise=False, debug_info=True)

    return currentBuildLocalPath

def getDownloadList(remoteImageSizeDict, localBuildPath):
    imageToDownload = []
    for (key, value) in remoteImageSizeDict.items():
        if not NxFiles.isFile(localBuildPath + '/' + str(key)):
            imageToDownload.append(str(key))
        else:
            if int(NxFiles.fileSize(localBuildPath + '/' + str(key))) != int(value):
                NxFiles.removeForce(localBuildPath + '/' + str(key))
                imageToDownload.append(str(key))
    return imageToDownload




def mainEn(*args, **kwargs):
    dumpInfo('Starting the whole iMustang process ...')

    buildOverDict = {}
    while True:
        dumpInfo('iMustang new round checking and downloading ...')
        try:
            myLink = Link2InfoWeb()
            if not myLink.login():
                wait4Next()
                continue

            # select the main version list to be checked
            selectedMainVersionList = myLink.getSelectedMainVersion(myLink.getMainVersion())

            # in selected main version list
            for i in selectedMainVersionList:

                # select the build list to be checked
                selectedBuildList = selectBuildList(myLink, i)

                currentBuildListUrl = infoWebMainVersionUrl + str(i) + '/Images/'
                for j in selectedBuildList:
                    # get the remote image list
                    currentImageListUrl = currentBuildListUrl+str(j)+'/'
                    currentImagePageTableAttrs = {'data-current':'/files/FortiADC/'+str(i)+'/Images/'+str(j)}
                    remoteImageList = myLink.getRemoteImageList(currentImageListUrl, currentImagePageTableAttrs)

                    # get the selected image list
                    selectedImageList = selectImageList(remoteImageList)

                    # get remote image size dict
                    remoteImageSizeDict = myLink.headImageSize(selectedImageList, currentImageListUrl)
                    if not remoteImageSizeDict:
                        wait4Next()

                    # check and create local build folder
                    localBuildPath = checkLocalFolder(j)

                    # get image list to download
                    imageToDownload = getDownloadList(remoteImageSizeDict, localBuildPath)
                    dumpInfo('The image list to download is:')
                    dumpInfo(imageToDownload, raw=True)

                    # check imageToDownload and if build over
                    if imageToDownload == []:
                        if j in buildOverDict:
                            buildOverDict[j] = int(buildOverDict[j])+1
                        else:
                            buildOverDict[j] = 1
                    if j in buildOverDict:
                        if int(buildOverDict[j]) >= checkOverCount:
                            del buildOverDict[j]
                            myFile = open(fileExceptBuildList, 'a')
                            myFile.write(str(j) + '\n')
                            myFile.close()

                    downloadThreadList = []
                    for ima in imageToDownload:
                        dumpInfo('Starting the thread to download '+str(ima)+' ...')
                        downloader = HttpDownload.PyRequestsDownload(currentImageListUrl+ima, myLink.returnCookies(), localBuildPath)
                        downloader.start()
                        downloadThreadList.append(downloader)

                    dumpInfo('Waiting for all threads over...')
                    for thrd in downloadThreadList:
                        thrd.join()
                    dumpInfo('All threads over.')

        except Exception as e:
            dumpInfo('Meets global exception in this round checking and downloading:')
            dumpInfo(e, raw=True)
        wait4Next()









