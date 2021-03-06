#!/usr/bin/python


import sys

def runInfo4Us(*args, **kwargs):
    from NxView.NxUsr.NxBin import EnInfo4Us
    EnInfo4Us.start(*args, **kwargs)

def runCheckConnectivity(*args, **kwargs):
    from NxView.NxUsr.NxBin import EnCheckConnectivity
    EnCheckConnectivity.start(*args, **kwargs)

def runImustang(*args, **kwargs):
    from NxView.NxUsr.NxBin import EnImustang
    EnImustang.start(*args, **kwargs)

def runImustang2(*args, **kwargs):
    from NxView.NxUsr.NxBin import EnImustang2
    EnImustang2.start(*args, **kwargs)

def runTrial(*args, **kwargs):
    from NxView.NxUsr.NxBin import EnTrial
    EnTrial.start(*args, **kwargs)



projectNameMap = {
    'Info4Us':eval('runInfo4Us'),
    'CheckConnectivity': eval('runCheckConnectivity'),
    'iMustang': eval('runImustang'),
    'iMustang2': eval('runImustang2'),
    'Trial': eval('runTrial')

}


def showHelp():
    print ''
    print 'Usage:'
    print ''
    print str(sys.argv[0]) + ' <project name> [Parameters]'
    print ''
    print 'Available project name:'
    for i in projectNameMap:
        print i
    print ''
    exit()



if __name__ == '__main__':
    if len(sys.argv) < 2:
        showHelp()
    else:
        if sys.argv[1] not in projectNameMap:
            showHelp()
        else:
            projectNameMap[sys.argv[1]](sys.argv[2:])



