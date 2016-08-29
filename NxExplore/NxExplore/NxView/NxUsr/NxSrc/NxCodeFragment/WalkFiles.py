#!/usr/bin/python
import os

for root, dirs, files in os.walk("."):
    path = root.split('/')
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)
