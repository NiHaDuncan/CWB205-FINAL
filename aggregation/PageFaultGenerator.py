import os
import json

'''
    The primary purpose of this script is to generate hard page faults for a
    variable amount of time based on total length of data input.

    Due to an unfixable bug it also trims down PushEvent Data to save space.
'''

def getJsonFiles(dataDir):
    return [jsonFile for jsonFile in os.listdir(dataDir) if os.path.isfile(os.path.join(dataDir, jsonFile))]

def runAnalysis(filePath, repoSet):
    for line in open(filePath):
        data = json.loads(line)
        if data['type'] == "PushEvent":
            repoSet.add(data['repo']['name'])

if __name__ == "__main__":
    dataDir = '../../test/data/new/'
    jsonFiles = getJsonFiles(dataDir)
    repoSet = set()

    for jsonFile in jsonFiles:
        runAnalysis(dataDir + jsonFile, repoSet)

    outputFile = open('output3', 'w')
    for repo in repoSet:
        outputFile.write(repo + '\n')
