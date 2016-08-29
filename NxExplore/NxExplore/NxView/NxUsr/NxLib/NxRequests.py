#!/usr/bin/python



import socket

from ..NxExternalLibs import requests
from ..NxExternalLibs.requests.packages.urllib3.poolmanager import PoolManager
from ..NxExternalLibs.requests.adapters import HTTPAdapter



class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super(SourceAddressAdapter, self).__init__(**kwargs)
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       socket_options=[(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)],
                                       source_address=self.source_address,
                                       )


class NxRequests():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'NxRequests/by NxRequests'}
        self.cookies = {}
        self.data = {}
        self.session.verify = False
        self.json = {}

    def addHeader(self, name, value):
        self.headers[name] = value
        self.session.headers.update(self.headers)

    def addCookie(self, name, value):
        self.cookies[name] = value
        self.session.cookies.update(self.cookies)

    def addData(self, name, value):
        self.data[name] = value

    def setAuth(self, username, password):
        self.session.auth = (username, password)

    def addJson(self, key, value):
        self.json[key] = value

    def setVerify(self, verify):
        # verify = True or False
        self.session.verify = verify

    def mountAdapter(self, adapter, prefix=None):
        if prefix:
            self.session.mount(prefix, adapter)
        else:
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)

    def setSourceAddr(self, srcAddress, srcPort):
        # srcAddress is string
        # srcPort is integer
        self.mountAdapter(SourceAddressAdapter(srcAddress, srcPort))

    def resetSession(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'NxRequests/by NxRequests'}
        self.cookies = {}
        self.data = {}
        self.session.verify = False
        self.json = {}

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def options(self, url, **kwargs):
        return self.session.options(url, **kwargs)

    def head(self, url, **kwargs):
        return self.session.head(url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(url, data=self.data, json=self.json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data=self.data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.session.patch(url, data=self.data, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)







if __name__ == '__main__':
    #myRequest = NxRequests()
    #myRequest.addJson('key1', 'value1')
    #print myRequest.post('http://www.google.com')
    pass






