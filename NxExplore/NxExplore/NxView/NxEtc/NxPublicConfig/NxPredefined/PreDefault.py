#!/usr/bin/python

import os



PreDefaultScriptPath = os.path.split(os.path.realpath(__file__))[0]
originalWorkingPath = os.getcwd()
os.chdir(PreDefaultScriptPath)
os.chdir('..')
#NxPublicConfigPredefinedPath = os.getcwd()
NxPublicConfigPath = os.getcwd()
#os.chdir('..')
#NxPublicConfigPath = os.getcwd()
os.chdir('..')
NxEtcPath = os.getcwd()
os.chdir('..')
NxViewPath = os.getcwd()
os.chdir('..')
NxExplorePath = os.getcwd()
os.chdir(originalWorkingPath)



NxExploreInputPath = NxExplorePath+'/NxInput'
NxExploreOutputPath = NxExplorePath+'NxOutput'
NxExploreRootPath = NxExplorePath+'/NxRoot'
NxBinPath = NxViewPath+'/NxBin'
NxLibPath = NxViewPath+'/NxLib'
NxProjectsPath = NxViewPath+'/NxProjects'
NxRunPath = NxViewPath+'/NxRun'
NxTmpPath = NxViewPath+'/NxTmp'
NxToolsPath = NxViewPath+'/NxTools'
NxUsrPath = NxViewPath+'/NxUsr'
NxVarPath = NxViewPath+'/NxVar'
NxProjectConfigPath = NxEtcPath+'/NxProjectConfig'
NxProjectMixPath = NxProjectsPath+'/NxMix'
NxTmpExchangePath = NxTmpPath+'/NxExchange'
NxTmpTrialPath = NxTmpPath+'/NxTrial'
NxUsrBinPath = NxUsrPath+'/NxBin'
NxUsrLibPath = NxUsrPath+'/NxLib'
NxUsrLocalPath = NxUsrPath+'/NxLocal'
NxUsrSharePath = NxUsrPath+'/NxShare'
NxUsrSrcPath = NxUsrPath+'/NxSrc'
NxUsrManPath = NxUsrSharePath+'/NxMan'
NxVarInputPath = NxVarPath+'/NxInput'
NxVarOutputPath = NxVarPath+'/NxOutput'
NxVarLogPath = NxVarPath+'/NxLog'
NxVarResourcesPath = NxVarPath+'/NxResources'



















