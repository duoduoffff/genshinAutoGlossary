#! /usr/local/bin/python3

from Common import gen
from Common import conf
from Common import file

if __name__ == '__main__':
    bigArray = gen.genFe()
    tradPrompt = input("Would you like to have traditional characters? [Y/n] ")
    if(tradPrompt == "N" or tradPrompt == "n"):
        genedText = gen.gen(bigArray, traditional=False)
    else:
        genedText = gen.gen(bigArray, traditional=True)

    combinedPath = "./{0}/{1}".format(conf.buildPath, conf.outputName)
    file.FileOperations.writeToFile(genedText, combinedPath)
