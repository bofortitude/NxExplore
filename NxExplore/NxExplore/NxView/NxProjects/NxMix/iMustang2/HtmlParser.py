#!/usr/bin/python



from ....NxEtc.NxProjectConfig.NxMixProjectConfig.iMustang2.Default import *
from bs4 import BeautifulSoup



def getBuildList(html, infoWebHtmlBuildTableAttrs):
    buildList = []
    buildPattern = infoWebHtmlBuildStrPattern
    soup = BeautifulSoup(html)
    imageTable = soup.find('table', attrs=infoWebHtmlBuildTableAttrs)
    buildTagList = imageTable.findChildren('a', attrs={'href':buildPattern})

    for i in buildTagList:
        buildList.append(str(i.getText()).replace('/', ''))
    return buildList

def getMainVersionList(html):
    mainVersionList = []
    soup = BeautifulSoup(html)
    mainVersionTable = soup.find('table', attrs=infoWebHtmlMainVersionTableAttrs)
    mainVersionTagList = mainVersionTable.findChildren('a')
    for i in mainVersionTagList:
        mainVersionList.append(str(i.getText()).replace('/', ''))
    return mainVersionList

def getImageDict(html, imagePageTableAttrs):
    imageSizeDict = {}
    imageModifiedDict = {}
    soup = BeautifulSoup(html)
    imageListTable = soup.find('table', attrs=imagePageTableAttrs)
    tbody = imageListTable.find('tbody')
    allImageUnits = tbody.find_all_next('tr')

    for i in allImageUnits:
        singleUnitList = i.contents
        if len(singleUnitList) < 7:
            continue

        entireImageNameString = str(singleUnitList[1])
        entireModifiedString = str(singleUnitList[3])

        if len(entireImageNameString.split('>')) < 3:
            continue
        if len(entireModifiedString.split('>')) < 2:
            continue

        imageModifiedDict[str(singleUnitList[1]).split('>')[2].split('<')[0]] = str(singleUnitList[3]).split('>')[1].split('<')[0]
    return imageModifiedDict

def getImageList(html, imagePageTableAttrs):
    imageList = []
    imagePattern = infoWebHtmlImageStrPattern
    soup = BeautifulSoup(html)
    imageListTable = soup.find('table', attrs=imagePageTableAttrs)
    imageTagList = imageListTable.findChildren('a', attrs={'href': imagePattern})
    for i in imageTagList:
        imageList.append(str(i.getText()).replace('/', ''))
    return imageList

def isLoginOk(html):

    soup = BeautifulSoup(html)
    findUsernameLabelResult = soup.find_all('label', attrs={'for':'Username'})
    findPasswordLabelResult = soup.find_all('label', attrs={'for': 'Password'})

    if len(findUsernameLabelResult) != 0 and len(findPasswordLabelResult) != 0:
        return False
    else:
        return True












