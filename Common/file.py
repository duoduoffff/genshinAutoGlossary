#! /usr/local/bin/python3

# Reads files.

import json

class FileOperations():
    """File operations"""
    def readAsJson(fileName):
        fhandle = open(fileName, "r", encoding='utf-8')
        jsonObj = json.loads(fhandle.read())
        fhandle.close()
        return jsonObj

    def readAsPlainText(fileName):
        fhandle = open(fileName, "r", encoding='utf-8')
        str = fhandle.read()
        fhandle.close()
        return str

    def writeToFile(content, fileName):
        with open(fileName, "w", encoding='utf-8') as f:
            f.write(content)

    def appendToFile(content, fileName):
        with open(fileName, "a", encoding='utf-8') as f:
            f.write(content)
            f.write("\n")
