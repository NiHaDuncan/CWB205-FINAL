import os
import json

totalNumberOfPushEventInAScaryGlobalVariable = 0

def getJsonFiles(dataDir):
    return [jsonFile for jsonFile in os.listdir(dataDir) if os.path.isfile(os.path.join(dataDir, jsonFile))]

def printPerFileAnalysis(fileName, numUniqueRepos, numRepos):
    firstBar = ' ' * (18-len(fileName)) + '|'
    secondBar = "       |"
    print(fileName, firstBar, numUniqueRepos, secondBar, numRepos)

def runAnalysis(filePath):
    global totalNumberOfPushEventInAScaryGlobalVariable


    PushEventCount = 0
    res = dict()
    eventID = "PushEvent"

    for line in open(filePath):
        data = json.loads(line)
        if data['type'] == eventID:
            PushEventCount += 1
            repo = data['repo']['name'].partition("/")
            if repo[2] in res:
                res[repo[2]].add(repo[0])
            else:
                res[repo[2]] = {repo[0]}

    totalNumberOfPushEventInAScaryGlobalVariable += PushEventCount
    printPerFileAnalysis(filePath.split("/")[-1], len(res), PushEventCount)

    return res

if __name__ == "__main__":
    dataDir = '../../data/'
    jsonFiles = getJsonFiles(dataDir)
    repoDict = dict()

    print("Listing number of unique repos per file")
    print("File Name          | Unique Repos | Total Repos")
    for jsonFile in jsonFiles:
        # Apparently python passes objects by reference so .update() isn't needed but I'm too lazy to change that
        repoDict.update(runAnalysis(dataDir + jsonFile))

    # count = Number of API requests required with only partial optimization
    count = 0
    for key in repoDict:
        for user in repoDict[key]:
            count += 1

    print("\nRequests needed with no optimization: ", totalNumberOfPushEventInAScaryGlobalVariable)
    print("Requests needed with partial optimization: ", count)
    print("Requests needed with full optimization: ", len(repoDict))
    print("Ratio of number of optimal API requests / number of PushEvents", (len(repoDict)/totalNumberOfPushEventInAScaryGlobalVariable))
