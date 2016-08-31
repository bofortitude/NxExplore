#!/usr/bin/python

import ConfigParser
import os

class NxConfig():
    def __init__(self, configFile):
        self.configFile = configFile
        if not os.path.isfile(self.configFile):
            file = open(self.configFile, 'w')
            file.close()
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.configFile)

    def getSections(self):
        return self.conf.sections()

    def getItemsOfSection(self, section):
        ''' Return False, if no this section'''
        if not self.conf.has_section(section):
            return False
        return self.conf.items(section)

    def getValueOfOption(self, section, option):
        ''' Return False, if has no item.'''
        if not self.conf.has_section(section):
            return False
        if not self.conf.has_option(section, option):
            return False
        return self.conf.get(section, option)

    def addSection(self, section):
        self.conf.add_section(section)
        self.writeToFile()

    def addSectionNoWriting(self, section):
        self.conf.add_section(section)

    def setValueOfOption(self, section, option, value):
        if not self.conf.has_section(str(section)):
            self.addSection()
        self.conf.set(str(section), str(option), str(value))
        self.writeToFile()

    def setValueOfOptionNoWriting(self, section, option, value):
        if not self.conf.has_section(str(section)):
            self.addSection()
        self.conf.set(str(section), str(option), str(value))

    def removeSection(self, section):
        self.conf.remove_section(section)
        self.writeToFile()

    def removeSectionNoWriting(self, section):
        self.conf.remove_section(section)

    def removeOption(self, section, option):
        if not self.conf.has_section(section):
            return
        self.conf.remove_option(section, option)
        self.writeToFile()

    def removeOptionNoWriting(self, section, option):
        if not self.conf.has_section(section):
            return
        self.conf.remove_option(section, option)


    def writeToFile(self, newFile=None):
        if newFile:
            self.conf.write(open(newFile, 'w'))
        else:
            self.conf.write(open(self.configFile, 'w'))

    def getConfigObj(self):
        return self.conf







