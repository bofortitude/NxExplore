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

BindPath="/var/named/"
DbLocalFileName="db.sample"
BaiducomFileName="db.baidu.com"
AdccomFileName="db.adc.com"



echo "\$TTL    604800" > "$BindPath""$DbLocalFileName"

echo "@       IN      SOA     localhost. root.localhost. (" >> "$BindPath""$DbLocalFileName"
echo "                              2         ; Serial"  >> "$BindPath""$DbLocalFileName"
echo "                         604800         ; Refresh" >> "$BindPath""$DbLocalFileName"
echo "                          86400         ; Retry" >> "$BindPath""$DbLocalFileName"
echo "                        2419200         ; Expire" >> "$BindPath""$DbLocalFileName"
echo "                         604800 )       ; Negative Cache TTL" >> "$BindPath""$DbLocalFileName"
echo ";"  >> "$BindPath""$DbLocalFileName"
echo "Create $BindPath$DbLocalFileName over."


if [ -f "$BindPath""$BaiducomFileName" ]; then
    echo "$BindPath""$BaiducomFileName exists.";
    \cp "$BindPath""$BaiducomFileName" "$BindPath""$BaiducomFileName"".bk"
    rm -rf "$BindPath""$BaiducomFileName"
    echo $BindPath""$BaiducomFileName" has been moved to ""$BindPath""$BaiducomFileName"".bk ."
fi
cp "$BindPath""$DbLocalFileName" "$BindPath""$BaiducomFileName" 
echo "$BindPath""$DbLocalFileName"" has been copied to ""$BindPath""$BaiducomFileName ." 
#sed -i "s/@\tIN\tNS\tlocalhost.//" "$BindPath""$BaiducomFileName"
#sed -i "s/@\tIN\tA\t127.0.0.1//" "$BindPath""$BaiducomFileName"
#sed -i "s/@\tIN\tAAAA\t::1//" "$BindPath""$BaiducomFileName"
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
#sed -i 's/@\tIN\tNS\tlocalhost.//' "$BindPath""$AdccomFileName"
#sed -i 's/@\tIN\tA\t127.0.0.1//' "$BindPath""$AdccomFileName"
#sed -i 's/@\tIN\tAAAA\t::1//' "$BindPath""$AdccomFileName"
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

echo "Restarting service named..."
systemctl restart named
echo "\"named\" has been restarted."



sed -i "s/Reply-Message=.*/Reply-Message=$dstIpAddress/g" /etc/raddb/mods-config/files/accounting
echo "IP address in /etc/raddb/mods-config/files/accounting has been replaced with $dstIpAddress ."
sed -i "s/Reply-Message=.*/Reply-Message=$dstIpAddress/g" /etc/raddb/users
echo "IP address in /etc/raddb/users has been replaced with $dstIpAddress ."
echo "Restarting service radiusd..."
systemctl restart radiusd
echo "\"radiusd\" has been restarted."





