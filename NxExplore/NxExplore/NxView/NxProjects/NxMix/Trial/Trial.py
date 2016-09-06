#!/usr/bin/python


import logging
from ....NxUsr.NxLib.NxLogging import setSimpleLogging
from ....NxEtc.NxPublicConfig.NxPredefined.PreDefault import *


def mainEn(*args, **kwargs):
    setSimpleLogging(logFile=NxVarLogPath+'/'+'GlobalLogs/myLog.log', debug=False)
    logging.info('this is the first line')
    setSimpleLogging(debug=True)
    logging.debug('new debug info')





