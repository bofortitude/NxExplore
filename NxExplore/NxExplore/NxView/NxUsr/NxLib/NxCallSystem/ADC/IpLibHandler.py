#!/usr/bin/python

import os
from ... import IpNet
import random


ip_handler = IpNet.ip_net()

lib_path = os.path.split(os.path.realpath(__file__))[0]+'/IpLibrary'
country_map = 'country_map.txt'
ipv4_map = 'ipv4_map.txt'
ipv6_map = 'ipv6_map.txt'
pre_define_isp = 'pre-define-isp'
geo_ip_sub = 'geo_ip_sub'
ipv4_geo_ip_sub = 'ipv4'
ipv6_geo_ip_sub = 'ipv6'


all_file_list = os.listdir(lib_path)




def clear_field(line):
    line_field = line.split(';')
    new_field = []
    for i in line_field:
        new_field.append(i.replace('\t', '').replace('\n', ''))
    return new_field



def split_geo_files():
    # Suppose all the files exist
    if not os.path.exists(lib_path+'/'+geo_ip_sub):
        os.makedirs(lib_path+'/'+geo_ip_sub)

    if ipv4_map in all_file_list:
        id_to_ipv4 = {}
        last_line = None
        for line in open(lib_path + '/' + ipv4_map):
            if last_line == None or last_line.find(';') == -1 or line.find(';') == -1:
                last_line = line
                continue
            last_field = clear_field(last_line)
            current_field = clear_field(line)

            last_ip_range = (int(last_field[0]), int(current_field[0]) - 1)
            if last_field[2] in id_to_ipv4:
                id_to_ipv4[last_field[2]].append(last_ip_range)
            else:
                id_to_ipv4[last_field[2]] = [last_ip_range]
            last_line = line

        if not os.path.exists(lib_path+'/'+geo_ip_sub+'/'+ipv4_geo_ip_sub):
            os.makedirs(lib_path+'/'+geo_ip_sub+'/'+ipv4_geo_ip_sub)
        for (i, j) in id_to_ipv4.items():
            file_obj = open(lib_path+'/'+geo_ip_sub+'/'+ipv4_geo_ip_sub+'/'+i, 'w')
            for k in j:
                file_obj.write(str(k[0])+' '+str(k[1])+'\n')
            file_obj.close()

    if ipv6_map in all_file_list:
        id_to_ipv6 = {}
        for line in open(lib_path + '/' + ipv6_map):
            line_field = line.split()
            if len(line_field) < 3:
                continue
            if line_field[2] in id_to_ipv6:
                id_to_ipv6[line_field[2]].append((line_field[0], line_field[1]))
            else:
                id_to_ipv6[line_field[2]] = [(line_field[0], line_field[1])]

        if not os.path.exists(lib_path+'/'+geo_ip_sub+'/'+ipv6_geo_ip_sub):
            os.makedirs(lib_path+'/'+geo_ip_sub+'/'+ipv6_geo_ip_sub)
        for (l, m) in id_to_ipv6.items():
            file_obj = open(lib_path+'/'+geo_ip_sub+'/'+ipv6_geo_ip_sub+'/'+l, 'w')
            for n in m:
                file_obj.write(n[0]+' '+n[1]+'\n')
            file_obj.close()




def get_country_map():
    if country_map in all_file_list:
        #id_to_country = {}
        country_to_id = {}
        for line in open(lib_path + '/' + country_map):
            new_field = clear_field(line)
            #id_to_country[new_field[3]] = new_field[4]
            country_to_id[new_field[4]] = new_field[0]
        return country_to_id
    else:
        return False

def get_country_id(country_name):
    if country_map in all_file_list:
        for line in open(lib_path + '/' + country_map):
            new_field = clear_field(line)
            if new_field[4] == country_name:
                return new_field[0]
        return False
    else:
        return False




