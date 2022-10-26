#! /usr/local/bin/python3

import json
from . import file
from . import conf

def loadSea():
    dataPath = conf.dataPath
    mapLoc = conf.chsTextSeaPath
    combinedPath = "{0}{1}".format(dataPath, mapLoc)

    return file.FileOperations.readAsJson(combinedPath)
