#!/usr/bin/python


from Link2InfoWeb import Link2InfoWeb

from ....NxUsr.NxLib.NxCallSystem.Linux.RunShellCommand import RunShellCommand




'''
 wget --timeout 10 --tries=5 --no-check-certificate --no-cookies
 --header "Cookie: _cmportal=BAh7CEkiCHVpZAY6BkVGSSIKYm9mZWkGOwBUSSIPcHJvamVjdF9pZAY7AEZJIggxMjMGOwBGSSIPc2Vzc2lvbl9pZAY7AFRJIiU2Y2EzOTRjN2I3OWNiNjM1MmQ1MTExMGM5MTBiMGQxNgY7AFQ%3D--48844f3c32dc31141fe37ea846044beba700fc9e"
 https://info.fortinet.com/files/FortiADC/v4.00/Images/build0645/FAD_100F-V400-build0645-FORTINET.out -O /root/Temp/aa.out

'''



class WgetDownload():
    def __init__(self, timeout=60, tries=5):
        self.timeout = timeout
        self.tries = tries
        self.CommandRun = RunShellCommand()

    def download(self, url, cookie, dstPath):
        imageName = str(url).split('/')[-1]
        downloadCommand = 'wget --timeout '+str(self.timeout)+' --tries='+str(self.tries)\
                          +' --no-check-certificate --no-cookies --header "Cookie: _cmportal='+str(cookie)+'" '+str(url)+' -O '+dstPath+'/'+imageName
        self.CommandRun.addRunningCommand(downloadCommand)

    def wait(self):
        self.CommandRun.wait4Subprocess()






