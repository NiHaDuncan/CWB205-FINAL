import requests
import json
import time
import os

alphabet = "abcdefghijklmnopqrstuvwxyz"

def getAlias(counter):

    aliasDigits = []
    while counter:
        aliasDigits.append(counter % 26)
        counter //=26

    aliasDigits = aliasDigits[::-1]

    ret = ''
    for digit in aliasDigits:
        ret += alphabet[digit]

    return ret

def getData(queryString,expectedMin):
    print('In getData')
    payload = json.dumps({'query': queryString})
    headers = {'Authorization': 'Bearer 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', 'Content-Type': 'application/json'}

    attemptCounter = False
    while True:
        if attemptCounter:
            return "error"
        attemptCounter = True
        try:
            response = requests.request("POST", "https://api.github.com/graphql", headers=headers, data=payload)
        except:
            continue
        if 'response' in locals():
            if len(response.text) > expectedMin:
                return response


f = open('output3_uniq','r')
files = []
for directory in ['data4','data5','data6']:
    files.extend(sorted(filter(lambda fileInDir: 'python_output' in fileInDir and 'processed' not in fileInDir, os.listdir(directory)), key=lambda fileName: int(fileName[13:])))
#files = sorted(filter(lambda fileInDir: 'python_output' in fileInDir and 'processed' not in fileInDir, os.listdir('data4')), key=lambda fileName: int(fileName[13:]))
#files.extend(sorted(filter(lambda fileInDir: 'python_output' in fileInDir and 'processed' not in fileInDir, os.listdir('data5')), key=lambda fileName: int(fileName[13:])))
#files.extend(sorted(filter(lambda fileInDir: 'python_output' in fileInDir and 'processed' not in fileInDir, os.listdir('data6')), key=lambda fileName: int(fileName[13:])))

counter = 1
startingOffset = 0
numberOfSteps = 2272
linesPerStep = 500

for lineSkip in range(startingOffset*500):
    f.readline()
    counter += 1

for currStep in range(startingOffset,numberOfSteps):
    if 'python_output'+str(currStep) in files:
        for lineSkip in range(500):
            f.readline()
            counter += 1
        continue
    print('Starting step', currStep)
    queryList = []
    for j in range(linesPerStep):
        line = f.readline()
        try:
            queryList.append([getAlias(counter),line.split('/')[1].rstrip(),line.split('/')[0]])
        except:
            break
        counter += 1

    queryString = 'query{rateLimit{limit cost remaining resetAt used nodeCount}'
    for tup in queryList:
        queryString += tup[0] + ': repository(name: "' + tup[1] + '", owner: "' + tup[2] + '"){languages(first: 10, orderBy: {field: SIZE, direction: DESC}){edges {size node {name}}}}'
    queryString += '}'

    print('Getting response')
    response = getData(queryString, linesPerStep*10)

    if response == 'error':
        with open('python_errorlog','a') as el: el.write('Error in step ' + str(currStep) + ' continuing')
        print('Error in step', currStep, 'continuing')
    else:
        print('Writing output')
        with open('python_output'+str(currStep),'a') as a: 
            for repo in response.json()['data'].items():
                if repo[1] is None:
                    continue
                if 'languages' in repo[1]:
                    s = ''
                    for lang in repo[1]['languages']['edges']:
                        s += lang['node']['name'] + ',' + str(lang['size']) + ';'
                    s = s[:len(s)-1] + '\n'
                    #print(repo[0] + ' ' + s + '\n')
                    a.write(repo[0] + ':' + s)

        with open('python_errorlog','a') as el: el.write('Step' + str(currStep) + 'completed\n')
