#!/usr/bin/python

from NxView.NxEtc.NxPublicConfig.NxPredefined.PreDefault import *
from NxView.NxTools import RemovePyc
from NxView.NxUsr.NxLib import NxFiles
from NxView.NxUsr.NxLib.NxLogging import setSimpleLogging
import logging


exceptList = [
    'README.rst',
    '__init__.py'

]


setSimpleLogging()



logging.info('Clean up the files in '+str(NxExploreRootPath)+'/NxTrash'+' ...')
filesInTrash = NxFiles.listDir(str(NxExploreRootPath)+'/NxTrash')
for o in filesInTrash:
    if o not in exceptList:
        NxFiles.removeForce(str(NxExploreRootPath)+'/NxTrash/'+str(o))
        logging.warning(str(NxExploreRootPath)+'/NxTrash/'+str(o)+' has been removed.')



logging.info('Clean up the .pyc file ...')
RemovePyc.delPycFile()

logging.info('Clean up the files in '+str(NxRunPath)+' ...')
filesInRun = NxFiles.listDir(NxRunPath)
for i in filesInRun:
    if i not in exceptList:
        NxFiles.removeForce(NxRunPath+'/'+str(i))
        logging.warning(NxRunPath+'/'+str(i)+' has been removed.')



logging.info('Clean up the files in '+str(NxVarLogPath)+' ...')
logging.info('Clean up the files in '+str(NxVarLogPath)+'/'+'GlobalLogs ...')
filesInGlobalLog = NxFiles.listDir(str(NxVarLogPath)+'/'+'GlobalLogs')
if filesInGlobalLog:
    for j in filesInGlobalLog:
        if j not in exceptList:
            NxFiles.removeForce(str(NxVarLogPath)+'/'+'GlobalLogs/'+str(j))
            logging.warning(str(NxVarLogPath)+'/'+'GlobalLogs/'+str(j)+' has been removed.')

logging.info('Clean up the files in '+str(NxVarLogPath)+'/'+'ProjectLogs ...')
filesInProjectlog = NxFiles.listDir(str(NxVarLogPath)+'/'+'ProjectLogs')
if filesInProjectlog:
    for k in filesInProjectlog:
        if k not in exceptList:
            NxFiles.removeForce(str(NxVarLogPath)+'/'+'ProjectLogs/'+k)
            logging.warning(str(NxVarLogPath)+'/'+'ProjectLogs/'+str(k)+' has been removed.')

logging.info('Clean up the files in '+str(NxTmpPath)+' ...')
logging.info('Clean up the files in '+str(NxTmpExchangePath)+' ...')
filesInExchange = NxFiles.listDir(NxTmpExchangePath)
if filesInExchange:
    for l in filesInExchange:
        if l not in exceptList:
            NxFiles.removeForce(NxTmpExchangePath+'/'+l)
            logging.warning(NxTmpExchangePath+'/'+str(l)+' has been removed.')

logging.info('Clean up the files in '+str(NxTmpTrialPath)+' ...')
filesInTmpTrial = NxFiles.listDir(NxTmpTrialPath)
if filesInTmpTrial:
    for m in filesInTmpTrial:
        if m not in exceptList:
            NxFiles.removeForce(NxTmpTrialPath+'/'+m)
            logging.warning(str(NxTmpTrialPath)+'/'+str(m)+' has been removed.')

logging.info('Clean up the geo_ip_sub folder ...')
geoIpSubParentFolder = NxUsrLibPath+'/NxCallSystem/ADC/IpLibrary'
if NxFiles.isDir(geoIpSubParentFolder):
    if NxFiles.isDir(geoIpSubParentFolder+'/geo_ip_sub'):
        NxFiles.removeForce(geoIpSubParentFolder+'/geo_ip_sub')
        logging.warning(geoIpSubParentFolder+'/geo_ip_sub'+' has been removed.')



