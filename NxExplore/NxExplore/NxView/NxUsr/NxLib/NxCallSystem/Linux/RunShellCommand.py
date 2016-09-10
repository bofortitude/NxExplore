#!/usr/bin/python


from ...DumpInfo import dumpInfo
import subprocess
import logging

def runShellCmd(command, ok_msg=None, error_msg=None, doRaise=True, debug_info=False):
    '''Return the status code'''
    if debug_info == True:
        logging.info('[Run: ' + str(command) + ']')
        #print '[Run: ' + command + ']'

    shell_run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return_string = ''
    status_code = shell_run.wait()
    for line in shell_run.stdout.readlines():
        if debug_info == True:
            logging.info(str(line))
            #print line
        return_string = return_string + line
    if status_code == 0:
        if debug_info == True:
            #print ok_msg
            logging.info(str(ok_msg))
    else:
        if doRaise == True:
            if debug_info == True:
                #print error_msg
                logging.info(str(error_msg))
            raise RuntimeError(error_msg, 'in RunShellCommand.py')
        else:
            if debug_info == True:
                #print error_msg
                logging.info(str(error_msg))
        return False
    return return_string


class RunShellCommand():
    def __init__(self, debug=True):
        self.cmdSubprocessDict = {}
        self.debug = debug
        self.incompleteCommandsList = []

    def addRunningCommand(self, command):
        dumpInfo('Run command: '+str(command)+' ...')
        shellRun = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.cmdSubprocessDict[str(command)] = shellRun
        dumpInfo('Command '+str(command)+' has been started.')

    def wait4Subprocess(self):
        dumpInfo('Waiting for all the shell commands over...')
        for (i, j) in self.cmdSubprocessDict.items():

            statusCode = j.wait()
            dumpInfo('The command "'+i+'" status cde is:')
            dumpInfo(statusCode, raw=True)

            returnString = ''
            for line in j.stdout.readlines():
                dumpInfo(line, raw=True)
            if statusCode != 0:
                self.incompleteCommandsList.append(i)

    def getIncompleteCommands(self):
        return self.incompleteCommandsList








