import json
from urllib.request import urlopen
from urllib.error import HTTPError
import os

#URL Modifiers

# API URL base  -  Includes /repo switch
apiRepoBase = "https://api.github.com/repos/"

# apiLang adds onto apiRepoBase  -  returns single python object e.g. { "Language": (int)numOfLines, "Language2": (int)numOfLines }
apiLang = "/languages"

# eventID of the event of note
eventID = "PushEvent"

# Holds PushEvent data in form <K,V> = <commitRepo, apiLang_Object>
languagesData = dict()

#Creates unique errLog file
errLog = "errorLog0"
while os.path.exists(errLog):
    num = int(errLog[8:len(errLog)])+1
    errLog = errLog[0:8] + str(num)

count = 0
for line in open('data/2021-01-01-0.json', 'r'):
    if count == 100:
        break
    data = json.loads(line)
    if data['type'] == eventID:
        if len(data['payload']['commits']) == 0:
                f = open('errorLog', 'a')
                f.write("No commit msg: (" + commitRepo + ")\n")
        else:
            commitMsg = data['payload']['commits'][0]['message']

        commitRepo = data['repo']['name']

        if commitRepo not in languagesData:
            try:
                if commitRepo in languagesData:
                    languagesData[commitRepo].append(json.loads(urlopen(apiRepoBase+commitRepo+apiLang).read()))
                else:
                    languagesData[commitRepo] = [json.loads(urlopen(apiRepoBase+commitRepo+apiLang).read())]
            except HTTPError as err:
                if err.code == 404:
                    f = open('errorLog', 'a')
                    f.write("404: (" + commitRepo + "), message(" + commitMsg + ")\n")
                else if err.code == 403:
                    f = open('errorLog', 'a')
                    f.write("403: (" + commitRepo + "), message(" + commitMsg + ")\n")
                else:
                    f = open('errorLog', 'a')
                    f.write(err.code, ": (" + commitRepo + "), message(" + commitMsg + ")\n")


# Partition() breaks the key down into user/partition pair, [0] prints only user
for key in languagesData:
    print(key.partition("/")[0], languagesData[key])
