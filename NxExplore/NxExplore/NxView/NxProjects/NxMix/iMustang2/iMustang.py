#!/usr/bin/python


import time
import multiprocessing
import logging


from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2.Default import *
from .Link2InfoWeb import *
from ....NxUsr.NxLib import NxFiles
from ....NxUsr.NxLib.NxConfig import NxConfig
import HttpDownload
from ....NxUsr.NxLib.NxCallSystem.Linux.RunShellCommand import runShellCmd
import InfoPush
from CheckWebConnectivity import checkSubnet
from CheckLocalStatus import checkDiskUsage





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

    logging.info('The selected build list in local disk is:')
    logging.info(str(selectedBuildList))
    return selectedBuildList

def wait4Next():
    logging.info('Sleep ' + str(checkInterval) + 's for next round checking and downloading...')
    time.sleep(checkInterval)

def selectBuildList(myLink, i):
    currentBuildListUrl = infoWebMainVersionUrl + str(i) + '/Images/'
    currentInfoWebHtmlBuildTableAttrs = {'data-current': '/files/FortiADC/' + str(i) + '/Images'}
    currentBuildList = myLink.getBuildListOnSite(currentBuildListUrl, currentInfoWebHtmlBuildTableAttrs)
    if not currentBuildList:
        logging.warning('The current build list is false!!')
        wait4Next()
    selectedBuildList = getSelectedBuildList(currentBuildList)
    return selectedBuildList

def selectImageList(remoteImageList):
    selectedImageList = []
    if not remoteImageList:
        logging.warning('The remote image list is false!!')
        wait4Next()
    if selectedImageReList == []:
        logging.info('The selectedImageReList is empty.')
        return remoteImageList
    elif not selectedImageReList:
        logging.warning('The selectedImageReList is false!!')
        return remoteImageList
    for i in remoteImageList:
        for j in selectedImageReList:
            if j.search(i):
                selectedImageList.append(i)
                break
    logging.info('The selectedImageList is '+str(selectedImageList)+' .')
    return selectedImageList

def checkLocalFolder(j):
    if not NxFiles.isDir(imageLocalStoragePath):
        logging.info('The directory "'+str(imageLocalStoragePath)+'" does not exist, make it now.')
        NxFiles.makeDirs(imageLocalStoragePath)
    currentBuildLocalPath = imageLocalStoragePath + '/' + str(j)
    if not NxFiles.isDir(currentBuildLocalPath):
        # no local build folder
        logging.info('The local build folder "'+str(currentBuildLocalPath)+'" does not exist, make it now.')
        NxFiles.makeDirs(currentBuildLocalPath)

    if not NxFiles.isDir(currentBuildLocalPath+'/'+'coredump'):
        logging.info('The coredump folder "'+str(currentBuildLocalPath+'/'+'coredump')+'" does not exist, make it now.')
        NxFiles.makeDirs(currentBuildLocalPath+'/'+'coredump')
    runShellCmd('chown ftp:root '+currentBuildLocalPath+'/'+'coredump',
                ok_msg='The '+currentBuildLocalPath+'/'+'coredump'+' has been chowned.',
                error_msg='The '+currentBuildLocalPath+'/'+'coredump'+' chowned error!',
                doRaise=False, debug_info=True)
    logging.info('Current working build path is '+str(currentBuildLocalPath)+' .')
    return currentBuildLocalPath

def getDownloadList(remoteImageSizeDict, localBuildPath):
    imageToDownload = []
    for (key, value) in remoteImageSizeDict.items():
        if key is None:
            logging.warning('The key is None!!')
            continue
        if not NxFiles.isFile(localBuildPath + '/' + str(key)):
            logging.info('The file "'+str(localBuildPath + '/' + str(key))+'" does not exist, it is to be downloaded.')
            imageToDownload.append(str(key))
        else:
            if key is None:
                tmpKey = 'None'
            else:
                tmpKey = str(key)

            localFileSize = NxFiles.fileSize(localBuildPath + '/' + str(key))
            logging.info('The size of file "'+str(tmpKey)+'" in local disk is '
                             +str(localFileSize)+' .')

            if value is None:
                tmpRemoteValue = 'None'
            else:
                tmpRemoteValue = str(value)

            logging.info('The size of file "' +str(tmpKey)+ '" in remote server is '+str(tmpRemoteValue)+' .')
            if int(NxFiles.fileSize(localBuildPath + '/' + str(key))) != int(value):
                logging.info('The size of file "'+str(key)+'" are different between local disk and remote server, it is to be downloaded.')
                NxFiles.removeForce(localBuildPath + '/' + str(key))
                imageToDownload.append(str(key))
    return imageToDownload

def startCheckingConn():
    p = multiprocessing.Process(target=checkSubnet)
    p.start()

