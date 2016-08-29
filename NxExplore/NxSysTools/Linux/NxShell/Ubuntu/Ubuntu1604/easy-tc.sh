#!/bin/bash


############################ Custom variable ############################




############################ Custom variable ############################














############################ Predefined variable ############################

delay_time=null
clear_config=no
src_address=null
dst_address=null
source_mac=null
protocol=null
display_config=no
every_number=null
packet_num_string=null
tc_loss=null
tc_duplicate=null
tc_corrupt=null



############################ Predefined variable ############################









cathelp()
{


cat << EOF

How to:
./easy-tc.sh interface [options]


Note:
1. "interface" is the outbound interface.
2. There can be 9 rules at most.


Options:
  -h  [help]                             Show help.

 (filter)
  -s  [outbound_source-address]          Format is like < -s 1.1.0.0/16 >.
  -d  [outbound_destination-address]     Format is like < -d 2.2.2.2/32 >.
  -p  [protocol]                         Default is "icmp", also you can chose "tcp" or "udp".
  -E  [iptables.every]                   Must be used with "-P". 
  -P  [iptables.packet]                  Must be used with "-E". Format is like < -E 20 -p 2-4,7,10,14-17 >.

 (source MAC address)
  -m  [source_MAC_address]               Special mode, this parameter can't be used with "-E" and "-P", format like <-m 01:12:32:33:44:21>.

 (tc option)
  -t  [delay_time]                       Format is "300ms", "2s", default is "0ms".
  -l  [loss]                             Loss rate of tc, "-l 10%" means 10% packets will be droped randomly.
  -r  [duplicate]                        Duplicate rate of tc, "-r 20%" means 20% packets will be duplicated randomly.
  -b  [corrupt]                          Corrupt rate of tc, "-b 30%" means 30% packets will be corrupted randomly.

 (configuration)
  -c  [clear_config]                     Clear the tc and iptables configuration of the interface.
  -a  [display_config]                   Display the tc and iptables configuration of the interface.


Run like:
./easy-tc.sh eth5 -t 100ms -d "10.80.0.0/16"
./easy-tc.sh eth5 -t 100ms -s "10.78.1.4/32" -d "10.80.0.0/16"
./easy-tc.sh eth5 -c


Ver: 20140207

EOF


exit



}






if [[ $* == "" || $1 == "-h" ]]; then
    cathelp
fi

interface=$1

shift $(($OPTIND))
while getopts "hs:d:p:E:P:t:l:r:b:ca" opt
do

    case $opt in
         
         h) cathelp ;;   
         s) src_address=$OPTARG ;;
         d) dst_address=$OPTARG ;;
         p) protocol=$OPTARG ;;
         E) every_number=$OPTARG ;;
         P) packet_num_string=$OPTARG ;;
         m) source_mac=$OPTARG ;;
         t) delay_time=$OPTARG ;;
         l) tc_loss=$OPTARG ;;
         r) tc_duplicate=$OPTARG ;;
         b) tc_corrupt=$OPTARG ;;
         c) clear_config=yes ;;
         a) display_config=yes ;;
         ?) cathelp ;;

    esac

done









############################## function ##############################




clear_configuration()
{


    tc qdisc del dev $interface root handle 1111: prio >/dev/null 2>/dev/null
    echo "[Command]: tc qdisc del dev $interface root handle 1111: prio >/dev/null 2>/dev/null"
    echo ""

    for ((iptables_mark=1;iptables_mark<=10;iptables_mark++))
    do

        mark_value="231$iptables_mark"
        formal_mark_value=`printf "%x" $mark_value`

        real_mark_line=`iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value" | awk -F ":" '{print $1}'`
        #echo 'iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value" | awk -F ":" '{print $1}''


        if [[ $real_mark_line == "" ]]; then
            continue
        else
            tmp_multi_mark=`echo $real_mark_line | awk '{print NF}'`
            if [[ $tmp_multi_mark == 1 ]]; then
                let mark_line=$real_mark_line-2
                iptables -t mangle -D POSTROUTING $mark_line
                echo "[Command]: iptables -t mangle -D POSTROUTING $mark_line"
		echo ""

            else
                while true
                do
                    iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value" >/dev/null
                    echo "[Command]: iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value" >/dev/null"
		    echo ""
                    if [[ $? == 1 ]]; then
                        break
                    fi

                    now_real_mark_line=`iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value" | sed -n "1,1p" | awk -F ":" '{print $1}'`
                    let now_mark_line=$now_real_mark_line-2
                    iptables -t mangle -D POSTROUTING $now_mark_line
                    echo "[Command]: iptables -t mangle -D POSTROUTING $now_mark_line"
		    echo ""



                done
                

            fi

        fi
    done

    echo ""
    echo "Clear configurations of $interface about easy-tc.    [OK]!"
    echo ""
    exit

}

