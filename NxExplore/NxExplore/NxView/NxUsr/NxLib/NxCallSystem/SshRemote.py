#!/usr/bin/python

import paramiko


class SshAgent():
    def __init__(self, remoteIp, username, passwd, remotePort=22):
        self.remoteIp = remoteIp
        self.username = username
        self.passwd = passwd
        self.remotePort = remotePort

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def connectRemote(self):
        print 'Connecting remote server "'+self.remoteIp+':'+str(self.remotePort)+'" ...'
        self.ssh.connect(self.remoteIp, self.remotePort, self.username, self.passwd)
        print 'Connecting remote server "'+self.remoteIp+':'+str(self.remotePort)+' succeeds.'

    def execCommand(self, command):
        print 'Executing command "'+command+'" on server "'+self.remoteIp+':'+str(self.remotePort)+'" ...'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdoutList = stdout.readlines()
        stderrList = stderr.readlines()
        #print 'The result from remote server "'+self.remoteIp+':'+str(self.remotePort)+'" is:'
        if stdoutList != []:
            print '\n---------------- Result ----------------'
            print self.username+'@'+self.remoteIp+':~# '+command
            for i in stdoutList:
                print i,
            print self.username + '@' + self.remoteIp + ':~# '
            print '----------------------------------------\n'
        if stderrList != []:
            #print 'The error from remote server "'+self.remoteIp+':'+str(self.remotePort)+'" is:\n'
            print '\n!!!!!!!!!!!!!! Error !!!!!!!!!!!!!!'
            for j in stderrList:
                print j,
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
        return stdoutList, stderrList


    def closeSsh(self):
        print 'Closing the connection to server "'+self.remoteIp+':'+str(self.remotePort)+'" ...'
        self.ssh.close()
        print 'Connection to server "'+self.remoteIp+':'+str(self.remotePort)+'" has been closed.'




