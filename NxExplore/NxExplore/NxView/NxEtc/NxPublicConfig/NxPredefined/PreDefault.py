#!/usr/bin/python

import os


PredefinedDefaultScriptPath = os.path.split(os.path.realpath(__file__))[0]

originalWorkingPath = os.getcwd()
os.chdir(PredefinedDefaultScriptPath)
os.chdir('..')
NxConfigsPath = os.getcwd()
os.chdir('..')
NxStackPath = os.getcwd()
os.chdir('..')
NxFocusPath = os.getcwd()
os.chdir(originalWorkingPath)

NxExchangePath = NxStackPath+'/'+'NxExchange'
NxLogsPath = NxFocusPath+'/'+'NxLogs'
NxInputPath = NxFocusPath+'/'+'NxInput'
NxOutputPath = NxFocusPath+'/'+'NxOutput'















