#! /usr/local/bin/python3

import opencc
# from snownlp import SnowNLP
import pypinyin

from . import load
from . import file
from . import dedup
from . import conf
from . import getCurrentVersion as ver

import sys # OPTIMIZE: streamline call of libs
sys.path.append("..")
from Avatar import loadAllItems as Avatar
from Homeworld import loadAllItems as Homeworld
from Material import loadAllItems as Material
from Regions import loadAllItems as Regions
from Weapon import loadAllItems as Weapon
from Artifact import loadAllItems as Artifact

def convertToTrad(text):
    converter = opencc.OpenCC("s2t.json")
    return converter.convert(text)

def gen(array, traditional=True):
    print("Generating...\n")

    text = "---\n"
    text += "name: {0}\n".format(conf.outputName[:-10])
    text += "version: {0}\n".format(ver.get())
    text += "sort: by_weight\n"
    text += "use_preset_vocabulary: true\n"
    text += "..."
    text += "\n\n"

    for item in array:
        if traditional == False:
            trad = item
        else:
            trad = convertToTrad(item)
        # pinyin = SnowNLP(item).pinyin
        pinyin = pypinyin.pinyin(item, style=pypinyin.NORMAL)
        tab = "\t"

        pinyinStr = ""
        for o in pinyin:
            pinyinStr += o[0]
            pinyinStr += " "
        pinyinStr = pinyinStr[:-1]

        text += trad
        text += tab
        text += pinyinStr
        text += tab
        text += conf.defaultWeight
        text += "\n"
    
    return text

def genFe(artifact=False, 
            avatars=True, 
            homeworld=False, 
            material=True,
            regions=True,
            weapon=True):
    textSea = load.loadSea()
    print("loaded text sea, length {0} bytes.".format(str(len(textSea))))

    array = []
    if(artifact == True):
        ar = Artifact.exec(textSea)
        array.extend(ar)
    
    if(avatars == True):
        av = Avatar.exec(textSea)
        array.extend(av)
        
    if(homeworld == True):
        ho = Homeworld.exec(textSea)
        array.extend(ho)
        
    if(material == True):
        mt = Material.exec(textSea)
        array.extend(mt)
    
    if(regions == True):
        rg = Regions.exec(textSea)
        array.extend(rg)
        
    if(weapon == True):
        wp = Weapon.exec(textSea)
        array.extend(wp)

    bigArray = dedup.exec(array)
    print(type(bigArray[1000]))
    print("Generated {0} abbreviations.".format(str(len(bigArray))))
    
    return bigArray