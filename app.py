#! /usr/local/bin/python3

import opencc
# from snownlp import SnowNLP
import pypinyin

from Common import load
from Common import file
from Common import dedup
from Common import conf
from Common import getCurrentVersion as ver

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
    text += "name: {0}\n".format(conf.outputName[:-5])
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

if __name__ == '__main__':
    textSea = load.loadSea()
    print("loaded text sea, length {0} bytes.".format(str(len(textSea))))

    artifact = Artifact.exec(textSea)
    avatars = Avatar.exec(textSea)
    homeworld = Homeworld.exec(textSea)
    material = Material.exec(textSea)
    regions = Regions.exec(textSea)
    weapon = Weapon.exec(textSea)

    arrays = []
    arrays.extend(avatars)
    arrays.extend(homeworld)
    arrays.extend(material)
    arrays.extend(regions)
    arrays.extend(weapon)
    arrays.extend(artifact)

    bigArray = dedup.exec(arrays)
    print("Generated {0} abbreviations.".format(str(len(bigArray))))
    tradPrompt = input("Would you like to have traditional characters? [Y/n] ")
    if(tradPrompt == "N" or tradPrompt == "n"):
        genedText = gen(bigArray, traditional=False)
    else:
        genedText = gen(bigArray, traditional=True)

    combinedPath = "./{0}/{1}".format(conf.buildPath, conf.outputName)
    file.FileOperations.writeToFile(genedText, combinedPath)
