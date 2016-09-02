#!/usr/bin/python

from NxView.NxUsr.NxLib.DumpInfo import dumpInfo
from NxView.NxEtc.NxPublicConfig.NxPredefined.PreDefault import *
from NxView.NxTools import RemovePyc
from NxView.NxUsr.NxLib import NxFiles


exceptList = [
    'README.rst',
    '__init__.py'

]




dumpInfo('Clean up the .pyc file ...')
RemovePyc.delPycFile()

dumpInfo('Clean up the files in '+str(NxRunPath)+' ...')
filesInRun = NxFiles.listDir(NxRunPath)
for i in filesInRun:
    if i not in exceptList:
        NxFiles.removeForce(NxRunPath+'/'+str(i))
        dumpInfo(NxRunPath+'/'+str(i)+' has been removed.')



dumpInfo('Clean up the files in '+str(NxVarLogPath)+' ...')
dumpInfo('Clean up the files in '+str(NxVarLogPath)+'/'+'GlobalLogs ...')
filesInGlobalLog = NxFiles.listDir(str(NxVarLogPath)+'/'+'GlobalLogs')
if filesInGlobalLog:
    for j in filesInGlobalLog:
        if j not in exceptList:
            NxFiles.removeForce(str(NxVarLogPath)+'/'+'GlobalLogs/'+str(j))
            dumpInfo(str(NxVarLogPath)+'/'+'GlobalLogs/'+str(j)+' has been removed.')

dumpInfo('Clean up the files in '+str(NxVarLogPath)+'/'+'ProjectLogs ...')
filesInProjectlog = NxFiles.listDir(str(NxVarLogPath)+'/'+'ProjectLogs')
if filesInProjectlog:
    for k in filesInProjectlog:
        if k not in exceptList:
            NxFiles.removeForce(str(NxVarLogPath)+'/'+'ProjectLogs/'+k)
            dumpInfo(str(NxVarLogPath)+'/'+'ProjectLogs/'+k+' has been removed.')

dumpInfo('Clean up the files in '+NxTmpPath+' ...')
dumpInfo('Clean up the files in '+NxTmpExchangePath+' ...')
filesInExchange = NxFiles.listDir(NxTmpExchangePath)
if filesInExchange:
    for l in filesInExchange:
        if l not in exceptList:
            NxFiles.removeForce(NxTmpExchangePath+'/'+l)
            dumpInfo(NxTmpExchangePath+'/'+l+' has been removed.')

dumpInfo('Clean up the files in '+NxTmpTrialPath+' ...')
filesInTmpTrial = NxFiles.listDir(NxTmpTrialPath)
if filesInTmpTrial:
    for m in filesInTmpTrial:
        if m not in exceptList:
            NxFiles.removeForce(NxTmpTrialPath+'/'+m)
            dumpInfo(NxTmpTrialPath+'/'+m+' has been removed.')