drop_packet_nth()
{

    # 1st parameter means mark value.
    # 2nd parameter means packet_num_string.
    # 3rd parameter means every_number

    packet_num_str=$2
    every_num=$3

   
    #handle the parameter
    ori_str_num_total=`echo $packet_num_str | awk -F "," '{print NF}'`

    for ((ori_str_num=1;ori_str_num<=$ori_str_num_total;ori_str_num++))
    do
        tmp_string=`echo $packet_num_str | awk -F "," -v var=$ori_str_num '{print $var}'`
        echo $tmp_string | grep "-" > /dev/null
        tmp_judge=$?
        if [[ $tmp_judge == 1 ]]; then
            formal_packet_num_str[${#formal_packet_num_str[@]}]=$tmp_string
        elif [[ $tmp_judge == 0 ]]; then
            tmp_min_num=`echo $tmp_string | awk -F "-" '{print $1}'`
            tmp_max_num=`echo $tmp_string | awk -F "-" '{print $2}'`
            for ((tmp_total=$tmp_min_num;tmp_total<=$tmp_max_num;tmp_total++))
            do
                formal_packet_num_str[${#formal_packet_num_str[@]}]=$tmp_total
            done
        fi
    done


    drop_packet_acct=${#formal_packet_num_str[@]}



    for drop_pac in ${formal_packet_num_str[@]}
    do

        let final_real_drop_pac=${drop_pac}-1
        iptables -t mangle -A POSTROUTING -p $protocol -o $interface -s $src_address -d $dst_address -m statistic --mode nth --every $every_num --packet $final_real_drop_pac -j MARK --set-mark $1
        echo "[Command]: iptables -t mangle -A POSTROUTING -p $protocol -o $interface -s $src_address -d $dst_address -m statistic --mode nth --every $every_num --packet $final_real_drop_pac -j MARK --set-mark $1"
	echo ""

    done




}




backup_drop_packet_nth()
{

    # 1st parameter means mark value.
    # 2nd parameter means packet_num_string.
    # 3rd parameter means every_number

    packet_num_str=$2
    every_num=$3

   
    #handle the parameter
    ori_str_num_total=`echo $packet_num_str | awk -F "," '{print NF}'`

    for ((ori_str_num=1;ori_str_num<=$ori_str_num_total;ori_str_num++))
    do
        tmp_string=`echo $packet_num_str | awk -F "," -v var=$ori_str_num '{print $var}'`
        echo $tmp_string | grep "-" > /dev/null
        tmp_judge=$?
        if [[ $tmp_judge == 1 ]]; then
            formal_packet_num_str[${#formal_packet_num_str[@]}]=$tmp_string
        elif [[ $tmp_judge == 0 ]]; then
            tmp_min_num=`echo $tmp_string | awk -F "-" '{print $1}'`
            tmp_max_num=`echo $tmp_string | awk -F "-" '{print $2}'`
            for ((tmp_total=$tmp_min_num;tmp_total<=$tmp_max_num;tmp_total++))
            do
                formal_packet_num_str[${#formal_packet_num_str[@]}]=$tmp_total
            done
        fi
    done


    drop_packet_acct=${#formal_packet_num_str[@]}


    for ((every_total=1;every_total<=$every_num;every_total++))
    do
        traffic_sim[${#traffic_sim[@]}]=$every_total
    done

    for drop_pac in ${formal_packet_num_str[@]}
    do

        let remain_pac=${#traffic_sim[@]}-1
        for ((drop_index=0;drop_index<=$remain_pac;drop_index++))
        do

            if [[ ${traffic_sim[$drop_index]} == ${drop_pac} ]]; then
                let final_every=$remain_pac+1

                iptables -t mangle -A POSTROUTING -p $protocol -o $interface -s $src_address -d $dst_address -m statistic --mode nth --every $final_every --packet $drop_index -j MARK --set-mark $1
                echo "[Command]: iptables -t mangle -A POSTROUTING -p $protocol -o $interface -s $src_address -d $dst_address -m statistic --mode nth --every $final_every --packet $drop_index -j MARK --set-mark $1"
		echo ""
 

                unset traffic_sim[$drop_index]
                for tmp_change in ${traffic_sim[@]}
                do
                    tmp_traffic_sim[${#tmp_traffic_sim[@]}]=${tmp_change}
                done
                unset traffic_sim

                for tmp_change_b in ${tmp_traffic_sim[@]}
                do
                    traffic_sim[${#traffic_sim[@]}]=${tmp_change_b}
                done
                unset tmp_traffic_sim

                break
            fi
        done
    done




}





write_iptables_rule()
{

    #1st parameter means mark value.

    iptables -t mangle -A POSTROUTING -p $protocol -s $src_address -d $dst_address -o $interface  -j MARK --set-mark $1
    echo "[Command]: iptables -t mangle -A POSTROUTING -p $protocol -s $src_address -d $dst_address -o $interface  -j MARK --set-mark $1"
    echo ""
}

write_tc_qdisc_rule()
{
    #1st parameter means tc handle id.
    #2nd means tc loss.
    #3rd means tc duplicate.
    #4th means tc corrupt.

    

    tc qdisc add dev $interface root handle 1111: prio bands 16 >/dev/null 2>/dev/null
    echo "[Command]: tc qdisc add dev $interface root handle 1111: prio bands 16 >/dev/null 2>/dev/null"
    echo ""
    tc qdisc add dev $interface parent 1111:$1 handle $1: netem delay $delay_time loss $2 duplicate $3 corrupt $4
    echo "[Command]: tc qdisc add dev $interface parent 1111:$1 handle $1: netem delay $delay_time loss $2 duplicate $3 corrupt $4"
    echo ""

}




write_tc_filter_rule()
{
    #1st parameter means mark value.
    #2nd parameter means tc handle id.

    tc filter add dev $interface protocol ip parent 1111: handle $1 fw flowid 1111:$2
    cc="tc filter add dev $interface protocol ip parent 1111: handle $1 fw flowid 1111:$2"
    echo "[Command]: "$cc
    echo ""

}


main()
{


    for ((iptables_mark_a=1;iptables_mark_a<=11;iptables_mark_a++))
    do

        if [[ $iptables_mark_a == 2 ]]; then
            continue
        fi
        if [[ $iptables_mark_a == 11 ]]; then
            echo ""
            echo "There can be 9 tc rules at most.    [Fail]"
            echo ""
            exit
        fi


        mark_value_a="231$iptables_mark_a"
        formal_mark_value_a=`printf "%x" $mark_value_a`

        real_mark_line_a=`iptables -t mangle -nvL POSTROUTING | grep -n ".*" | grep "MARK.*$interface.*MARK set 0x$formal_mark_value_a" | awk -F ":" '{print $1}'`

        if [[ $real_mark_line_a == "" ]]; then
            tc filter show dev $interface | grep "handle 0x$formal_mark_value_a" >/dev/null
            if [[ $? == 0 ]]; then
                continue
            else
                tc qdisc show dev $interface | grep "parent 1111:$iptables_mark_a"  > /dev/null
                if [[ $? == 0 ]]; then
                    continue
                else 
                    if [[ $drop_pac_function == no ]]; then
                        write_iptables_rule $mark_value_a
                    elif [[ $drop_pac_function == yes ]]; then
                    
                        drop_packet_nth $mark_value_a $packet_num_string $every_number
                    fi
                    write_tc_qdisc_rule $iptables_mark_a $tc_loss $tc_duplicate $tc_corrupt
                    write_tc_filter_rule $mark_value_a $iptables_mark_a
                    break
                fi
            fi
        else
            continue
        fi
    done

}


result()
{

    echo ""
    echo ""
    echo "********************************************* DETAILS *********************************************"
    echo ""
    echo "-----------------------------------------tc qdisc of $interface-----------------------------------------"
    tc qdisc show dev $interface
    echo ""
    echo "-----------------------------------------tc filter of $interface-----------------------------------------"
    tc filter show dev $interface
    echo ""
    echo "-----------------------------------------iptables rule-----------------------------------------"
    iptables -t mangle -nvL POSTROUTING
    echo "iptables -t mangle -nvL POSTROUTING"
    echo ""

}



final_result()
{
    echo ""
    echo  "**************************************** FINAL RESULT ****************************************"

    all_mark_num=(0x907 0x909 0x90a 0x90b 0x90c 0x90d 0x90e 0x90f 0x5a46)

    total_ipta_line=`iptables -t mangle -nvL POSTROUTING | wc -l`
    let real_total_ipta_line=$total_ipta_line-2

    for ((ipta_num=1;ipta_num<=$real_total_ipta_line;ipta_num++))
    do
        let now_ipta_num=$ipta_num+2

        for new_i in ${all_mark_num[@]}
        do
            iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" |  grep "MARK.*$interface.*MARK set ${new_i}" >/dev/null
            if [[ $? == 0 ]]; then
                iptables_src=`iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" | awk '{print $8}'`
                iptables_dst=`iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" | awk '{print $9}'`
                iptables_pro=`iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" | awk '{print $4}'`
                filter_classid=`tc filter show dev $interface | grep "${new_i}" | awk -F "classid" '{print $2}'`
                qdisc_num=`echo $filter_classid | awk -F ":" '{print $2}'`
                qdisc_delay=`tc qdisc show dev $interface | grep "qdisc netem $qdisc_num:" | awk -F "delay" '{print $2}' | awk '{print $1}'`
                qdisc_loss=`tc qdisc show dev $interface | grep "qdisc netem $qdisc_num:" | awk -F "loss" '{print $2}' | awk '{print $1}'`
                qdisc_duplicate=`tc qdisc show dev $interface | grep "qdisc netem $qdisc_num:" | awk -F "duplicate" '{print $2}' | awk '{print $1}'`
                qdisc_corrupt=`tc qdisc show dev $interface | grep "qdisc netem $qdisc_num:" | awk -F "corrupt" '{print $2}' | awk '{print $1}'`
      
                iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p"| grep "statistic mode nth every" >/dev/null
                whether_every=$?

                if [[ $whether_every == 1 ]]; then

                    echo "No. $ipta_num int=$interface; proto=$iptables_pro; src_addr=$iptables_src; dst_addr=$iptables_dst; tc.delay=$qdisc_delay tc.loss=$qdisc_loss; tc.dup=$qdisc_duplicate; tc.corr=$qdisc_corrupt ."
                elif [[ $whether_every == 0 ]]; then
                    iptables_every=`iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" | awk '{print $14}'`
                    iptables_packet=`iptables -t mangle -nvL POSTROUTING | sed -n "$now_ipta_num, $now_ipta_num p" | awk '{print $16}'`
                    echo "No. $ipta_num int=$interface; proto=$iptables_pro; src_addr=$iptables_src; dst_addr=$iptables_dst; ipta.every=$iptables_every; ipta.pkt=$iptables_packet; tc.loss=$qdisc_loss tc.delay=$qdisc_delay; tc.dup=$qdisc_duplicate; tc.corr=$qdisc_corrupt ."

                fi
            fi
        done

    done

    echo ""


}



init_parameter()
{

    #Init parameter
    if [[ $delay_time == null ]]; then
        delay_time=0ms
    fi
    if [[ $protocol == null ]]; then
        protocol=icmp
    fi
    if [[ $tc_loss == null ]]; then
        tc_loss="0%"
    fi
    if [[ $src_address == "null" ]]; then
        src_address=0.0.0.0/0
    fi
    if [[ $dst_address == "null" ]]; then
        dst_address=0.0.0.0/0
    fi
    if [[ $tc_duplicate == null ]]; then
        tc_duplicate="0%"
    fi
    if [[ $tc_corrupt == null ]]; then
        tc_corrupt="0%"
    fi


}

check_parameter()
{


    if [[ $src_address == null && $dst_address == null && $protocol && $every_number == null && $packet_num_string == null && $delay_time == null && $tc_loss == null && $clear_config == no && $display_config == no && $tc_duplicate == null && $tc_corrupt == null ]]; then

        final_result
        exit

    fi



    if [[ $every_number == "null" && $packet_num_string != "null" ]]; then
        cathelp
    elif [[ $every_number != "null" && $packet_num_string == "null" ]]; then
        cathelp
    elif [[ $every_number == "null" && $packet_num_string == "null" ]]; then
        drop_pac_function=no
    else
        drop_pac_function=yes

    fi



}


############################## function ##############################

check_parameter
init_parameter


if [[ $clear_config == yes ]]; then
    clear_configuration
fi

if [[ $display_config == yes ]]; then
    result
    final_result
    exit

fi



main
final_result

