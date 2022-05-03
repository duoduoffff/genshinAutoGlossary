#! /usr/local/bin/python3

import re

def removeBrackets(string):
    chars = ""
    for char in string:
        if char != "「" and char != "」":
            chars += char

    return chars

def removeMinusChar(string):
    chars = string.split("-")
    return chars[-1]

def removeMiddot(string):
    chars = string.split("·")
    return chars[0]

def removeRecipe(string):
    chars = string.split("：")
    return chars[-1]

def removeDSL(string):
    remTest = re.search(r'test|测试', string)
    remCommonAtk = re.search(r'普攻', string)
    remBP = re.search(r'BP', string)
    remDeprecated = re.search(r'（废弃）', string)
    remSpecialChars = re.search(r'《|》|（|）|<|>|\/|{|}', string)
    if(remTest or remBP or remDeprecated or remSpecialChars or remCommonAtk):
        pass
    elif string:
        return string

def removeTooLongStrs(string):
    if(string and len(string) > 7):
        pass
    else:
        return string

def removeNonChineseChars(string):
    if(string):
        Chinese = re.match(r'^[\u4e00-\u9fa5]+$', string)
        if(Chinese):
            return string
        else:
            pass