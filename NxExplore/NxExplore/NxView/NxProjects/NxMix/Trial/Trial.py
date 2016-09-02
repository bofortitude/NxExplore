#!/usr/bin/python





def mainEn(*args, **kwargs):
    from ..iMustang.CheckLocalStatus import checkDiskUsage
    checkDiskUsage(10)