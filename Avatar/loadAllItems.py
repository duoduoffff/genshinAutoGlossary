#! /usr/local/bin/python3

import os, json

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
    combinedPath = "{0}/{1}".format(basePath, config.avatarExcelConfigData)
    allAvatars = file.FileOperations.readAsJson(combinedPath)

    result = []
    for item in allAvatars:
        result.append(item["NameTextMapHash"])

    return result

def getReadableNames(textSea, id):
    return text.get(textSea, id)

def exec(textSea):
    print("Converting Avatars...")
    all = []
    avatars = getAllNames()
    for avatar in avatars:
        readable = getReadableNames(textSea, avatar)
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