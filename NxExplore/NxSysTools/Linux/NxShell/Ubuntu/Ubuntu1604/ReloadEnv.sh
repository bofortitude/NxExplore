#!/bin/bash

currentWorkingPath=`pwd`
cd `dirname $0`
scriptPath=`pwd`
cd $currentWorkingPath

easyTC="easy-tc.sh"
reInitNetwork="ReInitNetwork.sh"

chmod +x $scriptPath/*.sh


# Clear iptables rules 
echo "[Starting to clear iptables rules ...]"
iptables -F
iptables -t nat -F
iptables -t raw -F
iptables -t mangle -F
echo "[iptables rules of table raw/mangle/nat/filter have been cleared.]"
echo ""



# Clear all the rules that easy-tc.sh created
if [ -f $scriptPath/$easyTC ]; then
    echo "[Starting to run $easyTC to clear all the iptables and tc rules created by $easyTC ...]"
    interfaceList=`ip link | grep -v -E "^   "| awk '{print $2}'| awk -F ":" '{print $1}'`
    for i in $interfaceList
        do
            if [ $i != "lo" ]; then
                $scriptPath/$easyTC $i -c

            fi
        done
    echo "[Running $easyTC over.]"
    echo ""
else
    echo "[There is no file $easyTC in path $scriptPath, skip this step!]"
    echo ""
fi


# Reinit the networking environment
echo "[Starting to flush interface IP...]"
interfaceList=`ip link | grep -v -E "^   "| awk '{print $2}'| awk -F ":" '{print $1}'`
for i in $interfaceList
    do
        ip address flush dev $i
    done
echo "[Flushing is over.]"
echo ""
echo "[Starting to restart service networking...]"
service networking restart
echo "[The networking has been restarted.]"
echo ""
echo "[Run the file \"/etc/rc.local\".]"
sh /etc/rc.local
echo "[Running\"/etc/rc.local\" over.]"
echo ""


