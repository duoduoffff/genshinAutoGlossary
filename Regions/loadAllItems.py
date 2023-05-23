#! /usr/local/bin/python3

import os, json, re

import sys
sys.path.append("..")
from Common import load
from Common import conf
from Common import file
from Common import dedup
from Common import sanitize
from Common import getNameByTextMapId as text

from . import config

def getAllNames():
    objects = []
    
    basePath = conf.dataPath
    combinedPath = "{0}/{1}".format(basePath, config.mapExcelConfigData)
    allRegions = file.FileOperations.readAsJson(combinedPath)

    result = []
    for item in allRegions:
        stringType = item["textMapId"]

        if(item is not None):
            areaPattern = re.search(r'UI\_MAP_AREA', stringType)
            cityPattern = re.search(r'UI\_MAP_City', stringType)
            if (areaPattern or cityPattern):
                result.append(item["textMapContentTextMapHash"])

    return result

def getReadableNames(textSea, id):
    return text.get(textSea, id)

def exec(textSea):
    print("Converting Regions...")
    all = []
    regions = getAllNames()
    for region in regions:
        readable = getReadableNames(textSea, region)
        if (readable and len(readable) > 0):
            readable = sanitize.removeBrackets(readable)
            readable = sanitize.removeMinusChar(readable)
            readable = sanitize.removeMiddot(readable)
            readable = sanitize.removeDSL(readable)
            readable = sanitize.removeNonChineseChars(readable)
            if(readable):
                all.append(readable)

    # print(all)
    all = dedup.exec(all)
    print("Converted {0} items.\n".format(str(len(all))))
    return all