#!/usr/bin/env python
cctModulePath = None

def setModulePath(newpath):
    global cctModulePath
    cctModulePath = newpath
    
def getModulePath():
    global cctModulePath
    return cctModulePath