def get_country_ip_list(category, total, address_type):
    country_id = get_country_id(category)
    if country_id == False:
        return False

    ip_range_list = []
    if address_type == 'IPv4':
        if not os.path.exists(lib_path + '/' + geo_ip_sub + '/' + ipv4_geo_ip_sub):
            split_geo_files()
        elif country_id not in os.listdir(lib_path + '/' + geo_ip_sub + '/'+ipv4_geo_ip_sub):
            split_geo_files()
        if country_id not in os.listdir(lib_path + '/' + geo_ip_sub + '/'+ipv4_geo_ip_sub):
            return False
        whole_ip_list = []
        for line in open(lib_path + '/' + geo_ip_sub + '/'+ipv4_geo_ip_sub+'/'+country_id):
            splited_line = line.split()
            whole_ip_list.append((int(splited_line[0]), int(splited_line[1])))

        for i in xrange(total):
            random_line = random.sample(whole_ip_list, 1)[0]
            current_selection = random.randint(random_line[0], random_line[1])
            ip_range_list.append(ip_handler.int_to_ip(current_selection))

        return ip_range_list

    elif address_type == 'IPv6':
        if not os.path.exists(lib_path + '/' + geo_ip_sub + '/' + ipv6_geo_ip_sub):
            split_geo_files()
        elif country_id not in os.listdir(lib_path + '/' + geo_ip_sub + '/'+ipv6_geo_ip_sub):
            split_geo_files()
        if country_id not in os.listdir(lib_path + '/' + geo_ip_sub + '/' + ipv6_geo_ip_sub):
            return False

        whole_ip6_list = []
        for line in open(lib_path + '/' + geo_ip_sub + '/'+ipv6_geo_ip_sub+'/'+country_id):
            splited_line = line.split()
            whole_ip6_list.append((splited_line[0], splited_line[1]))

        for j in xrange(total):
            random_line = random.sample(whole_ip6_list, 1)[0]
            start_ip6 = ip_handler.ip_to_int(random_line[0])
            end_ip6 = ip_handler.ip_to_int(random_line[1])
            current_selection = random.randint(start_ip6, end_ip6)
            ip_range_list.append(ip_handler.int_to_ip(current_selection, format='ipv6'))
        return ip_range_list


def get_isp_province_dict():
    isp_dict = {}
    province_dict = {}
    isp_province_dict = {}
    if pre_define_isp not in all_file_list:
        return isp_dict, province_dict, isp_province_dict

    isp_file_list = []
    for line in open(lib_path+'/'+pre_define_isp):
        if line.find('Version') != -1:
            continue
        stripped_line = line.replace('\n', '')
        if stripped_line == '':
            continue
        isp_file_list.append(stripped_line)

    current_isp = 'isp_none'
    current_province = 'province_none'
    for i in isp_file_list:
        if i.find('ISP name') != -1:
            current_isp = i.split(':')[1]
        elif i.find('Province') != -1:
            current_province = i.split(':')[1]
        else:
            if current_isp not in isp_dict:
                isp_dict[current_isp] = [i]
            else:
                isp_dict[current_isp].append(i)
            if current_province not in province_dict:
                province_dict[current_province] = [i]
            else:
                province_dict[current_province].append(i)
            if (current_isp, current_province) not in isp_province_dict:
                isp_province_dict[(current_isp, current_province)] = [i]
            else:
                isp_province_dict[(current_isp, current_province)].append(i)

    return isp_dict, province_dict, isp_province_dict


def get_isp_ip_list(category, total, address_type):
    if address_type != 'IPv4':
        return False
    # category format:  'china-telecom Anhui', 'china-telecom any', 'any Anhui', 'any, any'=False
    isp_splited = category.split()
    if len(isp_splited) < 2:
        return False
    if isp_splited[0] == 'any' and isp_splited[1] == 'any':
        return False

    isp_dict, province_dict, isp_province_dict = get_isp_province_dict()
    if isp_dict == {} and province_dict == {} and isp_province_dict == {}:
        return False
    if isp_splited[0] == 'any' and isp_splited[1] != 'any':
        #'any Anhui'
        if isp_splited[1] not in province_dict:
            return False
        final_ip_list = []
        for i in xrange(total):
            current_subnet = random.sample(province_dict[isp_splited[1]], 1)[0]
            final_ip_list.append(ip_handler.ip_random(current_subnet, 1)[0])
        return final_ip_list

    elif isp_splited[0] != 'any' and isp_splited[1] == 'any':
        #'china-telecom any'
        if isp_splited[0] not in isp_dict:
            return False
        final_ip_list = []
        for j in xrange(total):
            current_subnet = random.sample(isp_dict[isp_splited[0]], 1)[0]
            final_ip_list.append(ip_handler.ip_random(current_subnet, 1)[0])
        return final_ip_list

    else:
        #'china-telecom Anhui'
        if (isp_splited[0], isp_splited[1]) not in isp_province_dict:
            return False
        final_ip_list = []
        for k in xrange(total):
            current_subnet = random.sample(isp_province_dict[(isp_splited[0], isp_splited[1])], 1)[0]
            final_ip_list.append(ip_handler.ip_random(current_subnet, 1)[0])
        return final_ip_list





def get_ip_list(lib_type, category, total, ipv6=False):
    lib_type_list = ['ISP', 'Country']
    if ipv6 == False:
        address_type = 'IPv4'
    else:
        address_type = 'IPv6'
    if lib_type not in lib_type_list:
        return False

    if lib_type == 'Country':
        return get_country_ip_list(category, total, address_type)
    elif lib_type == 'ISP':
        return get_isp_ip_list(category, total, address_type)





if __name__ == '__main__':
    split_geo_files()
    #get_ip_list('ISP', 'china-telecom any')













