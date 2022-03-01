import os, json

def attachLanguagesToCommitsInAnOrderlyFashionAndSaveTheOutputToSomeFilesThatWillBeLocatedInASubDirectOrYOFtheCuRReNtDirECTory(langDict):
    for jsonFile in ([jsonFile for jsonFile in os.listdir('../../../../test/data/') if os.path.isfile(os.path.join('../../../../test/data/',jsonFile))]):
        for l in (json.loads(line) for line in open('../../../../test/data/'+jsonFile,'r') if json.loads(line)['type'] == 'PushEvent'):
            if l['repo']['name'] in langDict: 
                print({ 'repo': l['repo']['name'], 'lang': langDict[l['repo']['name']], 'commits': [message['message'] for message in l['payload']['commits']]})
                break
        break

def buildLangDict():
    langDict = {}
    for dataFile in ([fileName for fileName in os.listdir('../../twoweekdatapackage/') if 'processed' in fileName]):
        for l in (line for line in open('../../twoweekdatapackage/'+dataFile,'r') if ':\n' not in line):
            langDict[l.split(':')[0]] = [(lang.split(',')[0],lang.split(',')[1].rstrip()) for lang in l.split(':')[1].split(';')]
    return langDict
                        
if __name__ == '__main__':
    langDict = buildLangDict()
    #attachLanguagesToCommitsInAnOrderlyFashionAndSaveTheOutputToSomeFilesThatWillBeLocatedInASubDirectOrYOFtheCuRReNtDirECTory(langDict)
    counter = 0
    for k, v in langDict.items():
        counter += 1
        if counter > 1:
            break
        print(k,v)

