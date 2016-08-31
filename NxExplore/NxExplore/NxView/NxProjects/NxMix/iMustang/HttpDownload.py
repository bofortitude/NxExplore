#!/usr/bin/python


import threading


from Link2InfoWeb import Link2InfoWeb

from ....NxUsr.NxLib.NxCallSystem.Linux.RunShellCommand import RunShellCommand
from ....NxUsr.NxLib.DumpInfo import dumpInfo
from ....NxLib import requests




'''
 wget --timeout 10 --tries=5 --no-check-certificate --no-cookies
 --header "Cookie: _cmportal=BAh7CEkiCHVpZAY6BkVGSSIKYm9mZWkGOwBUSSIPcHJvamVjdF9pZAY7AEZJIggxMjMGOwBGSSIPc2Vzc2lvbl9pZAY7AFRJIiU2Y2EzOTRjN2I3OWNiNjM1MmQ1MTExMGM5MTBiMGQxNgY7AFQ%3D--48844f3c32dc31141fe37ea846044beba700fc9e"
 https://info.fortinet.com/files/FortiADC/v4.00/Images/build0645/FAD_100F-V400-build0645-FORTINET.out -O /root/Temp/aa.out

'''



class WgetDownload(): # Not available
    def __init__(self, timeout=60, tries=5):
        self.timeout = timeout
        self.tries = tries
        self.CommandRun = RunShellCommand()

    def download(self, url, cookie, dstPath):
        dumpInfo('Starting to download via wget command, the url is "'+str(url)+'" , the cookie is "'+str(cookie)+'", the dstPath is "'+str(dstPath)+'" .')
        imageName = str(url).split('/')[-1]
        downloadCommand = 'wget --timeout '+str(self.timeout)+' --tries='+str(self.tries)\
                          +' --no-check-certificate --no-cookies --header "Cookie: _cmportal='+str(cookie)+'" '+str(url)+' -O '+dstPath+'/'+imageName
        dumpInfo('The wget command is:')
        dumpInfo(downloadCommand, raw=True)
        self.CommandRun.addRunningCommand(downloadCommand)

    def wait(self):
        self.CommandRun.wait4Subprocess()



class PyRequestsDownload(threading.Thread):
    def __init__(self, url, cookies, dstPath):
        threading.Thread.__init__(self)
        self.url = url
        self.cookies = cookies
        self.dstPath = dstPath

    def run(self):
        local_filename = self.url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(self.url, stream=True, cookies=self.cookies)
        with open(self.dstPath + '/' + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush() commented by recommendation from J.F.Sebastian




