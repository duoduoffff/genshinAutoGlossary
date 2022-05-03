#! /usr/local/bin/python3

def get(textSea, textMapId):
    result = textSea[str(textMapId)]
    if len(result) > 0:
        return result