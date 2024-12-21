#! /usr/local/bin/python3

import json
#import opencc
from . import file
from . import conf

yuhaoDb = "{0}/yuhao.full.dict.yaml".format(conf.prodPath)

def convert2Trad(text):
    import opencc
    converter = opencc.OpenCC("s2t.json")
    return converter.convert(text)

def convert2Json():
    yml = file.FileOperations.readAsPlainText(yuhaoDb)
    result = []
    lines = yml.split("\n")
    tab = "\t"
    for line in lines:
        if(tab in line):
            charInfo = line.split(tab)
            char = {
                "charName": charInfo[0],
                "charInput": charInfo[1]
            }
            if(len(char["charName"]) == 1 and len(char["charInput"]) == 4):
                result.append(char)
    
    return result

def selInput(char, selRange=[0, 3]):
    # enters a Chinsese character (which must be in traditional) and selects its charInput to the specified digit.
    # tradChar = convert2Trad(char)
    hJson = convert2Json()
    candidates = list(filter(lambda h: h["charName"] == char, hJson))
    
    if(len(candidates) == 1):
        charInput = candidates[0]["charInput"]
        return charInput[slice(selRange[0], selRange[1])]
    else:
        return ""
