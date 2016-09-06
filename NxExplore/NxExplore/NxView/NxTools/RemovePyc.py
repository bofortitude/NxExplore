#!/usr/bin/python

import os
import re
#import NxFiles
import shutil
import logging



def removeForce(path):
    '''
    Remove give path forcely.
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

def walkRemovePyc(rootPath):
    logging.warning('Starting to remove all the ".pyc" files recursively from the directory "' + str(rootPath) + '" ...')
    pycPattern = re.compile(r'.*\.pyc$')
    for root, dirs, files in os.walk(rootPath):
        for i in files:
            if pycPattern.match(root+'/'+i):
                if removeForce(root+'/'+i) == True:
                    logging.warning('The file "'+str(root)+'/'+str(i)+'" has been removed.')
                else:
                    logging.warning('Removing file "' + root + '/' + i + '" meets error!')

def delPycFile(includeParent=True):
    originalWorkingPath= os.getcwd()
    scriptPath = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(scriptPath)
    os.chdir('..')
    parrentPath = os.getcwd()
    os.chdir(originalWorkingPath)
    if includeParent:
        walkRemovePyc(parrentPath)
    else:
        walkRemovePyc(scriptPath)


if __name__ == '__main__':
    delPycFile()


