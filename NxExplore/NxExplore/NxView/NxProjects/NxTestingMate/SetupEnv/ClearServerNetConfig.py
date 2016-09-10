#!/usr/bin/python


from NxExplore.NxExplore.NxView.NxUsr.NxLib.NxCallSystem import SshRemote

import sys
import re

def clearNetworkConfig(serverIp, username='root', passwd='fortinet', serverPort=22):
    mySsh = SshRemote.SshAgent(serverIp, username, passwd, serverPort)
    mySsh.connectRemote()

    # Delete all vlan interfaces
    print 'Starting to delete all the VLAN interfaces on server "'+str(serverIp)+'" ...'
    intList = mySsh.execCommand('ip link|grep -E -v "^ "|awk \'{print $2}\'|awk -F ":" \'{print $1}\'')
    vlanIntPattern = re.compile(r'.*\..*@.*')
    for i in intList[0]:
        matchResult = vlanIntPattern.match(i.replace('\n', ''))
        if matchResult:
            mySsh.execCommand('ip link del '+i.split('@')[0])
    print 'All the VLAN interfaces on server "'+str(serverIp)+'" have been deleted.'

    # Flush all the IP addresses of interfaces
    print 'Starting to flush all the IP addresses on server "'+str(serverIp)+'" ...'
    intList = mySsh.execCommand('ip link|grep -E -v "^ "|awk \'{print $2}\'|awk -F ":" \'{print $1}\'')

    for j in intList[0]:
        findMgmtResult = mySsh.execCommand(
            'ip add show ' + str(j).replace('\n', '') + '|grep ' + str(serverIp) + ' > /dev/null 2>/dev/null; echo $?')
        if findMgmtResult[0][0].find('0') != -1:
            checkOsResult = mySsh.execCommand('ls /etc/ | grep redhat > /dev/null 2>/dev/null ; echo $?')
            if checkOsResult[0][0].find('1') != -1:
                # Ubuntu
                mySsh.execCommand('ip add flush dev ' + str(j).replace('\n', '') + ' ; systemctl restart networking')
            else:
                #CentOS
                mySsh.execCommand('ip add flush dev ' + str(j).replace('\n', '') + ' ; systemctl restart network')
            break
    for j in intList[0]:
        findMgmtResult = mySsh.execCommand('ip add show '+str(j).replace('\n', '')+'|grep '+str(serverIp)+' > /dev/null 2>/dev/null; echo $?')
        if findMgmtResult[0][0].find('0') != -1:
            print '"'+str(j).replace('\n', '')+'" is the management interface, skip this step.'
            continue
        mySsh.execCommand('ip add flush dev '+j.replace('\n', ''))
    print 'Flushing IP addresses on server "'+str(serverIp)+'" over.'


    # Clear all the iptables rules
    print 'Starting to clear iptables rules on server "'+str(serverIp)+'" ...'
    mySsh.execCommand('iptables -F')
    mySsh.execCommand('iptables -t nat -F')
    mySsh.execCommand('iptables -t raw -F')
    mySsh.execCommand('iptables -t mangle -F')
    print 'Clearing iptables rules on server "'+str(serverIp)+'" over.'


    # Clear tc rules created by easy-tc.sh
    # tc qdisc del dev eth1 root handle 1111: prio >/dev/null 2>/dev/null
    print 'Starting to clear the tc rules on server "'+str(serverIp)+'" created by easy-tc.sh.'
    intList = mySsh.execCommand('ip link|grep -E -v "^ "|awk \'{print $2}\'|awk -F ":" \'{print $1}\'')
    for k in intList[0]:
        mySsh.execCommand('tc qdisc del dev '+str(k).replace('\n', '')+' root handle 1111: prio >/dev/null 2>/dev/null')
    print 'Clearing tc rules on server "'+str(serverIp)+'" over.'


    mySsh.closeSsh()


def initNetworkConfig(serverIp, username='root', passwd='fortinet', serverPort=22):
    mySsh = SshRemote.SshAgent(serverIp, username, passwd, serverPort)
    mySsh.connectRemote()

    mySsh.execCommand('sysctl -w net.ipv4.ip_forward=1')
    mySsh.execCommand('sysctl -w net.ipv6.conf.all.forwarding=1')

    intList = mySsh.execCommand('ip link|grep -E -v "^ "|awk \'{print $2}\'|awk -F ":" \'{print $1}\'')
    for i in intList[0]:
        mySsh.execCommand('ip link set '+str(i).replace('\n', '')+' up')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ''
        print 'Usage:'
        print './ClearServerNetConfig.py <Server IP>'
        print ''
        exit()

    clearNetworkConfig(sys.argv[1])
    initNetworkConfig(sys.argv[1])







