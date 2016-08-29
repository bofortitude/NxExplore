#!/bin/bash



showHelp(){

echo "./ResetService.sh <IP address>"
echo ""
exit

}


if [ $# -lt 1 ]; then
    showHelp
fi



dstIpAddress=$1
dstIpAddressV6="2001::"`echo $dstIpAddress|sed 's/\./:/g'`

BindPath="/etc/bind/"
DbLocalFileName="db.local"
BaiducomFileName="db.baidu.com"
AdccomFileName="db.adc.com"



if [ -f "$BindPath""$BaiducomFileName" ]; then
    echo "$BindPath""$BaiducomFileName exists.";
    \cp "$BindPath""$BaiducomFileName" "$BindPath""$BaiducomFileName"".bk"
    rm -rf "$BindPath""$BaiducomFileName"
    echo $BindPath""$BaiducomFileName" has been moved to ""$BindPath""$BaiducomFileName"".bk ."
fi
cp "$BindPath""$DbLocalFileName" "$BindPath""$BaiducomFileName" 
echo "$BindPath""$DbLocalFileName"" has been copied to ""$BindPath""$BaiducomFileName ." 
sed -i 's/@\tIN\tNS\tlocalhost.//' "$BindPath""$BaiducomFileName"
sed -i 's/@\tIN\tA\t127.0.0.1//' "$BindPath""$BaiducomFileName"
sed -i 's/@\tIN\tAAAA\t::1//' "$BindPath""$BaiducomFileName"
echo -e "@\tIN\tNS\tns.baidu.com." >> "$BindPath""$BaiducomFileName"
echo -e "ns\tIN\tA\t$dstIpAddress" >> "$BindPath""$BaiducomFileName"
echo -e "www\tIN\tA\t$dstIpAddress" >> "$BindPath""$BaiducomFileName"
echo -e "mail\tIN\tA\t$dstIpAddress" >>"$BindPath""$BaiducomFileName"
echo "" >> "$BindPath""$BaiducomFileName"
echo -e "ns\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$BaiducomFileName"
echo -e "www\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$BaiducomFileName"
echo -e "mail\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$BaiducomFileName"
sed -i 's/localhost/baidu.com/g' "$BindPath""$BaiducomFileName"
echo "The db.baidu.com file has been recreated over."



if [ -f "$BindPath""$AdccomFileName" ]; then
    echo "$BindPath""$AdccomFileName exists.";
    \cp "$BindPath""$AdccomFileName" "$BindPath""$AdccomFileName"".bk"
    rm -rf "$BindPath""$AdccomFileName"
    echo $BindPath""$AdccomFileName" has been moved to ""$BindPath""$AdccomFileName"".bk ."
fi
cp "$BindPath""$DbLocalFileName" "$BindPath""$AdccomFileName"
echo "$BindPath""$DbLocalFileName"" has been copied to ""$BindPath""$AdccomFileName ." 
sed -i 's/@\tIN\tNS\tlocalhost.//' "$BindPath""$AdccomFileName"
sed -i 's/@\tIN\tA\t127.0.0.1//' "$BindPath""$AdccomFileName"
sed -i 's/@\tIN\tAAAA\t::1//' "$BindPath""$AdccomFileName"
echo -e "@\tIN\tNS\tns.adc.com." >> "$BindPath""$AdccomFileName"
echo -e "ns\tIN\tA\t$dstIpAddress" >> "$BindPath""$AdccomFileName"
echo -e "www\tIN\tA\t$dstIpAddress" >> "$BindPath""$AdccomFileName"
echo -e "mail\tIN\tA\t$dstIpAddress" >>"$BindPath""$AdccomFileName"
echo "" >> "$BindPath""$AdccomFileName"
echo -e "ns\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$AdccomFileName"
echo -e "www\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$AdccomFileName"
echo -e "mail\tIN\tAAAA\t$dstIpAddressV6" >> "$BindPath""$AdccomFileName"
sed -i 's/localhost/adc.com/g' "$BindPath""$AdccomFileName"
echo "The db.adc.com file has been recreated over."


sed -i 's/Reply-Message=.*/Reply-Message=$dstIpAddress/g' /etc/freeradius/acct_users
echo "IP address in /etc/freeradius/acct_users has been replaced with $dstIpAddress ."
sed -i 's/Reply-Message=.*/Reply-Message=$dstIpAddress/g' /etc/freeradius/users
echo "IP address in /etc/freeradius/users has been replaced with $dstIpAddress ."





