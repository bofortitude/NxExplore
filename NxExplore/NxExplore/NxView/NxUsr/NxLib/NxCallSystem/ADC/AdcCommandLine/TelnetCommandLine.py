#!/usr/bin/python

import telnetlib
import time
import os
import sys


class TelnetCommandLine:
    def __init__(self, adc_ip, adc_port=23, username='admin', passwd='', expect_string='# '):

        self.adc_ip = adc_ip
        self.adc_port = adc_port
        self.username = username
        self.passwd = passwd
        self.expect_string = expect_string
        self.telnet_obj = telnetlib.Telnet()
        self.login()

    def record(self, content, linebreak=False, string_format=False):
        if string_format == False:
            if linebreak == False:
                print content,
            else:
                print content
        else:
            print '[' + time.ctime() + '] ' + content

    def login(self):
        self.record('', linebreak=True)
        self.record('Try to connect to "' + self.adc_ip + '" ...', string_format=True)
        self.telnet_obj.close()
        self.telnet_obj.open(self.adc_ip, port=self.adc_port, timeout=10)
        self.record('The connection has been established.', string_format=True)
        read_content = self.telnet_obj.read_until('login: ')
        self.record(read_content.rstrip())
        self.telnet_obj.write(self.username + '\n')
        read_content = self.telnet_obj.read_until('Password: ')
        self.record(read_content.rstrip())
        self.telnet_obj.write(self.passwd + '\n')
        read_content = self.telnet_obj.read_until(self.expect_string, timeout=10)
        self.record(read_content.rstrip())

    def run_cmd(self, command):
        try:
            self.telnet_obj.write(command + '\n')
            self.record(self.telnet_obj.read_until(self.expect_string, timeout=10).rstrip())
        except:
            self.record('', linebreak=True)
            self.record('Something wrong while running the command "' + command + '"!!!')
            raise StandardError

    def run_cmd_file(self, file_name):
        self.record('', linebreak=True)
        self.record('Start to run the file "' + file_name + '" ...', string_format=True)
        if not os.path.exists(file_name):
            self.record('The file "' + file_name + '" doesn\'t exist, nothing to do!!!', string_format=True)
            return
        my_file = open(file_name, 'r')
        file_lines = my_file.readlines()
        my_file.close()
        for i in file_lines:
            self.run_cmd(i.strip())
        self.record('', linebreak=True)
        self.record('The file "' + file_name + '" has been run over.', string_format=True)

    def return_root_view(self):
        self.telnet_obj.write('\n')
        read_content = self.telnet_obj.read_until(self.expect_string, timeout=10).rstrip()
        self.record(read_content)
        if read_content.find(') ' + self.expect_string.rstrip()) == -1:
            return
        for i in xrange(10):
            self.telnet_obj.write('\x03')  # send Ctrl-c combo
            read_content = self.telnet_obj.read_until(self.expect_string, timeout=10).rstrip()
            self.record(read_content)
            if read_content.find(') ' + self.expect_string.rstrip()) == -1:
                return
        self.re_login()

    def re_login(self):
        self.telnet_obj.close()
        self.login()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:'
        print ''
        print './TelnetCommandLine.py <ADC_IP> <CMD_File>'
        print ''
        exit()

    my_cmd = TelnetCommandLine(sys.argv[1])
    my_cmd.run_cmd_file(sys.argv[2])
