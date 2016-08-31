#!/usr/bin/python

import os
import sys
import shutil



# Notes:


def getScriptPath():
    '''
    Return the this script file path.
    This code should always be copied to the running file.
    '''
    return os.path.split(os.path.realpath(__file__))[0]

def getWorkingPath():
    return os.getcwd()

def changeWorkingPath(path):
    '''
    If change the working path OK, then return True, otherwise, return False.
    '''
    try:
        os.chdir(path)
        return True
    except:
        return False

def getUpperPath(localPath):
    originalWorkingPath = getWorkingPath()
    changeWorkingPath(localPath)
    changeWorkingPath('..')
    upperPath = getWorkingPath()
    changeWorkingPath(originalWorkingPath)
    return upperPath

def isExist(path):
    return os.path.exists(path)

def isFile(path):
    return os.path.isfile(path)

def isDir(path):
    return os.path.isdir(path)

def listDir(path):
    '''Return False if meets exception.'''
    try:
        return os.listdir(path)
    except:
        return False

def getFileList(path):
    '''
    Get all the files from given path
    Return False if meets exception.
    '''
    resultList = []
    myPath = str(path)
    if myPath == '':
        return []

    if myPath[-1] == '/':
        prefix = myPath
    else:
        prefix = myPath+'/'

    try:
        listResult = os.listdir(myPath)
    except:
        return False

    for i in listResult:
        if os.path.isfile(prefix+i):
            resultList.append(i)
    return resultList

def getDirList(path):
    '''
    Get all the directories from given path.
    Return False if meets exception.
    '''
    resultList = []
    myPath = str(path)
    if myPath == '':
        return []
    if myPath[-1] == '/':
        prefix = myPath
    else:
        prefix = myPath+'/'
    try:
        listResult = os.listdir(myPath)
    except:
        return False
    for i in listResult:
        if os.path.isdir(prefix+i):
            resultList.append(i)
    return resultList

def makeDirs(path):
    '''Return False if meets unknown exceptions.'''
    try:
        os.makedirs(path)
        return True
    except OSError:
        return True
    except:
        return False

def removeForce(path):
    '''
    Remove given path forcely.
    :param path:
    :return:
    '''
    if not os.path.exists(path):
        return True

    if os.path.isfile(path):
        try:
            os.remove(path)
            return True
        except:
            return False
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
            return True
        except:
            return False
    else:
        return False

def fileSize(path):
    if not isFile(path):
        return False
    return os.path.getsize(path)



if __name__ == '__main__':
    pass







