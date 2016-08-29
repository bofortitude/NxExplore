#!/usr/bin/python

from ....NxConfigs.NxPredefined.PredefinedWebInfoFortinet import *
from bs4 import BeautifulSoup



def getBuildList(html):
    buildList = []
    buildPattern = infoWebHtmlBuildStrPattern
    soup = BeautifulSoup(html)
    imageTable = soup.find('table', attrs=infoWebHtmlBuildTableAttrs)
    buildTagList = imageTable.findChildren('a', attrs={'href':buildPattern})

    for i in buildTagList:
        buildList.append(str(i.getText()).replace('/', ''))
    return buildList


def isLoginOk(html):

    soup = BeautifulSoup(html)
    findUsernameLabelResult = soup.find_all('label', attrs={'for':'Username'})
    findPasswordLabelResult = soup.find_all('label', attrs={'for': 'Password'})

    if len(findUsernameLabelResult) != 0 and len(findPasswordLabelResult) != 0:
        return False
    else:
        return True












