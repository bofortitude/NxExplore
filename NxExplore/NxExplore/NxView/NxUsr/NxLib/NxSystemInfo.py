#!/usr/bin/python


import os



def diskUsage(directoryPath):
    try:
        disk = os.statvfs(directoryPath)
        percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail)
        return int(percent)
    except Exception as e:
        return False

