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
# from . import getFurnitureNames

def getAllItems(dir):
    objects = []
    # https://stackoverflow.com/questions/4117588/non-recursive-os-walk
    for root, dirs, filenames in os.walk(dir):
        for fileName in filenames:
            combinedPath = "{0}/{1}".format(dir, fileName)
            jsonObj = file.FileOperations.readAsJson(combinedPath)
            targets = jsonObj["furnitureUnits"]

            objects.extend(targets)
        break

    allFurnitures = []
    for item in objects:
        allFurnitures.append(item["furnitureID"])

    return allFurnitures

def getTextMapHashByFurniture(id):
    basePath = conf.dataPath
    furnitureNamesConfig = "{0}{1}".format(basePath, config.furnitureExcelData)
    furnitureNames = file.FileOperations.readAsJson(furnitureNamesConfig)

    # print(furnitureNames)

    targetObj = list(filter(lambda x: x["id"] == id, furnitureNames))
    # print("@41: " + json.dumps(targetObj))
    return targetObj[0]["nameTextMapHash"]

def getReadableNames(textSea, id):
    return text.get(textSea, id)

def exec(textSea):
    print("Converting Homeworld...")
    basePath = conf.dataPath
    furnSuitData = "{0}{1}".format(basePath, config.furnitureSuitData)
    all = []
    furnitures = getAllItems(furnSuitData)
    for furniture in furnitures:
        textMapHash = getTextMapHashByFurniture(furniture)
        readable = getReadableNames(textSea, textMapHash)

        readable = sanitize.removeBrackets(readable)
        readable = sanitize.removeMinusChar(readable)
        readable = sanitize.removeNonChineseChars(readable)

        if (len(readable) > 0):
            all.append(readable)

    # print(all)
    all = dedup.exec(all)
    print("Converted {0} items.\n".format(str(len(all))))
    return all