def startCheckingDisk():
    p = multiprocessing.Process(target=checkDiskUsage)
    p.start()


def mainEn(*args, **kwargs):
    logging.info('Starting the whole iMustang2 process ...')
    #InfoPush.pushInfo('[172.22.15.138] iMustang has been restarted. ('+str(time.ctime())+')')
    InfoPush.send2Me('[172.22.15.138] iMustang2 has been restarted. ('+str(time.ctime())+')')

    logging.info('Starting the process of checking connectivity ....')
    startCheckingConn()

    logging.info('Starting the process of checking disk usage ...')
    startCheckingDisk()


    buildOverDict = {}
    while True:
        logging.info('iMustang2 new round checking and downloading ...')
        try:
            myLink = Link2InfoWeb()
            if not myLink.login():
                InfoPush.send2Me('[172.22.15.138] Login failed!')
                wait4Next()
                continue

            # select the main version list to be checked
            selectedMainVersionList = myLink.getSelectedMainVersion(myLink.getMainVersion())
            if not selectedMainVersionList:
                InfoPush.send2Me('[172.22.15.138] Getting selected main version list failed!')
                wait4Next()
                continue

            # in selected main version list
            for i in selectedMainVersionList:
                if i is None:
                    logging.warning('The current main version is None!!!')
                    wait4Next()
                    continue
                logging.info('Current main version is '+str(i)+' .')
                # select the build list to be checked
                selectedBuildList = selectBuildList(myLink, i)

                currentBuildListUrl = infoWebMainVersionUrl + str(i) + '/Images/'
                for j in selectedBuildList:
                    # get the remote image list
                    if j is None:
                        logging.warning('The current build is None!!!')
                        wait4Next()
                        continue
                    currentImageListUrl = currentBuildListUrl+str(j)+'/'
                    currentImagePageTableAttrs = {'data-current':'/files/FortiADC/'+str(i)+'/Images/'+str(j)}
                    remoteImageList = myLink.getRemoteImageList(currentImageListUrl, currentImagePageTableAttrs)
                    if not remoteImageList:
                        InfoPush.send2Me('[172.22.15.138] Getting remote image list failed!')
                        wait4Next()
                        continue

                    # get the selected image list
                    selectedImageList = selectImageList(remoteImageList)

                    # get remote image size dict
                    remoteImageSizeDict = myLink.headImageSize(selectedImageList, currentImageListUrl)
                    if not remoteImageSizeDict:
                        InfoPush.send2Me('[172.22.15.138] Getting remote image size dict failed!')
                        wait4Next()
                        continue

                    # check and create local build folder
                    localBuildPath = checkLocalFolder(j)

                    # get image list to download
                    imageToDownload = getDownloadList(remoteImageSizeDict, localBuildPath)
                    logging.info('The image list to download is:')
                    logging.info(str(imageToDownload))

                    # check imageToDownload and if build over
                    if imageToDownload == []:
                        if len(selectedBuildList) == len(remoteImageSizeDict):
                            logging.info('(Remote Image size dict) "'+str(remoteImageSizeDict)+'" = (Selected build list) "'+str(selectedBuildList)+'" .')
                            if j in buildOverDict:
                                buildOverDict[j] = int(buildOverDict[j])+1
                            else:
                                buildOverDict[j] = 1
                        else:
                            logging.warning('(Remote Image size dict) "' + str(
                                remoteImageSizeDict) + '" != (Selected build list) "' + str(selectedBuildList) + '" .')
                            buildOverDict[j] = 0
                    else:
                        buildOverDict[j] = 0

                    if j in buildOverDict:
                        if int(buildOverDict[j]) >= checkOverCount:
                            del buildOverDict[j]
                            logging.info('Add the build number '+str(j)+' to file '+str(fileExceptBuildList)+' .')
                            myFile = open(fileExceptBuildList, 'a')
                            myFile.write(str(j) + '\n')
                            myFile.close()
                            logging.info('Sending the message to receivers '+str(infoReceiver)+' ...')
                            InfoPush.pushInfo('All selected images of '+str(j)+' has been downloaded over, you can check it on '+str(localBuildPath)+' .')


                    downloadThreadList = []
                    for ima in imageToDownload:
                        logging.info('Starting the thread to download '+str(ima)+' ...')
                        downloader = HttpDownload.PyRequestsDownload(currentImageListUrl+ima, myLink.returnCookies(), localBuildPath)
                        downloader.start()
                        downloadThreadList.append(downloader)

                    if downloadThreadList != []:
                        logging.info('Waiting for all threads over...')
                        for thrd in downloadThreadList:
                            thrd.join()
                        logging.info('All threads over.')

        except Exception as e:
            logging.warning('Meets global exception in this round checking and downloading:')
            logging.debug(str(e))
            InfoPush.send2Me('[172.22.15.138 exception!]:'+str(e))
        wait4Next()









