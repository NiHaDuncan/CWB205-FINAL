import os
import json

autoMessageList = ["Auto merge by bot","Auto update","Auto updated","Auto update index.js"]

def getJsonFiles(dataDir):
    return [jsonFile for jsonFile in os.listdir(dataDir) if os.path.isfile(os.path.join(dataDir, jsonFile))]

def generateBadRepoList():
    badRepoList = []
    dataDirs = ['data/','data2/','data3/','data4/']
    for dataDir in dataDirs:
        for files in filter(lambda l: 'processed' in l, os.listdir(dataDir)):
            for line in open(dataDir+files, 'r'):
                if line.split(':')[1] == '\n':
                    badRepoList.append((line.split(':')[0]))
    return badRepoList

def getComments(filePath, repoDict):
    for line in open(filePath,'r'):
        data = json.loads(line)
        if data['type'] == "PushEvent":
            for commit in filter(None, data['payload']['commits']):
                if len(commit['message']) > 8 and len(commit['message']) < 560 and commit['message'] not in autoMessageList:
                    if data['repo']['name'] in repoDict:
                        if len(repoDict[data['repo']['name']]['text']) < 8:
                            repoDict[data['repo']['name']]['text'].append(commit['message'])
                    else:
                        repoDict[data['repo']['name']] = {'repo': data['repo']['name'], 'text': [commit['message']]}

if __name__ == "__main__":
    dataDir = '../../test/data/'
    jsonFiles = sorted(getJsonFiles(dataDir))
    with open('commentOutputFileList3','w') as cOFL:
        cOFL.write(str(jsonFiles[25:37]))
    repoDict = dict()
    counter = 0
    print('building repoDict')
    for jsonFile in jsonFiles:
        counter += 1
        if counter > 24 and counter < 37:
            getComments(dataDir + jsonFile, repoDict)
    
    print(counter)
    print('building badRepoList')
    badRepoList = generateBadRepoList()
    print('removing badRepoList entries from repoDict')
    for badRepo in badRepoList:
        repoDict.pop(badRepo,None)

    repoDict = dict(filter(lambda l: len(l[1]['text']) > 1, repoDict.items()))
    print(len(repoDict))
    print(sum(len(v['text']) for v in repoDict.values()))

    outputFile = open('commentOutput3', 'w')
    outputFile.write(json.dumps(sorted(repoDict.values(),key=lambda l: len(l['text']))))
