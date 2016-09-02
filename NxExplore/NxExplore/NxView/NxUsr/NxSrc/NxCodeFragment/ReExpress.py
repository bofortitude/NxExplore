#!/usr/bin/python

import re


pattern = re.compile('^build\d+$')
if pattern.search('build23'):
    print True


