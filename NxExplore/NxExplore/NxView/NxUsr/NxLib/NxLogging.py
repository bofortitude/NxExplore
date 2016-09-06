#!/usr/bin/python

import logging
import logging.handlers



'''

%(name)s Logger       # logger's name
%(levelno)s           # numberic type log level
%(levelname)s         # text type log level
%(pathname)s          #
%(filename)s
%(module)s
%(funcName)s
%(lineno)d
%(created)f
%(relativeCreated)d
%(asctime)s
%(thread)d
%(threadName)s
%(process)d
%(message)s

'''

def setSimpleLogging(logFile = None, debug=True, maxBytes=10000000, backupCount=3):
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handlersList = list(logger.handlers)
    if handlersList != []:
        for i in handlersList:
            logger.handlers.remove(i)

    consoleHandler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s : %(message)s')
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


    if logFile is not None:
        #fileHandler = logging.FileHandler(logFile)
        #fileHandler.setFormatter(formatter)
        #logger.addHandler(fileHandler)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(logFile, maxBytes=maxBytes, backupCount=backupCount)
        rotatingFileHandler.setFormatter(formatter)
        logger.addHandler(rotatingFileHandler)

    # filter = logging.Filter('mylogger.child1.child2')
    # fileHandler.addFilter(filter)
    # logger.addFilter(filter)



