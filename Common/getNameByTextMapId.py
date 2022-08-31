#! /usr/local/bin/python3

def get(textSea, textMapId):
    if str(textMapId) in textSea:
        result = textSea[str(textMapId)]
        if len(result) > 0:
            return result