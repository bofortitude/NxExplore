#!/bin/bash



showHelp(){

echo "./ResetService.sh <IP address>"
echo ""
exit

}


if [ $# -lt 1 ]; then
    showHelp
fi

FirstParameter=$1


currentWorkingPath=`pwd`
cd `dirname $0`
scriptPath=`pwd`
cd $currentWorkingPath

UbuntuRoot=$scriptPath"/Ubuntu"
CentosRoot=$scriptPath"/CentOS"
Ubuntu1604=$UbuntuRoot"/Ubuntu1604"
Centos7=$CentosRoot"/CentOS7"


ls /etc/|grep redhat > /dev/null 2>/dev/null
if [[ $? == 1 ]]; then
    # Ubuntu
    cat /etc/issue|grep 16.04 >/dev/null 2>/dev/null
    if [[ $? == 0 ]]; then
        $Ubuntu1604/ResetService.sh $FirstParameter
    fi

else
    # CentOS
    cat /etc/redhat-release |grep "release 7" >/dev/null 2>/dev/null
    if [[ $? == 0 ]]; then
        $Centos7/ResetService.sh $FirstParameter
    fi



fi
