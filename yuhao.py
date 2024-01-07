#!/usr/local/bin/python3

import re
import json
import requests

from Common import getCurrentVersion as ver
from Common import file
from Common import loadYml
from Common import load
from Common import gen
from Common import conf

globalProxySettings = {
        "http": "http://127.0.0.1:7890"
    }

def parseCsvSp(content, head=True):
    delim = ","
    
    lines = content.splitlines()
    if(head == True):
        del lines[0]
    
    finItems = []
    for line in lines:
        items = line.split(delim)
        fcItem = {
            "char": items[0],
            "fullcode": items[1],
        }
        finItems.append(fcItem)
        
    return finItems

def toLowercase(ctt):
    return ctt.lower()

def convertSpecialAlphabetVariation(fullcode):
    return re.sub(r'ⓐ|ⓑ|ⓒ|ⓓ|ⓔ|ⓕ|ⓖ|ⓗ|ⓘ|ⓙ|ⓚ|ⓛ|ⓜ|ⓝ|ⓞ|ⓟ|ⓠ|ⓡ|ⓢ|ⓣ|ⓤ|ⓥ|ⓦ|ⓧ|ⓨ|ⓩ',
                      lambda x: chr(ord(x.group()) - 9424), fullcode)

def parseFullDict(filePath):
    skip = False
    csv = ""
    with open(filePath, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.strip() == '---':
                skip = True
                continue
            if line.strip() == "...":
                skip = False
                continue

            if line.strip() and skip == False and not line.startswith('#') and not line.startswith('---') and not line.startswith("..."):
                char, code = line.strip().split('\t')
                csv += char
                csv += ","
                csv += code
                csv += "\n"
    print(csv.split("\n")[0])
    return csv

def downloadFullCode(variant="light", 
                     repo="forFudan/yuhao", 
                     domain="raw.githubusercontent.com", 
                     commit="main",
                     enableProxy=True,
                     timeout=30):
    url = "https://{0}/{1}/{3}/{2}/chaifen/%E5%AE%87%E6%B5%A9%E8%BC%B8%E5%85%A5%E6%B3%95%E5%85%A8%E6%BC%A2%E5%AD%97%E6%8B%86%E5%88%86%E8%A1%A8.csv".format(domain, repo, variant, commit)
    print("Requesting fullcode...")
    if(enableProxy == False):
        fullCode = requests.get(url, stream=True, timeout=timeout)
    else:
        fullCode = requests.get(url, stream=True, proxies=globalProxySettings, timeout=timeout)
    print("Parsing fullcode...")
    fullCode = fullCode.content.decode('utf-8')
    #fullCode.raw.decode_content = True # Content-Encoding
    print(fullCode[0:20])
    
    return fullCode

def fullCodeDict(fullcodeobj):
    return {obj['char']: obj for obj in fullcodeobj}
    
def getFullCodeForChar(char, fullcodedict):
    char_info = fullcodedict.get(char)
    return char_info["fullcode"] if char_info is not None else None
    
def preprocessFullCode(fullcode):
    fullCodeObj = parseCsvSp(fullcode)
    sanitizedFullCode = []
    for char in fullCodeObj:
        sanitizedCode = convertSpecialAlphabetVariation(char["fullcode"])
        sanitizedCode = toLowercase(sanitizedCode)
        char["fullcode"] = sanitizedCode
        sanitizedFullCode.append(char)
    return sanitizedFullCode

def getInputCharForPhrase(phrase, fullCode):
    phraseLength = len(phrase)
    inputChar = ""
    for i in range(phraseLength):
        charCode = getFullCodeForChar(phrase[i], fullCode)
        if charCode is None:
            # print(phrase[i])
            return ""

    if(phraseLength) == 2:
        inputChar += getFullCodeForChar(phrase[0], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[0], fullCode)[1]
        inputChar += getFullCodeForChar(phrase[1], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[1], fullCode)[1]
    elif(phraseLength) == 3:
        inputChar += getFullCodeForChar(phrase[0], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[1], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[2], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[2], fullCode)[1]
    elif(phraseLength) >= 4:
        inputChar += getFullCodeForChar(phrase[0], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[1], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[2], fullCode)[0]
        inputChar += getFullCodeForChar(phrase[-1], fullCode)[0]
    elif(phraseLength) == 1:
        inputChar = getFullCodeForChar(phrase[0], fullCode)
    else:
        inputChar = ""
    
    return inputChar

def genYuhao():
    print("Generating...\n")
    fullDictPath = "{0}/yuhao.full.dict.yaml".format(conf.prodPath)
    fullCode = parseFullDict(fullDictPath)
    fullCode = parseCsvSp(fullCode, head=False)
    fullCodeDictVar = fullCodeDict(fullCode)
    tab = "\t"
    
    bigArray = gen.genFe()
    result = genSkeleton()
    
    for item in bigArray:
        inputChar = getInputCharForPhrase(item, fullCodeDictVar)
        # print("{0} -> {1}".format(item, inputChar))
        result += item
        result += tab
        result += inputChar
        result += "\n"
    
    return result

def genSkeleton():
    text = "---\n"
    text += "name: {0}\n".format('"yuhao.genshin"')
    text += "version: {0}\n".format(ver.get())
    text += "sort: original\n"
    text += "columns:\n"
    text += "  - text\n"
    text += "  - code\n"
    text += "..."
    text += "\n\n"

    return text
    
if __name__ == '__main__':
    text = genYuhao()
    combinedPath = "./{0}/{1}".format(conf.buildPath, "yuhao.genshin.dict.yaml")
    file.FileOperations.writeToFile(text, combinedPath)
    