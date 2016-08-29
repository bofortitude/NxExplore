#!/usr/bin/python

from TelnetCommandLine import TelnetCommandLine



class AdvancedCLI():
    def __init__(self, adc_ip, adc_port=23, username='admin', passwd='', expect_string='# ',
                 current_vdom=None):
        # current_vdom:
        # None -> Not specified -> No vdom
        # global -> global
        self.cli_obj = TelnetCommandLine(adc_ip, adc_port=adc_port, username=username, passwd=passwd,
                                         expect_string=expect_string)
        self.current_vdom = current_vdom
        if self.current_vdom == None:
            pass


    def return_current_root_view(self):
        pass







if __name__ == '__main__':
    pass
